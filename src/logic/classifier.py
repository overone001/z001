# -*- coding: utf-8 -*-
"""
分类逻辑模块
"""

from typing import List, Dict


class Classifier:
    """资料分类器"""
    
    def __init__(self):
        self.categories = {}
        self.rules = {}
    
    def add_category(self, name: str, keywords: List[str]):
        """添加分类和对应关键词"""
        self.categories[name] = keywords
    
    def classify(self, text: str) -> List[str]:
        """根据文本自动分类"""
        matched_categories = []
        text_lower = text.lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    matched_categories.append(category)
                    break
        
        return matched_categories if matched_categories else ["其他"]
    
    def get_suggestions(self, text: str) -> Dict[str, float]:
        """获取分类建议（带置信度）"""
        suggestions = {}
        text_lower = text.lower()
        
        for category, keywords in self.categories.items():
            matches = sum(1 for kw in keywords if kw.lower() in text_lower)
            if matches > 0:
                confidence = matches / len(keywords)
                suggestions[category] = confidence
        
        # 按置信度排序
        return dict(sorted(suggestions.items(), key=lambda x: x[1], reverse=True))
