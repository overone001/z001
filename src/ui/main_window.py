# -*- coding: utf-8 -*-
"""
主窗口UI - 完全简化版本
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QLabel,
    QMessageBox
)
from PyQt5.QtCore import Qt
import config
from src.database import Database


class MainWindow(QMainWindow):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle(config.APP_TITLE)
        self.setGeometry(100, 100, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 顶部工具栏
        toolbar_layout = QHBoxLayout()
        
        # 搜索框
        search_label = QLabel("搜索:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入关键词搜索...")
        self.search_input.returnPressed.connect(self.search_materials)
        
        # 分类筛选
        category_label = QLabel("分类:")
        self.category_combo = QComboBox()
        self.category_combo.addItem("全部", 0)
        self.load_categories()
        self.category_combo.currentIndexChanged.connect(self.filter_by_category)
        
        # 新增按钮
        self.add_btn = QPushButton("新增")
        self.add_btn.setFixedWidth(80)
        self.add_btn.clicked.connect(self.show_add_form)
        
        # 删除按钮
        self.delete_btn = QPushButton("删除")
        self.delete_btn.setFixedWidth(80)
        self.delete_btn.clicked.connect(self.delete_material)
        
        # 刷新按钮
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.setFixedWidth(80)
        self.refresh_btn.clicked.connect(self.load_materials)
        
        toolbar_layout.addWidget(search_label)
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(category_label)
        toolbar_layout.addWidget(self.category_combo)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.delete_btn)
        toolbar_layout.addWidget(self.refresh_btn)
        
        main_layout.addLayout(toolbar_layout)
        
        # 数据表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "标题", "分类", "内容", "创建时间"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(3, 300)
        
        main_layout.addWidget(self.table)
        
        # 加载数据
        self.load_materials()
    
    def load_categories(self):
        """加载分类到下拉框"""
        try:
            categories = self.db.get_categories()
            for category in categories:
                self.category_combo.addItem(category['name'], category['id'])
        except:
            pass
    
    def load_materials(self):
        """加载所有资料"""
        try:
            materials = self.db.get_all_materials()
            self.display_materials(materials)
        except:
            pass
    
    def display_materials(self, materials):
        """在表格中显示资料"""
        self.table.setRowCount(0)
        
        for row, material in enumerate(materials):
            self.table.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(material['id']))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, id_item)
            
            # 标题
            title_item = QTableWidgetItem(material['title'])
            title_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, title_item)
            
            # 分类
            category_item = QTableWidgetItem(material['category'] or "未分类")
            category_item.setFlags(category_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 2, category_item)
            
            # 内容
            content = material['content'][:100] if material['content'] else ""
            content_item = QTableWidgetItem(content)
            content_item.setFlags(content_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 3, content_item)
            
            # 创建时间
            time_item = QTableWidgetItem(material['created_at'][:10] if material['created_at'] else "")
            time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 4, time_item)
    
    def search_materials(self):
        """搜索资料"""
        keyword = self.search_input.text().strip()
        if not keyword:
            self.load_materials()
            return
        
        try:
            materials = self.db.search_materials(keyword)
            self.display_materials(materials)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"搜索失败: {str(e)}")
    
    def filter_by_category(self):
        """按分类筛选"""
        category_id = self.category_combo.currentData()
        
        if category_id == 0:  # 全部
            self.load_materials()
        else:
            try:
                materials = self.db.get_materials_by_category(category_id)
                self.display_materials(materials)
            except:
                pass
    
    def show_add_form(self):
        """显示添加表单 - 使用消息框"""
        msg = "输入格式: 标题|分类|内容|备注\n\n例如:\nPython教程|文档|Python是一种编程语言|重要"
        
        result = QMessageBox.information(
            self, 
            "新增资料",
            msg,
            QMessageBox.Ok | QMessageBox.Cancel
        )
        
        if result == QMessageBox.Ok:
            # 逐项输入
            self.add_material_step_by_step()
    
    def add_material_step_by_step(self):
        """一步步添加资料"""
        from PyQt5.QtWidgets import QInputDialog
        
        # 输入标题
        title, ok = QInputDialog.getText(self, "新增资料 - 第1步", "请输入标题:")
        if not ok or not title.strip():
            QMessageBox.information(self, "取消", "已取消添加")
            return
        
        # 选择分类
        categories = self.db.get_categories()
        items = [cat['name'] for cat in categories]
        
        if not items:
            QMessageBox.warning(self, "错误", "没有可用的分类")
            return
        
        item, ok = QInputDialog.getItem(self, "新增资料 - 第2步", "请选择分类:", items)
        if not ok:
            QMessageBox.information(self, "取消", "已取消添加")
            return
        
        category_id = next(cat['id'] for cat in categories if cat['name'] == item)
        
        # 输入内容
        content, ok = QInputDialog.getMultiLineText(self, "新增资料 - 第3步", "请输入内容:")
        if not ok:
            QMessageBox.information(self, "取消", "已取消添加")
            return
        
        # 输入备注
        notes, ok = QInputDialog.getMultiLineText(self, "新增资料 - 第4步", "请输入备注(可选):")
        if not ok:
            notes = ""
        
        # 保存
        try:
            self.db.add_material(
                title=title.strip(),
                content=content.strip(),
                category_id=category_id,
                notes=notes.strip()
            )
            QMessageBox.information(self, "成功", "资料已添加!")
            self.load_materials()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"添加失败: {str(e)}")
    
    def delete_material(self):
        """删除选中的资料"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "错误", "请先选择要删除的资料")
            return
        
        material_id = int(self.table.item(current_row, 0).text())
        title = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, 
            "确认删除", 
            f"确定要删除《{title}》吗?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_material(material_id)
                self.load_materials()
                QMessageBox.information(self, "成功", "资料已删除!")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除失败: {str(e)}")
