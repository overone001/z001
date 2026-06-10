# -*- coding: utf-8 -*-
"""
数据模型
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Category:
    """分类模型"""
    id: int
    name: str
    description: str = ""
    created_at: datetime = None


@dataclass
class Tag:
    """标签模型"""
    id: int
    name: str
    color: str = "#808080"
    created_at: datetime = None


@dataclass
class Material:
    """资料模型"""
    id: int
    title: str
    content: str = ""
    category_id: Optional[int] = None
    file_path: Optional[str] = None
    url: Optional[str] = None
    notes: str = ""
    tags: List[Tag] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
