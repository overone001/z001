# -*- coding: utf-8 -*-
"""
基础测试
"""

import unittest
import os
import tempfile
from src.database import Database
from src.logic.classifier import Classifier


class TestDatabase(unittest.TestCase):
    """数据库测试"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db = Database(self.temp_db.name)
        self.db.init_database()
    
    def tearDown(self):
        """测试后清理"""
        self.db.disconnect()
        os.unlink(self.temp_db.name)
    
    def test_add_material(self):
        """测试添加资料"""
        material_id = self.db.add_material(
            title="测试资料",
            content="这是一个测试",
            notes="测试备注"
        )
        self.assertGreater(material_id, 0)
    
    def test_get_all_materials(self):
        """测试获取所有资料"""
        self.db.add_material(title="资料1")
        self.db.add_material(title="资料2")
        
        materials = self.db.get_all_materials()
        self.assertEqual(len(materials), 2)
    
    def test_search_materials(self):
        """测试搜索资料"""
        self.db.add_material(title="Python教程")
        self.db.add_material(title="Java指南")
        
        results = self.db.search_materials("Python")
        self.assertEqual(len(results), 1)


class TestClassifier(unittest.TestCase):
    """分类器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.classifier = Classifier()
        self.classifier.add_category("技术", ["Python", "Java", "代码"])
        self.classifier.add_category("文章", ["博客", "新闻", "评论"])
    
    def test_classify(self):
        """测试分类"""
        result = self.classifier.classify("这是一篇Python教程")
        self.assertIn("技术", result)
    
    def test_get_suggestions(self):
        """测试获取建议"""
        suggestions = self.classifier.get_suggestions("Python代码示例")
        self.assertGreater(len(suggestions), 0)


if __name__ == '__main__':
    unittest.main()
