"""
日志工具：统一日志格式，支持控制台+文件双输出（便于调试和问题排查）
"""
import logging
import os
from colorlog import ColoredFormatter
from config import LOG_CONFIG

def get_logger(name: str) -> logging.Logger:
    """
    获取日志实例（支持控制台彩色输出+文件记录）
    :param name: 日志模块名
    :return: logging.Logger实例
    """
    # 创建日志器
    logger = logging.getLogger(name)
    logger.setLevel(LOG_CONFIG["log_level"])
    logger.propagate = False  # 避免重复输出

    # 确保日志文件夹存在
    log_dir = os.path.dirname(LOG_CONFIG["log_file"])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # 控制台处理器（彩色输出）
    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red"
        }
    )
    console_handler.setFormatter(console_formatter)

    # 文件处理器（记录到文件）
    file_handler = logging.FileHandler(LOG_CONFIG["log_file"], encoding="utf-8")
    file_formatter = logging.Formatter(LOG_CONFIG["log_format"])
    file_handler.setFormatter(file_formatter)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger