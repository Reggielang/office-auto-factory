import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from src.checks.utils import os_utils


def get_logger():
    logger = logging.getLogger('OneDragon')
    logger.handlers.clear()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s.%(msecs)03d] [%(filename)s %(lineno)d] [%(levelname)s]: %(message)s',
                                  '%H:%M:%S')

    # 获取项目根目录
    log_file_path = os.path.join(os_utils.get_path_under_work_dir('.log'), 'log.txt')
    # 确保.log文件夹存在
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)  # 创建.log文件夹，如果不存在的话
    archive_handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1, backupCount=3,
                                               encoding='utf-8')
    archive_handler.setLevel(logging.INFO)
    archive_handler.setFormatter(formatter)
    logger.addHandler(archive_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def set_log_level(level: int) -> None:
    """
    显示日志等级
    :param level:
    :return:
    """
    log.setLevel(level)
    for handler in log.handlers:
        handler.setLevel(level)


# 定义日志记录函数
def log_message(message, text_edit):
    """
    记录带时间戳的日志消息到 QTextEdit 中。

    :param message: 要记录的消息文本
    :param text_edit: QTextEdit 对象，用于追加日志
    """
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    formatted_message = f"{current_time} {message}"
    text_edit.append(formatted_message)


log = get_logger()
