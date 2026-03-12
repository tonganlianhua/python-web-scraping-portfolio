# 百度百科爬虫 (BaiduBaike Spider)

一个功能强大的百度百科爬虫，支持词条搜索、内容获取、分类筛选、数据导出和分析。

## 功能特性

✨ **核心功能**
- 📄 爬取百度百科词条信息（词条名、摘要、简介、分类、链接、编辑次数等）
- 🔍 支持关键词搜索词条
- 📖 获取词条完整内容
- 🏷️ 支持按分类筛选（人物、地理、科技、历史等）
- 📊 生成数据分析报告（词条统计、分类分布、热门词条排行等）

📤 **数据导出**
- CSV 格式导出（支持 Excel 打开）
- JSON 格式导出（结构化数据）

🛡️ **反爬策略**
- 随机延时请求
- User-Agent 轮换
- 请求头伪装
- 自动重试机制

## 项目结构

```
baidu-scraper/
├── baidu_scraper.py    # 爬虫核心模块
├── exporter.py          # 数据导出模块
├── analyzer.py          # 数据分析模块
├── demo.py              # 演示脚本
├── test.py              # 测试脚本
├── requirements.txt     # 依赖包
└── README.md           # 项目文档
```

## 安装

### 1. 克隆或下载项目

```bash
cd D:\openclaw\workspace\projects\baidu-scraper
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install requests beautifulsoup4 lxml
```

## 快速开始

### 运行演示脚本

演示脚本会展示所有主要功能：

```bash
python demo.py
```

演示内容包括：
1. 搜索词条
2. 获取单个词条
3. 批量获取词条
4. 按分类筛选
5. 数据导出（CSV 和 JSON）
6. 数据分析报告
7. 获取热门词条

### 运行测试脚本

测试脚本会验证所有功能是否正常：

```bash
python test.py
```

## 使用示例

### 基础用法

```python
from baidu_scraper import BaiduBaikeSpider

# 创建爬虫实例
spider = BaiduBaikeSpider()

# 获取单个词条
entry = spider.get_entry("Python")
if entry:
    print(f"标题: {entry['title']}")
    print(f"摘要: {entry['summary']}")
    print(f"分类: {entry['categories']}")
    print(f"浏览量: {entry['views']}")
```

### 搜索词条

```python
# 搜索词条
results = spider.search_entries("人工智能")
for entry in results:
    print(f"标题: {entry['title']}")
```

### 批量获取词条

```python
# 批量获取
titles = ["机器学习", "深度学习", "神经网络"]
entries = spider.batch_get_entries(titles)
```

### 分类筛选

```python
# 按分类筛选
filtered = spider.filter_by_category(entries, ["计算机", "科学技术"])
for entry in filtered:
    print(f"{entry['title']}: {entry['categories']}")
```

### 数据导出

```python
from exporter import DataExporter

# 导出CSV
DataExporter.export_to_csv(entries, "output/entries.csv")

# 导出JSON
DataExporter.export_to_json(entries, "output/entries.json")

# 同时导出两种格式
DataExporter.export_to_csv_and_json(entries, "output/entries")
```

### 数据分析

```python
from analyzer import DataAnalyzer

# 生成分析报告
analyzer = DataAnalyzer()
report = analyzer.generate_report(entries)

# 打印报告
analyzer.print_report(report)

# 保存报告到文件
analyzer.save_report_to_file(report, "output/report.json")
```

### 获取热门词条

```python
# 获取热门词条
hot_entries = spider.get_hot_entries(limit=10)
for entry in hot_entries:
    print(f"{entry['title']}: {entry['views']} 浏览")
```

## API 文档

### BaiduBaikeSpider

爬虫核心类。

#### 方法

- `__init__()`: 初始化爬虫
- `search_entries(keyword: str, limit: int = 10) -> List[Dict]`: 搜索词条
- `get_entry(title: str) -> Optional[Dict]`: 获取词条完整信息
- `batch_get_entries(titles: List[str]) -> List[Dict]`: 批量获取词条
- `filter_by_category(entries: List[Dict], categories: List[str]) -> List[Dict]`: 按分类筛选
- `get_hot_entries(limit: int = 10) -> List[Dict]`: 获取热门词条
- `clear_cache()`: 清除缓存

