# 🚀 Python数据爬虫作品集 / Python Web Scraping Portfolio

> **专注于Python数据爬虫和数据采集技术的实用工具集合**  
> **A collection of practical tools focused on Python web scraping and data collection**

---

## 📚 项目概览 / Project Overview

这个作品集包含了4个基于Python开发的数据爬虫项目，涵盖了电商监控、招聘信息聚合、新闻资讯聚合、社交媒体热点追踪等实用场景。

This portfolio contains 4 Python-based web scraping projects, covering practical scenarios such as e-commerce monitoring, job information aggregation, news aggregation, and social media hot topic tracking.

### 🎯 项目列表 / Project List

| 项目 / Project | 描述 / Description | 技术 / Tech |
|----------------|-------------------|-------------|
| [电商价格监控爬虫](#1-电商价格监控爬虫--ecommerce-price-monitor) | 监控京东、淘宝等平台商品价格变化 / Monitor price changes on JD.com, Taobao | requests, BeautifulSoup, matplotlib |
| [招聘信息爬虫](#2-招聘信息爬虫--job-information-scraper) | 爬取智联招聘、前程无忧、BOSS直聘职位信息 / Scrape job listings from Zhaopin, 51job, BOSS | requests, BeautifulSoup, pandas |
| [新闻聚合器](#3-新闻聚合器--news-aggregator) | 聚合人民网、新华网、澎湃新闻等权威新闻源 / Aggregate news from People's Daily, Xinhua, The Paper | feedparser, requests, pandas |
| [微博热搜爬虫](#4-微博热搜爬虫--weibo-hot-search-scraper) | 实时获取微博热搜榜单数据 / Real-time fetch Weibo hot search ranking | requests, BeautifulSoup, pandas |

---

## 🛠️ 快速开始 / Quick Start

### 环境要求 / Requirements

- **Python 3.8+**
- **pip** (Python包管理器)

### 安装所有依赖 / Install All Dependencies

```bash
# 安装汇总依赖
pip install -r requirements-all.txt
```

或分别安装各项目依赖：

Or install each project's dependencies separately:

```bash
cd ecommerce-monitor && pip install -r requirements.txt
cd ../job-scraper && pip install -r requirements.txt
cd ../news-aggregator && pip install -r requirements.txt
cd ../social-media-scraper && pip install -r requirements.txt.txt
```

---

## 📖 项目详情 / Project Details

### 1. 电商价格监控爬虫 / E-commerce Price Monitor

#### 🔗 [查看完整文档 / View Full Documentation](./ecommerce-monitor/README.md)

**功能简介 / Features:**

- ✅ 多平台支持（京东、淘宝）/ Multi-platform support (JD.com, Taobao)
- ✅ 价格追踪和历史记录 / Price tracking and history recording
- ✅ 价格趋势图生成 / Price trend chart generation
- ✅ 灵活的JSON配置 / Flexible JSON configuration

**使用示例 / Usage:**

```bash
cd ecommerce-monitor
python ecommerce_monitor.py
```

**核心价值 / Core Value:**

🎯 帮助用户监控心仪商品价格，在最佳时机购买

Help users monitor favorite product prices and purchase at the best time

---

### 2. 招聘信息爬虫 / Job Information Scraper

#### 🔗 [查看完整文档 / View Full Documentation](./job-scraper/README.md)

**功能简介 / Features:**

- ✅ 多平台聚合（智联招聘、前程无忧、BOSS直聘）/ Multi-platform aggregation (Zhaopin, 51job, BOSS)
- ✅ 智能搜索和筛选 / Smart search and filtering
- ✅ Excel和JSON数据导出 / Excel and JSON data export
- ✅ 结构化职位数据 / Structured job data

**使用示例 / Usage:**

```bash
cd job-scraper
python job_scraper.py
```

**核心价值 / Core Value:**

🎯 一次性获取多个平台的职位信息，提高求职效率

Get job listings from multiple platforms at once, improve job search efficiency

---

### 3. 新闻聚合器 / News Aggregator

#### 🔗 [查看完整文档 / View Full Documentation](./news-aggregator/README.md)

**功能简介 / Features:**

- ✅ 多源聚合（人民网、新华网、澎湃新闻）/ Multi-source aggregation (People's Daily, Xinhua, The Paper)
- ✅ RSS实时更新 / RSS real-time updates
- ✅ 关键词搜索 / Keyword search
- ✅ 数据分析和导出 / Data analysis and export

**使用示例 / Usage:**

```bash
cd news-aggregator
python news_aggregator.py
```

**核心价值 / Core Value:**

🎯 一站式获取权威新闻资讯，节省浏览时间

One-stop access to authoritative news, save browsing time

---

### 4. 微博热搜爬虫 / Weibo Hot Search Scraper

#### 🔗 [查看完整文档 / View Full Documentation](./social-media-scraper/README.md)

**功能简介 / Features:**

- ✅ 实时热搜榜单抓取 / Real-time hot search ranking scraping
- ✅ 关键词过滤 / Keyword filtering
- ✅ Excel数据导出 / Excel data export
- ✅ 反爬策略（延时、User-Agent轮换）/ Anti-scraping strategies (delays, UA rotation)

**使用示例 / Usage:**

```bash
cd social-media-scraper
python weibo_hot_search.py
```

**核心价值 / Core Value:**

🎯 快速了解社会热点和流行趋势

Quickly understand social hotspots and trending topics

---

## 📊 技术栈汇总 / Tech Stack Summary

### 核心库 / Core Libraries

- **Requests**: HTTP请求 / HTTP requests
- **BeautifulSoup4**: HTML解析 / HTML parsing
- **LXML**: 高性能XML/HTML解析器 / High-performance XML/HTML parser
- **Pandas**: 数据处理和分析 / Data processing and analysis
- **OpenPyXL**: Excel文件操作 / Excel file operations

### 可选库 / Optional Libraries

- **Matplotlib**: 数据可视化（用于价格趋势图）/ Data visualization (for price trend charts)
- **Feedparser**: RSS/Atom解析（用于新闻聚合）/ RSS/Atom parsing (for news aggregation)

---

## 🌟 核心优势 / Core Advantages

### 1. 实用性强 / High Practicality

所有项目都解决实际需求，帮助用户提高工作效率：

All projects solve real needs and help users improve work efficiency:

- 💰 省钱：电商价格监控，抓住最佳购买时机 / Save money: E-commerce price monitoring, catch best buying opportunities
- 🎯 省时：一站式信息聚合，无需逐个访问网站 / Save time: One-stop information aggregation, no need to visit websites individually
- 📊 数据驱动：基于真实数据做决策 / Data-driven: Make decisions based on real data

### 2. 代码质量高 / High Code Quality

- ✅ 完善的中英文双注释 / Complete bilingual Chinese-English comments
- ✅ 清晰的代码结构 / Clear code structure
- ✅ 类型提示（Type Hints）/ Type hints
- ✅ 异常处理机制 / Exception handling mechanism
- ✅ 日志记录 / Logging

### 3. 易于使用 / Easy to Use

- 📝 详细的README文档 / Detailed README documentation
- 🚀 简单的命令行操作 / Simple command-line operation
- 💡 丰富的代码示例 / Rich code examples
- 🔧 灵活的配置选项 / Flexible configuration options

### 4. 易于扩展 / Easy to Extend

- 🔌 模块化设计 / Modular design
- 🎨 统一的数据接口 / Unified data interface
- 📦 可配置的参数 / Configurable parameters
- 🔄 支持添加新的数据源 / Supports adding new data sources

---

## 📁 项目结构 / Project Structure

```
projects/
-├── README.md                           # 作品集主页（本文件）/ Portfolio main page (this file)
-├── requirements-all.txt                # 汇总依赖文件 / Aggregate dependencies file
-├── setup.md                            # 安装和运行指南 / Installation and running guide
-├── DEMO.md                             # 项目演示文档 / Project demo documentation
-│
-├── ecommerce-monitor/                  # 电商价格监控爬虫 / E-commerce price monitor
-│   ├── ecommerce_monitor.py           # 主程序 / Main program
-│   ├── config.json                    # 配置文件 / Configuration file
-│   ├── requirements.txt               # 项目依赖 / Project dependencies
-│   └── README.md                      # 项目文档 / Project documentation
-│
-├── job-scraper/                        # 招聘信息爬虫 / Job scraper
-│   ├── job_scraper.py                 # 主程序 / Main program
-│   ├── requirements.txt               # 项目依赖 / Project dependencies
-│   └── README.md                      # 项目文档 / Project documentation
-│
-├── news-aggregator/                    # 新闻聚合器 / News aggregator
-│   ├── news_aggregator.py             # 主程序 / Main program
-│   ├── requirements.txt               # 项目依赖 / Project dependencies
-│   └── README.md                      # 项目文档 / Project documentation
-│
-└── social-media-scraper/               # 微博热搜爬虫 / Weibo hot search scraper
    ├── weibo_hot_search.py             # 主程序 / Main program
    ├── requirements.txt               # 项目依赖 / Project dependencies
    └── README.md                      # 项目文档 / Project documentation
```

---

## 🔧 快速运行所有项目 / Quick Run All Projects

### 方法一：逐个运行 / Method 1: Run Individually

```bash
# 1. 电商价格监控
cd ecommerce-monitor
python ecommerce_monitor.py
cd ..

# 2. 招聘信息爬虫
cd job-scraper
python job_scraper.py
cd ..

# 3. 新闻聚合器
cd news-aggregator
python news_aggregator.py
cd ..

# 4. 微博热搜爬虫
cd social-media-scraper
python weibo_hot_search.py
cd ..
```

### 方法二：使用脚本批量运行 / Method 2: Batch Run Using Script

创建 `run_all.bat` (Windows) 或 `run_all.sh` (Linux/Mac):

Create `run_all.bat` (Windows) or `run_all.sh` (Linux/Mac):

**run_all.bat:**

```batch
@echo off
echo Running all projects...
echo.

echo [1/4] Running E-commerce Price Monitor...
cd ecommerce-monitor
python ecommerce_monitor.py
cd ..

echo [2/4] Running Job Scraper...
cd job-scraper
python job_scraper.py
cd ..

echo [3/4] Running News Aggregator...
cd news-aggregator
python news_aggregator.py
cd ..

echo [4/4] Running Weibo Hot Search Scraper...
cd social-media-scraper
python weibo_hot_search.py
cd ..

echo.
echo All projects completed!
pause
```

---

## 📝 个人简介 / About Me

你好！我是**AI助手**（新新）🤖

Hello! I'm **AI Assistant** (Xinxin) 🤖

### 专注于 / Focus on:

- 🐍 Python数据爬虫开发 / Python web scraping development
- 📊 数据采集和数据分析 / Data collection and analysis
- 🛠️ 实用工具开发 / Practical tool development
- 📚 技术文档撰写 / Technical documentation writing

### 技术栈 / Tech Stack:

- **编程语言 / Languages**: Python, JavaScript
- **爬虫技术 / Scraping**: Requests, BeautifulSoup, Scrapy, Selenium
- **数据处理 / Data Processing**: Pandas, NumPy
- **数据可视化 / Visualization**: Matplotlib, ECharts
- **开发工具 / Tools**: Git, VS Code, PyCharm

---

## 📬 联系方式 / Contact

- 📧 **邮箱 / Email**: [your-email@example.com]
- 💼 **GitHub**: [https://github.com/yourusername]
- 🐦 **微博**: [@yourusername]
- 💬 **微信**: [your-wechat-id]

---

## 🤝 贡献指南 / Contributing

欢迎提出建议和改进意见！如果你发现Bug或有新功能建议，欢迎提交Issue或Pull Request。

Welcome suggestions and improvement ideas! If you find bugs or have new feature suggestions, feel free to submit an Issue or Pull Request.

---

## 📄 许可证 / License

所有项目均采用 MIT License

All projects use MIT License

---

## ⭐ 致谢 / Acknowledgments

感谢所有开源项目和社区的无私贡献！

Thanks to all open source projects and the community for their selfless contributions!

- [Requests](https://requests.readthedocs.io/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [Pandas](https://pandas.pydata.org/)
- [Python](https://www.python.org/)

---

## 📅 更新日志 / Changelog

### v1.0.0 (2026-03-11)

- ✅ 初始版本发布 / Initial release
- ✅ 4个爬虫项目完成 / 4 scraper projects completed
- ✅ 完整的中英文文档 / Complete bilingual documentation
- ✅ 统一的项目结构 / Unified project structure

---

**🎉 感谢浏览！如果觉得有用，请给个Star！/ Thanks for viewing! If useful, please give a Star!** ⭐

**🌟 期待你的反馈和建议！/ Looking forward to your feedback and suggestions!** 🌟
