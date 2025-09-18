"""
内容排除检测模块：调用大模型判断图片是否需要排除（非动漫、低质量等）
"""
from openai import OpenAI
from config import MODEL_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

# 初始化大模型客户端（复用client，避免重复创建）
client = OpenAI(
    base_url=MODEL_CONFIG["base_url"],
    api_key=MODEL_CONFIG["api_key"]
)

# 内容排除检测提示词
EXCLUSION_PROMPT = """请判断以下图像是否需要被排除，并返回指定格式的JSON：
### 一、需要排除的内容类型及特征
只要符合以下任何一种特征，均需排除：
#### 1. 非动漫内容
- **现实照片**：包含真实生活物件、真实人类、真实动物、真实纸张质感等；
- **真实手机截图**：存在系统级真实UI元素、真实交互控件等；
- **电脑截图特征**：任务栏、窗口标题栏、高亮截图框等；
- **信息类图像**：以文字信息传递为核心；
- **游戏截图**：含角色属性、用户信息、功能按钮。

#### 2. 非插画类动漫内容
- **漫画分镜**：使用多种矩形或方形分隔画面的漫画页面；
- **动漫截图/画面帧**：来自动画视频的截图。

#### 3. 低质量内容
- **模糊图像**：整体清晰度低或分辨率小于600*600；
- **有划痕图像**：画面存在明显线条状划痕瑕疵；
- **无意义图像**：内容空洞，没有实际动漫主体。

#### 4. 文字叠加内容
- **过多文字**：画面中存在大量文字覆盖；
- **刺眼文字**：颜色、大小或位置过于突兀的文字；
- **含emoji表情**：任何位置出现emoji表情符号。

### 二、返回格式要求
仅需返回JSON格式，无需任何文字解释：
- 若符合上述任何一类特征，返回：{"is_excluded": true}
- 若不符合任何一类特征（属于高质量动漫插画），返回：{"is_excluded": false}"""


def detect_exclusion(image_base64: str) -> tuple[bool, str]:
    """
    调用大模型检测图片是否需要排除
    :param image_base64: 图片Base64字符串
    :return: (是否需要排除, 检测详情)
    """
    if not image_base64:
        logger.error("内容排除检测失败：Base64字符串为空")
        return False, "Base64字符串为空"

    try:
        # 调用大模型
        response = client.chat.completions.create(
            model=MODEL_CONFIG["model_name"],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": EXCLUSION_PROMPT},
                        {"type": "image_url", "image_url": {"url": f"data:image/webp;base64,{image_base64}"}}
                    ]
                }
            ]
        )

        # 解析结果
        result_str = response.choices[0].message.content.strip()
        if "{" not in result_str or "}" not in result_str:
            return False, f"模型返回格式异常：{result_str[:50]}"

        import json
        result_dict = json.loads(result_str)
        is_excluded = result_dict.get("is_excluded", False)
        return is_excluded, f"模型判定：{'需排除' if is_excluded else '无需排除'}"

    except Exception as e:
        logger.error(f"内容排除检测调用失败 | 错误：{str(e)[:100]}")
        return False, f"调用出错：{str(e)[:50]}"