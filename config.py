# 配置文件
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 数据库路径
DB_PATH = os.path.join(BASE_DIR, 'data', 'materials.db')

# 数据目录
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 创建数据目录
os.makedirs(DATA_DIR, exist_ok=True)

# 应用配置
APP_TITLE = "资料库"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# 预设分类
DEFAULT_CATEGORIES = [
    "文档",
    "图片",
    "链接",
    "笔记",
    "视频",
    "其他"
]

# 预设标签
DEFAULT_TAGS = [
    "重要",
    "待处理",
    "已完成",
    "参考"
]
