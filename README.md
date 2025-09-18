# 漫画图片筛选工具

一个用于批量筛选漫画图片的工具，支持**晕影检测、NSFW内容过滤、分辨率筛选、非动漫内容排除**，最终输出高质量动漫插画。
声明，本项目通过调用豆包大模型的Doubao-Seed-1.6 Vision

## 功能特性
1. **晕影检测**：自动识别带有晕影效果的图片（如截图暗角），单独分类保存；
2. **NSFW过滤**：调用大模型检测色情、低俗内容，避免违规图片；
3. **分辨率筛选**：过滤低于600×600像素的低质量图片；
4. **内容排除**：排除非动漫内容（现实照片、截图、游戏截图等）；
5. **日志系统**：支持控制台彩色输出和文件记录，便于问题排查；
6. **模块化设计**：代码结构清晰，易扩展、易维护。


## 环境要求
- Python 3.8+ (本人使用3.10)
- 依赖包：见 `requirements.txt`


## 快速开始

### 1. 克隆项目
git clone https://github.com/your-username/comic_filter.git
cd comic_filter


### 2. 安装依赖 
pip install -r requirements.txt

### 3. 配置参数 
- 修改 config.py 中的核心配置（根据实际环境调整）：

# 输入图片文件夹（可添加多个）
INPUT_FOLDERS = [
    r"C:\Users\ZhuanZ（无密码）\Desktop\漫画筛选\测试2"
]

# 大模型API配置（替换为你的API Key）
MODEL_CONFIG = {
    "base_url": "https://ark.cn-beijing.volces.com/api/v3",
    "api_key": "your-api-key-here",  # 重要：替换为你的 API Key
    "model_name": "ep-20250917105406-tk7ll"
}

# 检测参数（可根据需求优化）
VIGNETTE_CONFIG = {
    "edge_ratio": 0.15,               # 边缘区域占比（15%）
    "brightness_ratio_threshold": 0.75,  # 边缘/中心亮度比阈值
    "blur_kernel": (7, 7)             # 高斯模糊核大小
}

### 4. 运行程序
python main.py


