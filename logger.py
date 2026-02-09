"""
日志模块 - 记录应用运行日志和错误信息
"""
import os
import datetime
import logging

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 设置日志
log_file = os.path.join(LOG_DIR, f"app_{datetime.datetime.now().strftime('%Y%m%d')}.log")
logger = logging.getLogger("ExcelApp")
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(log_file, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 也输出到控制台以便调试
console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)


def log_info(msg):
    logger.info(msg)


def log_error(msg):
    logger.error(msg)


def log_debug(msg):
    logger.debug(msg)


def log_exception(msg, exc):
    logger.exception(f"{msg}: {exc}")