#### 返回数据格式

```python
{
    'title': '词条标题',
    'url': '词条链接',
    'summary': '摘要',
    'intro': '简介',
    'categories': ['分类1', '分类2'],
    'content': '完整内容',
    'edit_count': 100,
    'views': 10000,
    'labels': ['标签1', '标签2']
}
```

### DataExporter

数据导出类（静态方法）。

#### 方法

- `export_to_csv(entries: List[Dict], filename: str, encoding: str = 'utf-8-sig') -> bool`: 导出CSV
- `export_to_json(entries: List[Dict], filename: str, encoding: str = 'utf-8') -> bool`: 导出JSON
- `export_to_csv_and_json(entries: List[Dict], base_filename: str) -> Dict[str, bool]`: 同时导出两种格式
- `load_from_json(filename: str) -> Optional[List[Dict]]`: 从JSON加载数据

### DataAnalyzer

数据分析类（静态方法）。

#### 方法

- `generate_report(entries: List[Dict]) -> Dict`: 生成分析报告
- `print_report(report: Dict)`: 打印分析报告
- `save_report_to_file(report: Dict, filename: str)`: 保存报告到文件

#### 报告格式

```python
{
    "summary": {
        "total_entries": 10,
        "total_views": 100000,
        "total_edits": 1000,
        "average_views": 10000.0,
        "average_edits": 100.0
    },
    "category_distribution": {
        "unique_categories": 20,
        "category_distribution": {...},
        "top_10_categories": [...]
    },
    "popular_entries": [...],
    "edit_statistics": {...},
    "content_statistics": {...}
}
```

## 反爬策略

本项目实现了多种反爬策略：

1. **随机延时**: 每次请求之间随机等待 1-3 秒
2. **User-Agent 轮换**: 使用多个不同的 User-Agent 伪装浏览器
3. **请求头伪装**: 添加完整的 HTTP 请求头
4. **自动重试**: 请求失败时自动重试 3 次
5. **缓存机制**: 已获取的词条会缓存，避免重复请求

## 注意事项

⚠️ **使用建议**

1. **请求频率**: 不要过于频繁地请求，建议每次请求间隔至少 1 秒
2. **数据使用**: 本项目仅用于学习和研究，不得用于商业用途
3. **遵守协议**: 请遵守百度百科的使用协议和robots.txt规定
4. **网络连接**: 确保网络连接正常，能够访问百度百科

⚠️ **已知限制**

1. 某些词条可能有反爬保护，可能无法获取
2. 热门词条榜单页面可能需要更复杂的解析
3. 大量请求可能被百度百科临时封禁

## 常见问题

### Q: 为什么获取某些词条失败？

A: 可能的原因：
- 词条不存在或已被删除
- 该词条有特殊的反爬保护
- 网络连接问题
- 被临时封禁（等待一段时间再试）

### Q: 如何避免被百度百科封禁？

A: 建议：
- 降低请求频率
- 使用缓存避免重复请求
- 不要在短时间内请求大量词条
- 遵守反爬策略（项目已实现）

### Q: 导出的CSV文件乱码怎么办？

A: 项目使用 `utf-8-sig` 编码，Excel 可以正常打开。如果仍然乱码，请尝试使用其他编辑器或转换编码。

## 依赖包

- `requests>=2.31.0`: HTTP 请求库
- `beautifulsoup4>=4.12.0`: HTML 解析库
- `lxml>=4.9.0`: XML/HTML 解析器

## 许可证

本项目仅供学习和研究使用。

## 贡献

欢迎提交问题和改进建议！

## 更新日志

### v1.0.0 (2026-03-12)

- ✨ 初始版本发布
- 📄 支持词条搜索和获取
- 🏷️ 支持分类筛选
- 📤 支持 CSV 和 JSON 导出
- 📊 支持数据分析报告
- 🛡️ 实现反爬策略

## 作者

新新 (AI助手)

## 致谢

感谢百度百科提供的数据来源。

---

**Happy Coding! 🚀**
