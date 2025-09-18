"""
图像预处理工具：晕影检测、亮度分析、分辨率检查
"""
import cv2
import numpy as np
from PIL import Image
from config import VIGNETTE_CONFIG, RESOLUTION_CONFIG
from utils.logger import get_logger

# 初始化日志
logger = get_logger(__name__)


def verify_image_integrity(image_path: str) -> bool:
    """
    验证图片文件完整性（避免损坏文件导致后续报错）
    :param image_path: 图片路径
    :return: 完整返回True，损坏返回False
    """
    try:
        with Image.open(image_path) as img:
            img.verify()  # 验证文件完整性
        return True
    except Exception as e:
        logger.error(f"图片验证失败：{image_path} | 错误：{str(e)[:50]}")
        return False


def check_resolution(image_path: str) -> tuple[bool, tuple[int, int]]:
    """
    检查图片分辨率是否符合要求
    :param image_path: 图片路径
    :return: (是否符合要求, (宽度, 高度))
    """
    min_w, min_h = RESOLUTION_CONFIG["min_width"], RESOLUTION_CONFIG["min_height"]
    try:
        with Image.open(image_path) as img:
            width, height = img.size
        is_valid = width >= min_w and height >= min_h
        return is_valid, (width, height)
    except Exception as e:
        logger.error(f"分辨率检查失败：{image_path} | 错误：{str(e)[:50]}")
        return False, (0, 0)


def detect_vignette_effect(image_path: str) -> tuple[bool, str]:
    """
    检测图片是否存在晕影效果（优化版）
    :param image_path: 图片路径
    :return: (是否有晕影, 检测详情)
    """
    edge_ratio = VIGNETTE_CONFIG["edge_ratio"]
    brightness_threshold = VIGNETTE_CONFIG["brightness_ratio_threshold"]
    blur_kernel = VIGNETTE_CONFIG["blur_kernel"]

    try:
        # 读取图片（支持中文路径）并转换为OpenCV格式
        with Image.open(image_path) as img_pil:
            img_rgb = img_pil.convert("RGB")
            img = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)

        # 灰度化 + 高斯模糊（去噪）
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, blur_kernel, 0)
        height, width = blurred.shape

        # 计算边缘区域宽度（确保至少5个像素）
        edge_width = int(min(height, width) * edge_ratio)
        edge_width = max(edge_width, 5)

        # 划分中心区域与边缘区域
        center_region = blurred[edge_width:height-edge_width, edge_width:width-edge_width]
        if center_region.size == 0:
            return False, "图片尺寸过小，无法划分区域"

        # 提取四个边缘条带
        top_edge = blurred[:edge_width, :]
        bottom_edge = blurred[height-edge_width:, :]
        left_edge = blurred[edge_width:height-edge_width, :edge_width]
        right_edge = blurred[edge_width:height-edge_width, width-edge_width:]

        # 计算亮度统计量
        center_mean = np.mean(center_region)
        edge_means = [np.mean(top_edge), np.mean(bottom_edge), np.mean(left_edge), np.mean(right_edge)]
        edge_mean = np.mean(edge_means)
        brightness_ratio = edge_mean / center_mean if center_mean > 0 else 0

        # 判断晕影
        has_vignette = brightness_ratio < brightness_threshold
        detail = (f"中心亮度:{center_mean:.1f}, 边缘亮度:{edge_mean:.1f}, "
                  f"亮度比:{brightness_ratio:.2f}, 阈值:{brightness_threshold}")
        return has_vignette, detail

    except Exception as e:
        logger.error(f"晕影检测失败：{image_path} | 错误：{str(e)[:50]}")
        return False, f"检测出错：{str(e)[:30]}"