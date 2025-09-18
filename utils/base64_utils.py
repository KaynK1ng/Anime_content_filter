"""
Base64 编码工具：将图片转换为Base64字符串（用于大模型输入）
"""
import base64
import os
from utils.logger import get_logger

logger = get_logger(__name__)


def image_to_base64(image_path: str) -> str | None:
    """
    将图片文件编码为Base64字符串
    :param image_path: 图片路径
    :return: Base64字符串（失败返回None）
    """
    if not os.path.exists(image_path):
        logger.error(f"图片路径不存在：{image_path}")
        return None

    try:
        with open(image_path, "rb") as image_file:
            # 编码为Base64并转为UTF-8字符串
            base64_str = base64.b64encode(image_file.read()).decode("utf-8")
        return base64_str
    except Exception as e:
        logger.error(f"图片Base64编码失败：{image_path} | 错误：{str(e)[:50]}")
        return None