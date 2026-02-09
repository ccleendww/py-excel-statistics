"""
UI 配置文件：字体与大小统一管理
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# 默认字体文件（如果存在），UI 会尝试使用此字体家族
DEFAULT_FONT_FILE = os.path.join(ASSETS_DIR, "JetBrainsMapleMono-Regular.ttf")
DEFAULT_FONT_FAMILY = "JetBrains Maple Mono"

# 字体大小配置
TITLE_FONT_SIZE = 14
LISTBOX_FONT_SIZE = 14
BUTTON_FONT_SIZE = 14
TEXT_FONT_SIZE = 12

# 刷新间隔（秒）
AUTO_REFRESH_INTERVAL = 0.5
