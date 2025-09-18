"""
漫画筛选主程序：流程控制入口
执行流程：初始化文件夹 → 遍历图片 → 晕影检测 → NSFW检测 → 分辨率检测 → 漫画内容排除检测 → 结果保存
"""
import os
from config import INPUT_FOLDERS, SUPPORTED_FORMATS, FOLDER_CONFIG
from utils.file_utils import init_folders, copy_image_to_target
from utils.image_processor import verify_image_integrity, check_resolution, detect_vignette_effect
from utils.base64_utils import image_to_base64
from model.nsfw_detector import detect_nsfw
from model.exclusion_detector import detect_exclusion
from utils.logger import get_logger

# 初始化日志
logger = get_logger("main")

def process_single_image(image_path: str) -> None:
    """
    处理单张图片（核心流程）
    :param image_path: 图片路径
    """
    filename = os.path.basename(image_path)
    logger.info(f"开始处理图片：{filename}")

    # 1. 验证图片完整性
    if not verify_image_integrity(image_path):
        return

    # 2. 晕影检测（优先级最高，检测到直接保存）
    has_vignette, vignette_detail = detect_vignette_effect(image_path)
    if has_vignette:
        copy_image_to_target(image_path, "vignette")
        logger.info(f"[晕影检测] 已保存：{filename} | {vignette_detail}")
        return

    # 3. 图片Base64编码（后续大模型需要）
    image_base64 = image_to_base64(image_path)
    if not image_base64:
        return

    # 4. NSFW检测
    is_nsfw, nsfw_detail = detect_nsfw(image_base64)
    if is_nsfw:
        copy_image_to_target(image_path, "nsfw")
        logger.info(f"[NSFW检测] 已保存：{filename} | {nsfw_detail}")
        return

    # 5. 分辨率检测
    is_valid_res, (width, height) = check_resolution(image_path)
    if not is_valid_res:
        copy_image_to_target(image_path, "low_resolution")
        logger.info(f"[分辨率检测] 已保存：{filename} | 尺寸：{width}x{height}（低于600x600）")
        return

    # 6. 内容排除检测
    is_excluded, exclusion_detail = detect_exclusion(image_base64)
    target_key = "excluded" if is_excluded else "normal"
    copy_image_to_target(image_path, target_key)
    logger.info(f"[内容排除检测] 已保存：{filename} | {exclusion_detail}")


def batch_process() -> None:
    """
    批量处理所有输入文件夹中的图片
    """
    # 初始化结果文件夹
    init_folders()
    logger.info("="*50)
    logger.info("开始批量处理图片")
    logger.info(f"输入文件夹：{INPUT_FOLDERS}")
    logger.info(f"支持格式：{SUPPORTED_FORMATS}")
    logger.info("="*50)

    # 遍历所有输入文件夹
    total_count = 0
    for folder in INPUT_FOLDERS:
        if not os.path.exists(folder):
            logger.error(f"输入文件夹不存在：{folder}，跳过该文件夹")
            continue

        logger.info(f"\n正在处理文件夹：{folder}")
        # 遍历文件夹中的文件
        for filename in os.listdir(folder):
            # 只处理支持的图片格式
            if not filename.lower().endswith(SUPPORTED_FORMATS):
                continue

            image_path = os.path.join(folder, filename)
            total_count += 1
            process_single_image(image_path)

    # 输出统计结果
    logger.info("\n" + "="*50)
    logger.info(f"批量处理完成！总计处理图片：{total_count}张")
    for key, path in FOLDER_CONFIG.items():
        file_count = len([f for f in os.listdir(path) if f.lower().endswith(SUPPORTED_FORMATS)])
        logger.info(f"{key}：{file_count}张 → 路径：{path}")
    logger.info("="*50)


if __name__ == "__main__":
    batch_process()