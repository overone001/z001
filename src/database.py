# -*- coding: utf-8 -*-
"""
数据库操作模块
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Any
import config


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def disconnect(self):
        """断开数据库连接"""
        if self.conn:
            self.conn.close()
    
    def init_database(self):
        """初始化数据库表"""
        self.connect()
        cursor = self.conn.cursor()
        
        # 创建分类表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建标签表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                color TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建资料表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                category_id INTEGER,
                file_path TEXT,
                url TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        ''')
        
        # 创建资料-标签关联表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS material_tags (
                material_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (material_id, tag_id),
                FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
        ''')
        
        # 插入预设分类
        for category in config.DEFAULT_CATEGORIES:
            cursor.execute(
                'INSERT OR IGNORE INTO categories (name) VALUES (?)',
                (category,)
            )
        
        # 插入预设标签
        for tag in config.DEFAULT_TAGS:
            cursor.execute(
                'INSERT OR IGNORE INTO tags (name) VALUES (?)',
                (tag,)
            )
        
        self.conn.commit()
    
    def add_material(self, title: str, content: str = "", category_id: int = None,
                    file_path: str = None, url: str = None, notes: str = "",
                    tag_ids: List[int] = None) -> int:
        """添加资料"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO materials (title, content, category_id, file_path, url, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, content, category_id, file_path, url, notes))
        
        material_id = cursor.lastrowid
        
        # 添加标签关联
        if tag_ids:
            for tag_id in tag_ids:
                cursor.execute(
                    'INSERT INTO material_tags (material_id, tag_id) VALUES (?, ?)',
                    (material_id, tag_id)
                )
        
        self.conn.commit()
        return material_id
    
    def get_all_materials(self) -> List[Dict]:
        """获取所有资料"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT m.id, m.title, m.content, c.name as category, m.created_at
            FROM materials m
            LEFT JOIN categories c ON m.category_id = c.id
            ORDER BY m.created_at DESC
        ''')
        
        return [dict(row) for row in cursor.fetchall()]
    
    def search_materials(self, keyword: str) -> List[Dict]:
        """搜索资料"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT m.id, m.title, m.content, c.name as category, m.created_at
            FROM materials m
            LEFT JOIN categories c ON m.category_id = c.id
            WHERE m.title LIKE ? OR m.content LIKE ? OR m.notes LIKE ?
            ORDER BY m.created_at DESC
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_materials_by_category(self, category_id: int) -> List[Dict]:
        """按分类获取资料"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT m.id, m.title, m.content, c.name as category, m.created_at
            FROM materials m
            LEFT JOIN categories c ON m.category_id = c.id
            WHERE m.category_id = ?
            ORDER BY m.created_at DESC
        ''', (category_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_categories(self) -> List[Dict]:
        """获取所有分类"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name FROM categories')
        return [dict(row) for row in cursor.fetchall()]
    
    def get_tags(self) -> List[Dict]:
        """获取所有标签"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name FROM tags')
        return [dict(row) for row in cursor.fetchall()]
    
    def delete_material(self, material_id: int):
        """删除资料"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM materials WHERE id = ?', (material_id,))
        self.conn.commit()
    
    def update_material(self, material_id: int, title: str = None, content: str = None,
                       category_id: int = None, notes: str = None) -> bool:
        """更新资料"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        
        updates = []
        params = []
        
        if title is not None:
            updates.append('title = ?')
            params.append(title)
        if content is not None:
            updates.append('content = ?')
            params.append(content)
        if category_id is not None:
            updates.append('category_id = ?')
            params.append(category_id)
        if notes is not None:
            updates.append('notes = ?')
            params.append(notes)
        
        if not updates:
            return False
        
        updates.append('updated_at = CURRENT_TIMESTAMP')
        params.append(material_id)
        
        query = f"UPDATE materials SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        self.conn.commit()
        
        return True
