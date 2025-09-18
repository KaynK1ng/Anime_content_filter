"""
项目配置文件：所有路径、参数统一管理，便于修改
"""
import os

# -------------------------- 基础路径配置 --------------------------
# 项目根目录（自动获取，无需手动修改）
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# 输入图片文件夹（需根据实际环境修改）
INPUT_FOLDERS = [
    r"C:\Users\ZhuanZ（无密码）\Desktop\Anime_content_filter\测试2"  #修改路径（例如：'···\zip1'）
]
# 结果保存根目录
RESULT_ROOT = os.path.join(ROOT_DIR, "result")  

# -------------------------- 结果文件夹配置 --------------------------
# 各类型结果的保存路径（自动创建）
FOLDER_CONFIG = {
    "vignette": os.path.join(RESULT_ROOT, "有晕影效果的图片"),
    "nsfw": os.path.join(RESULT_ROOT, "nsfw图片"),
    "low_resolution": os.path.join(RESULT_ROOT, "因分辨率低而被移除"),
    "excluded": os.path.join(RESULT_ROOT, "被移除"),
    "normal": os.path.join(RESULT_ROOT, "正常漫画")
}

# -------------------------- 图像检测参数配置 --------------------------
# 晕影检测参数
VIGNETTE_CONFIG = {
    "edge_ratio": 0.15,                  # 边缘区域占比（15%）
    "brightness_ratio_threshold": 0.85,  # 边缘/中心亮度比阈值
    "blur_kernel": (7, 7)                # 高斯模糊核大小
}

# 分辨率检测参数
RESOLUTION_CONFIG = {
    "min_width": 600,
    "min_height": 600
}

# 支持的图片格式
SUPPORTED_FORMATS = (".webp", ".jpg", ".jpeg", ".png", ".bmp")

# -------------------------- 大模型配置 --------------------------
MODEL_CONFIG = {
    "base_url": "https://ark.cn-beijing.volces.com/api/v3",  # 挂的是Doubao-Seed-1.6-vision的API
    "api_key": "fdd23614-b6d4-48c6-8e00-829dd7da1405",  
    "model_name": "ep-20250917105406-tk7ll"
}

# -------------------------- 日志配置 --------------------------
LOG_CONFIG = {
    "log_file": os.path.join(ROOT_DIR, "logs/comic_filter.log"),
    "log_level": "INFO",  # DEBUG/INFO/WARNING/ERROR
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}