# 新闻聚合器 / News Aggregator

## 项目简介 / Project Introduction

这是一个便捷的新闻聚合工具，可以从人民网、新华网、澎湃新闻等多个权威新闻源获取最新资讯，并提供关键词搜索、数据分析等功能。

A convenient news aggregation tool that fetches the latest news from multiple authoritative sources like People's Daily, Xinhua News, and The Paper, with features like keyword search and data analysis.

## 功能特性 / Features

✅ **多源聚合** / Multi-source aggregation  
聚合人民网、新华网、澎湃新闻等权威新闻源
Aggregates authoritative news sources like People's Daily, Xinhua News, and The Paper

✅ **实时更新** / Real-time updates  
基于RSS订阅，实时获取最新新闻内容
Based on RSS subscriptions, fetches latest news content in real-time

✅ **关键词搜索** / Keyword search  
支持通过关键词快速筛选感兴趣的新闻
Supports quick filtering of news of interest through keywords

✅ **数据分析** / Data analysis  
统计各来源新闻数量，生成分析报告
Statistics of news count from each source, generates analysis reports

✅ **多格式导出** / Multi-format export  
支持Excel和JSON格式导出，便于后续处理
Supports Excel and JSON format export for easy subsequent processing

## 技术栈 / Tech Stack

- **Python 3.8+**: 主要开发语言 / Main development language
- **Feedparser**: RSS/Atom解析 / RSS/Atom parsing
- **Requests**: HTTP请求库 / HTTP request library
- **BeautifulSoup4**: HTML解析 / HTML parsing
- **Pandas**: 数据处理和导出 / Data processing and export
- **OpenPyXL**: Excel文件读写 / Excel file read/write
- **JSON**: 数据存储格式 / Data storage format

## 安装说明 / Installation

### 1. 克隆项目 / Clone Project

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo/projects/news-aggregator
```

### 2. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

或逐个安装 / Or install individually:

```bash
pip install requests beautifulsoup4 lxml feedparser pandas openpyxl
```

## 使用方法 / Usage

### 基本使用 / Basic Usage

```bash
python news_aggregator.py
```

程序会自动获取所有新闻源的最新资讯。

The program automatically fetches the latest news from all sources.

### 代码示例 / Code Example

```python
from news_aggregator import NewsAggregator

# 创建聚合器实例
aggregator = NewsAggregator()

# 获取所有新闻源
news_list = aggregator.fetch_all(limit=20)

# 关键词搜索
filtered_news = aggregator.filter_by_keyword('经济')

# 导出为Excel
aggregator.export_to_excel('news_results.xlsx')

# 导出为JSON
aggregator.export_to_json('news_results.json')

# 打印统计
aggregator.print_summary()
```

### 指定新闻源 / Specify News Sources

```python
# 只获取人民网新闻
news = aggregator.fetch_rss('people', limit=10)

# 只获取新华新闻
news = aggregator.fetch_rss('xinhua', limit=10)

# 只获取澎湃新闻
news = aggregator.fetch_rss('thepaper', limit=10)
```

## 项目结构 / Project Structure

```
news-aggregator/
├── news_aggregator.py        # 主程序 / Main program
├── requirements.txt          # 依赖列表 / Dependencies list
├── news_results.xlsx         # 导出的Excel文件 / Exported Excel file
├── news_results.json         # 导出的JSON文件 / Exported JSON file
└── README.md                 # 项目文档 / Project documentation
```

## 数据格式 / Data Format

导出的数据包含以下字段：

Exported data includes the following fields:

| 字段 / Field | 说明 / Description |
|-------------|-------------------|
| 来源 / Source | 新闻来源网站 / News source website |
| 标题 / Title | 新闻标题 / News title |
| 发布时间 / Publish Time | 新闻发布时间 / News publish time |
| 摘要 / Summary | 新闻内容摘要 / News content summary |
| 链接 / Link | 新闻详情链接 / News detail link |

## 使用场景 / Use Cases

💡 **资讯快速浏览** / Quick news browsing  
一站式获取多个权威新闻源的最新资讯
One-stop access to latest news from multiple authoritative sources

💡 **专题跟踪** / Topic tracking  
通过关键词搜索，跟踪特定主题的新闻动态
Track news dynamics of specific topics through keyword search

💡 **媒体研究** / Media research  
分析不同媒体的内容偏好和发布规律
Analyze content preferences and publishing patterns of different media

💡 **数据归档** / Data archiving  
定期获取新闻数据，建立本地新闻档案
Regularly fetch news data to build local news archive

## 价值点 / Value Points

🎯 **信息全面** / Comprehensive information  
覆盖多个权威新闻源，信息来源广泛
Covers multiple authoritative news sources, extensive information sources

🎯 **节省时间** / Time-saving  
无需逐个访问网站，一键获取所有资讯
No need to visit websites individually, one-click access to all news

🎯 **易于筛选** / Easy filtering  
关键词搜索功能，快速找到感兴趣的内容
Keyword search feature, quickly find content of interest

🎯 **数据友好** / Data-friendly  
结构化数据导出，便于数据分析和挖掘
Structured data export, facilitating data analysis and mining

## 新闻源配置 / News Source Configuration

可以在代码中添加更多新闻源：

You can add more news sources in the code:

```python
self.news_sources = {
    'people': {
        'name': '人民网',
        'url': 'RSS链接',
        'type': 'rss'
    },
    'custom_source': {
        'name': '自定义来源',
        'url': '自定义RSS链接',
        'type': 'rss'
    },
}
```

## 注意事项 / Notes

⚠️ **网络要求** / Network requirements  
需要稳定的网络连接来访问RSS源
Requires stable network connection to access RSS sources

⚠️ **RSS可用性** / RSS availability  
部分网站的RSS链接可能失效，需要定期更新
Some website RSS links may fail, need regular updates

⚠️ **更新频率** / Update frequency  
建议不要过于频繁地请求RSS源，避免给服务器造成压力
Do not request RSS sources too frequently, avoid overloading servers

⚠️ **字符编码** / Character encoding  
注意处理不同网站的字符编码问题
Pay attention to character encoding issues from different websites

## 进阶功能 / Advanced Features

### 数据分析 / Data Analysis

```python
import pandas as pd

# 读取导出的Excel
df = pd.read_excel('news_results.xlsx')

# 统计各来源新闻数量
source_counts = df['来源'].value_counts()
print(source_counts)

# 按时间排序
df['发布时间'] = pd.to_datetime(df['发布时间'])
df_sorted = df.sort_values('发布时间', ascending=False)
```

### 定时任务 / Scheduled Tasks

结合cron或Windows计划任务，可以定期自动获取新闻：

Combine with cron or Windows scheduled tasks to automatically fetch news periodically:

```bash
# Linux/Mac crontab示例
0 */6 * * * cd /path/to/news-aggregator && python news_aggregator.py
```

## 贡献指南 / Contributing

欢迎提交Issue和Pull Request！

Welcome to submit Issues and Pull Requests!

## 许可证 / License

MIT License

## 作者 / Author

AI助手

## 更新日志 / Changelog

### v1.0.0 (2026-03-11)

- 初始版本发布 / Initial release
- 支持人民网、新华网、澎湃新闻 / Supports People's Daily, Xinhua News, The Paper
- 关键词搜索和多格式导出 / Keyword search and multi-format export

---

**觉得有用？给个Star吧！/ Find it useful? Give it a Star!** ⭐
