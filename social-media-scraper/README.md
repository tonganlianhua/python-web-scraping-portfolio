#微博热搜爬虫 / Weibo Hotserch Scraper

## 项目简介 / Project Introduction

这是一个高效的微博热搜榜单爬虫，可以实时获取微博平台的热搜话题，支持关键词搜索、数据导出等功能，帮助你快速了解社会热点和流行趋势。

An efficient Weibo hot search ranking scraper that can real-time fetch trending topics from Weibo platform, with features like keyword search and data export, helping you quickly understand social hotspots and trending topics.

## 功能特性 / Features

✅ **实时抓取** / Real-time scraping  
实时获取微博热搜榜单数据
Real-time fetch Weibo hot search ranking data

✅ **关键词搜索** / Keyword search  
支持通过关键词过滤热搜话题
Support filtering hot search topics through keywords

✅ **数据导出** / Data export  
支持Excel格式导出，便于数据分析和存档
Supports Excel format export for easy data analysis and archiving

✅ **结构化数据** / Structured data  
提供排名、标题、热度值、链接等完整信息
Provides complete information including ranking, title, heat value, link

✅ **反爬策略** / Anti-scraping strategies  
内置随机延时和User-Agent轮换，提高稳定性
Built-in random delays and User-Agent rotation for improved stability

## 技术栈 / Tech Stack

- **Python 3.8+**: 主要开发语言 / Main development language
- **Requests**: HTTP请求库 / HTTP request library
- **BeautifulSoup4**: HTML解析 / HTML parsing
- **LXML**: HTML解析器 / HTML parser
- **Pandas**: 数据处理和导出 / Data processing and export
- **OpenPyXL**: Excel文件读写 / Excel file read/write

## 安装说明 / Installation

### 1. 克隆项目 / Clone Project

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo/projects/social-media-scraper
```

### 2. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

或逐个安装 / Or install individually:

```bash
pip install requests beautifulsoup4 lxml pandas openpyxl
```

## 使用方法 / Usage

### 基本使用 / Basic Usage

```bash
python weibo_hot_search.py
```

按照提示选择是否输入关键词进行筛选。

Follow the prompts to choose whether to enter keywords for filtering.

### 代码示例 / Code Example

```python
from weibo_hot_search import WeiboHotSearchScraper

# 创建爬虫实例
scraper = WeiboHotSearchScraper(delay_range=(1, 2))

# 获取热搜数据
hot_data = scraper.fetch_hot_search()

# 关键词过滤
filtered_data = scraper.filter_by_keyword(hot_data, '科技')

# 导出为Excel
scraper.export_to_excel(filtered_data, 'weibo_hot_search.xlsx')
```

### 调整延时参数 / Adjust Delay Parameters

```python
# 增加延时，更稳定
scraper = WeiboHotSearchScraper(delay_range=(2, 5))

# 减少延时，更快获取
scraper = WeiboHotSearchScraper(delay_range=(0.5, 1))
```

## 项目结构 / Project Structure

```
social-media-scraper/
├── weibo_hot_search.py      # 主程序 / Main program
├── requirements.txt         # 依赖列表 / Dependencies list
├── weibo_hot_search.xlsx    # 导出的Excel文件 / Exported Excel file
└── README.md                # 项目文档 / Project documentation
```

## 数据格式 / Data Format

导出的数据包含以下字段：

Exported data includes the following fields:

| 字段 / Field | 说明 / Description |
|-------------|-------------------|
| 排名 / Ranking | 热搜排名 / Hot search ranking |
| 标题 / Title | 热搜话题标题 / Hot search topic title |
| 热度值 / Heat Value | 话题热度 / Topic heat value |
| 链接 / Link | 话题详情链接 / Topic detail link |

## 使用场景 / Use Cases

💡 **热点追踪** / Hot topics tracking  
实时了解社会热点和流行趋势
Real-time understanding of social hotspots and trending topics

💡 **舆情监控** / Public opinion monitoring  
关注特定话题或关键词的热度变化
Monitor heat value changes of specific topics or keywords

💡 **内容创作** / Content creation  
获取热点话题灵感，辅助内容创作
Get hot topic inspiration, assist with content creation

💡 **数据分析** / Data analysis  
收集热搜数据，进行趋势分析和研究
Collect hot search data for trend analysis and research

## 价值点 / Value Points

🎯 **实时性强** / Strong real-time capability  
获取最新的热搜数据，信息更新及时
Fetch the latest hot search data, timely information updates

🎯 **易于使用** / Easy to use  
简单的命令行操作，无需复杂配置
Simple command-line operation, no complex configuration needed

🎯 **数据完整** / Complete data  
提供排名、热度、链接等完整信息
Provides complete information including ranking, heat value, link

🎯 **灵活筛选** / Flexible filtering  
支持关键词搜索，快速定位感兴趣的话题
Supports keyword search, quickly locate topics of interest

## 核心功能说明 / Core Features

### 获取热搜数据 / Fetch Hot Search Data

```python
scraper = WeiboHotSearchScraper()
hot_data = scraper.fetch_hot_search()

