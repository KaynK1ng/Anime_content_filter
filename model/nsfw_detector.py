"""
NSFW 检测模块：调用大模型判断图片是否包含NSFW内容
"""
from openai import OpenAI
from config import MODEL_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

# 初始化大模型客户端
client = OpenAI(
    base_url=MODEL_CONFIG["base_url"],
    api_key=MODEL_CONFIG["api_key"]
)

# NSFW 检测提示词（集中管理，便于修改）
NSFW_PROMPT = """请判断以下图像是否包含NSFW（不适合公开观看的色情、低俗等成人内容），具体判定标准如下：
### 一、需判定为NSFW的低俗色情特征（符合任一即判定为true）
1. **隐私部位暴露**：
   - 直接暴露生殖器官（无论男女）、臀部（无衣物或衣物仅覆盖极小部分，无法遮挡核心区域）；
   - 女性乳房完全暴露（无衣物覆盖），或内衣外穿且乳房裸露区域超过50%；
   - 男性乳头及胸部下方区域因姿势/衣物问题裸露超过胸部总面积的60%。
2. **过度性暗示暴露**：
   - 女性乳沟暴露超过2指宽度，且搭配刻意俯身、挺胸等强调性特征的姿势；
   - 衣物刻意设计成“仅遮挡极小范围关键部位”，其余大面积皮肤裸露；
   - 图像聚焦于性特征部位，且无合理场景支撑。
3. **低俗色情行为/姿势**：
   - 存在模拟性行为的姿势；
   - 图像包含色情道具；
   - 人物表情或动作带有明显性挑逗意味。

### 二、无需判定为NSFW的正常场景
- 正常穿搭的乳沟、正常泳衣；
- 艺术创作、医疗科普图像；
- 儿童正常裸露。

### 三、返回格式要求
仅需返回JSON格式，无需任何文字解释：
- 若符合上述NSFW特征，返回：{"is_nsfw": true}
- 若不符合任何NSFW特征，返回：{"is_nsfw": false}"""


def detect_nsfw(image_base64: str) -> tuple[bool, str]:
    """
    调用大模型检测NSFW内容
    :param image_base64: 图片Base64字符串
    :return: (是否为NSFW, 检测详情)
    """
    if not image_base64:
        logger.error("NSFW检测失败：Base64字符串为空")
        return False, "Base64字符串为空"

    try:
        # 调用大模型
        response = client.chat.completions.create(
            model=MODEL_CONFIG["model_name"],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": NSFW_PROMPT},
                        {"type": "image_url", "image_url": {"url": f"data:image/webp;base64,{image_base64}"}}
                    ]
                }
            ]
        )

        # 解析结果
        result_str = response.choices[0].message.content.strip()
        if "{" not in result_str or "}" not in result_str:
            return False, f"模型返回格式异常：{result_str[:50]}"

        # 提取JSON（兼容模型可能的多余字符）
        import json
        result_dict = json.loads(result_str)
        is_nsfw = result_dict.get("is_nsfw", False)
        return is_nsfw, f"模型判定：{'NSFW' if is_nsfw else '非NSFW'}"

    except Exception as e:
        logger.error(f"NSFW检测调用失败 | 错误：{str(e)[:100]}")
        return False, f"调用出错：{str(e)[:50]}"