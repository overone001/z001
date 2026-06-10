# 资料库 (z001)

一个可以分类归纳资料的桌面助手

## 功能特性

- 📁 自动分类资料（支持文件、链接、笔记）
- 🏷️ 灵活的标签和分类系统
- 🔍 全文搜索功能
- 💾 本地 SQLite 数据库存储
- 📤 导入导出功能
- 🎨 简洁易用的界面

## 系统需求

- Python 3.7+
- PyQt5
- SQLite3

## 安装

```bash
git clone https://github.com/overone001/z001.git
cd z001
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 项目结构

```
z001/
├── README.md                # 项目说明
├── requirements.txt         # 依赖包列表
├── config.py               # 配置文件
├── main.py                 # 主程序入口
├── src/
│   ├── database.py         # 数据库操作
│   ├── models.py           # 数据模型
│   ├── ui/
│   │   └── main_window.py  # 主界面
│   └── logic/
│       └── classifier.py   # 分类逻辑
└── tests/
    └── test_basic.py       # 基础测试
```

## 使用指南

### 添加资料
1. 点击"新增"按钮
2. 输入资料信息（标题、内容、分类、标签）
3. 点击"保存"

### 分类资料
- 预设分类：文档、图片、链接、笔记等
- 支持自定义分类
- 支持多标签标记

### 搜索资料
- 按关键词搜索
- 按分类筛选
- 按标签过滤

## 开发计划

- [ ] 基础UI界面实现
- [ ] 数据库操作完善
- [ ] 分类和搜索功能
- [ ] 导入导出功能
- [ ] 数据备份功能

## 许可证

MIT License
