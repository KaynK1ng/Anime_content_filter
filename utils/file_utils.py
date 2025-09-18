"""
文件操作工具：创建文件夹、复制文件等（避免重复代码）
"""
import os
import shutil
from config import FOLDER_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)


def init_folders() -> None:
    """
    初始化所有结果文件夹（不存在则创建）
    """
    for folder_path in FOLDER_CONFIG.values():
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"创建结果文件夹：{folder_path}")
        else:
            logger.debug(f"结果文件夹已存在：{folder_path}")


def copy_image_to_target(image_path: str, target_folder_key: str) -> bool:
    """
    将图片复制到指定结果文件夹
    :param image_path: 源图片路径
    :param target_folder_key: 目标文件夹key（对应FOLDER_CONFIG的key）
    :return: 复制成功返回True
    """
    if target_folder_key not in FOLDER_CONFIG:
        logger.error(f"无效的目标文件夹key：{target_folder_key}")
        return False

    target_folder = FOLDER_CONFIG[target_folder_key]
    filename = os.path.basename(image_path)
    target_path = os.path.join(target_folder, filename)

    try:
        # 复制文件（保留元数据）
        shutil.copy2(image_path, target_path)
        logger.debug(f"图片复制成功：{filename} → {target_folder}")
        return True
    except Exception as e:
        logger.error(f"图片复制失败：{filename} | 错误：{str(e)[:50]}")
        return False