# 打印前10条热搜
for item in hot_data[:10]:
    print(f"{item['排名']}. {item['标题']} (热度: {item['热度值']})")
```

### 关键词过滤 / Keyword Filtering

```python
# 搜索包含"科技"的热搜
tech_topics = scraper.filter_by_keyword(hot_data, '科技')

# 搜索包含"教育"的热搜
edu_topics = scraper.filter_by_keyword(hot_data, '教育')
```

### 数据导出 / Data Export

```python
# 导出为Excel
scraper.export_to_excel(hot_data, 'all_hot_search.xlsx')

# 导出过滤后的数据
scraper.export_to_excel(filtered_data, 'filtered_hot_search.xlsx')
```

## 注意事项 / Notes

⚠️ **网络要求** / Network requirements  
需要稳定的网络连接访问微博网站
Requires stable network connection to access Weibo website

⚠️ **网页结构变化** / Page structure changes  
微博可能更新页面结构，需要定期维护解析逻辑
Weibo may update page structure, maintain parsing logic regularly

⚠️ **访问频率** / Access frequency  
建议不要过于频繁地请求，避免被限制访问
Do not request too frequently, avoid being restricted

⚠️ **合法合规** / Legal compliance  
请遵守微博的使用条款，合理使用爬虫技术
Please comply with Weibo terms of use, use web scraping technology reasonably

## 进阶功能 / Advanced Features

### 数据分析 / Data Analysis

```python
import pandas as pd

# 读取导出的Excel
df = pd.read_excel('weibo_hot_search.xlsx')

# 统计热度分布
print(df['热度值'].describe())

# 查找前5名热搜
top5 = df.head(5)
print(top5[['排名', '标题', '热度值']])
```

### 定时监控 / Scheduled Monitoring

结合cron或Windows计划任务，可以定期自动获取热搜：

Combine with cron or Windows scheduled tasks to automatically fetch hot search periodically:

```bash
# Linux/Mac crontab示例
*/30 * * * * cd /path/to/social-media-scraper && python weibo_hot_search.py
```

### 热度对比 / Heat Value Comparison

```python
# 保存历史数据进行对比分析
# 识别热度快速上升或下降的话题
history = load_previous_data()
current = fetch_current_data()

# 计算热度变化
for curr_item in current:
    for hist_item in history:
        if curr_item['标题'] == hist_item['标题']:
            curr_heat = parse_heat(curr_item['热度值'])
            hist_heat = parse_heat(hist_item['热度值'])
            change = curr_heat - hist_heat
            print(f"{curr_item['标题']}: 热度变化 {change}")
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
- 支持微博热搜榜单爬取 / Supports Weibo hot search ranking scraping
- 关键词搜索和Excel导出 / Keyword search and Excel export

---

**觉得有用？给个Star吧！/ Find it useful? Give it a Star!** ⭐
