#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
资料库主程序入口
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.database import Database
import config


def main():
    # 初始化数据库
    db = Database(config.DB_PATH)
    db.init_database()
    
    # 创建应用
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow(db)
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
