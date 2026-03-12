# 项目演示文档 / Project Demo Documentation

> **本文档提供了所有项目的演示说明和使用示例**  
> **This document provides demo instructions and usage examples for all projects**

---

## 📋 目录 / Table of Contents

- [演示准备](#演示准备--demo-preparation)
- [项目1：电商价格监控爬虫演示](#项目1电商价格监控爬虫演示--demo-1-ecommerce-price-monitor)
- [项目2：招聘信息爬虫演示](#项目2招聘信息爬虫演示--demo-2-job-scraper)
- [项目3：新闻聚合器演示](#项目3新闻聚合器演示--demo-3-news-aggregator)
- [项目4：微博热搜爬虫演示](#项目4微博热搜爬虫演示--demo-4-weibo-hot-search-scraper)
- [常见问题](#常见问题--faq)

---

## 🎬 演示准备 / Demo Preparation

### 环境要求 / Requirements

确保已安装Python 3.8+和所有依赖：

Ensure Python 3.8+ and all dependencies are installed:

```bash
# 检查Python版本
python --version

# 安装所有依赖
pip install -r requirements-all.txt
```

### 目录结构 / Directory Structure

确保项目目录结构完整：

Ensure complete project directory structure:

```
projects/
├── ecommerce-monitor/
├── job-scraper/
├── news-aggregator/
└── social-media-scraper/
```

---

## 🎬 项目1：电商价格监控爬虫演示 / Demo 1: E-commerce Price Monitor

### 演示目标 / Demo Goal

监控京东商品价格变化，生成价格趋势图。

Monitor JD.com product price changes and generate price trend charts.

### 演示步骤 / Demo Steps

#### 步骤1：查看配置文件 / Step 1: View Configuration File

```bash
cd ecommerce-monitor
cat config.json
```

**配置示例 / Configuration Example:**

```json
{
  "products": [
    {
      "name": "京东测试商品",
      "platform": "jd",
      "url": "https://item.jd.com/100012047978.html",
      "selector": ".price .p-price .price",
      "enabled": true
    }
  ],
  "settings": {
    "check_interval": 300,
    "log_file": "price_history.log",
    "history_file": "price_history.json"
  }
}
```

#### 步骤2：运行监控程序 / Step 2: Run Monitor Program

```bash
python ecommerce_monitor.py
```

**预期输出 / Expected Output:**

```
============================================================
电商价格监控爬虫 / E-commerce Price Monitor
============================================================

开始检查 1 个商品价格...
==================================================

[1/1] 检查商品: 京东测试商品
INFO: 获取京东价格: https://item.jd.com/100012047978.html
INFO: 京东价格: ¥1234.56
✅ 当前价格: ¥1234.56

INFO: 保存历史数据: 1 条记录

=== 价格统计摘要 / Price Statistics Summary ===

京东测试商品 (jd):
  记录数: 1
  最低价: ¥1234.56
  最高价: ¥1234.56
  平均价: ¥1234.56
========================================
```

#### 步骤3：查看历史数据 / Step 3: View Historical Data

```bash
cat price_history.json
```

#### 步骤4：生成价格趋势图 / Step 4: Generate Price Trend Chart

在程序运行时选择"y"生成图表：

Choose "y" to generate chart when prompted:

```
是否生成 "京东测试商品" 价格趋势图？(y/n): y
INFO: 保存历史数据: 1 条记录
✅ 价格趋势图已保存: 京东测试商品_price_trend.png
```

### 演示代码 / Demo Code

```python
from ecommerce_monitor import EcommerceMonitor

# 创建监控实例
monitor = EcommerceMonitor('config.json')

# 检查价格
records = monitor.check_all_products()

# 打印统计
monitor.print_summary()

# 生成价格趋势图
monitor.generate_price_chart('京东测试商品', 'demo_chart.png')
```

---

## 🎬 项目2：招聘信息爬虫演示 / Demo 2: Job Scraper

### 演示目标 / Demo Goal

爬取智联招聘和BOSS直聘的Python工程师职位信息。

Scrape Python engineer job listings from Zhaopin and BOSS Zhipin.

### 演示步骤 / Demo Steps

#### 步骤1：运行爬虫程序 / Step 1: Run Scraper Program

```bash
cd job-scraper
python job_scraper.py
```

**输入提示 / Input Prompts:**

```
============================================================
招聘信息爬虫 / Job Information Scraper
============================================================

请输入职位关键词 / Enter job keyword: Python工程师

请选择平台（多选用逗号分隔，留空则选择全部）:
Please select platforms (comma-separated, leave empty for all):
1. zhaopin (智联招聘)
2. qiancheng (前程无忧)
3. boss (BOSS直聘)
选择 / Select: zhaopin,boss
```

**预期输出 / Expected Output:**

```
开始爬取 "Python工程师" 相关职位...

=== 数据预览 / Data Preview ===
平台        职位名称            公司名称  薪资范围  城市  经验要求  学历要求  发布时间      职位链接
智联招聘    Python工程师     示例公司1  15K-25K   北京  3-5年    本科      2026-03-11  https://...
智联招聘    Python工程师     示例公司2  15K-25K   北京  3-5年    本科      2026-03-11  https://...
BOSS直聘    Python高级工程师 互联网公司1 25K-40K   深圳  5年以上  本科及以上 2026-03-11  https://...

✅ 成功获取 6 条职位信息
✅ Excel文件: job_results_20260311_225500.xlsx
✅ JSON文件: job_results_20260311_225500.json
```

#### 步骤2：查看导出文件 / Step 2: View Exported Files

```bash
# 查看Excel文件
ls -lh job_results_*.xlsx

# 查看JSON文件
cat job_results_*.json | head -20
```

### 演示代码 / Demo Code

```python
from job_scraper import JobScraper

# 创建爬虫实例
scraper = JobScraper()

# 爬取指定平台
jobs = scraper.scrape_all('Python工程师', ['zhaopin', 'boss'])

# 打印前3条
print('=== 前3条职位信息 ===')
for job in jobs[:3]:
    print(f"{job['职位名称']} - {job['公司名称']} - {job['薪资范围']}")

# 导出文件
scraper.export_to_excel('demo_jobs.xlsx')
scraper.export_to_json('demo_jobs.json')
```

---

## 🎬 项目3：新闻聚合器演示 / Demo 3: News Aggregator

### 演示目标 / Demo Goal

获取人民网、新华网、澎湃新闻的最新资讯，并进行关键词搜索。

Fetch latest news from People's Daily, Xinhua News, and The Paper, and perform keyword search.

### 演示步骤 / Demo Steps

#### 步骤1：运行聚合器程序 / Step 1: Run Aggregator Program

```bash
cd news-aggregator
python news_aggregator.py
```

**输入提示 / Input Prompts:**

```
============================================================
新闻聚合器 / News Aggregator
============================================================

开始获取新闻...
INFO: 开始获取 人民网 新闻 / Fetching news from People's Daily
INFO: 获取新闻: 某新闻标题...
INFO: 人民网 获取完成: 20 条

INFO: 开始获取 新华网 新闻 / Fetching news from Xinhua News
INFO: 获取新闻: 某新闻标题...
INFO: 新华网 获取完成: 20 条
```

**输入关键词搜索 / Keyword Search Input:**

```
请输入搜索关键词（留空则搜索全部）/ Enter keyword (empty for all): 经济
```

**预期输出 / Expected Output:**

```
=== 新闻统计 / News Statistics ===
总新闻数 / Total news: 60
来源分布 / Source distribution:
  - 人民网: 20 条
  - 新华网: 20 条
  - 澎湃新闻: 20 条
========================================

✅ 关键词过滤后剩余 15 条新闻

=== 数据预览 / Data Preview ===
来源     标题                         发布时间              摘要
新华网   中国经济持续高质量发展...   2026-03-11 10:30:00  据报道，中国经济...
人民网   经济发展新动能持续增强...   2026-03-11 10:25:00  分析认为，新动能...

✅ Excel文件: news_results_20260311_225500.xlsx
✅ JSON文件: news_results_20260311_225500.json
```

### 演示代码 / Demo Code

```python
from news_aggregator import NewsAggregator

# 创建聚合器实例
aggregator = NewsAggregator()

# 获取所有新闻
news_list = aggregator.fetch_all(limit=10)

# 打印统计
aggregator.print_summary()

# 关键词搜索
filtered = aggregator.filter_by_keyword('科技')
print(f"\n找到 {len(filtered)} 条科技相关新闻")

# 导出文件
aggregator.export_to_excel('demo_news.xlsx', filtered)
```

---

## 🎬 项目4：微博热搜爬虫演示 / Demo 4: Weibo Hot Search Scraper

### 演示目标 / Demo Goal

实时获取微博热搜榜单，并进行关键词过滤。

Real-time fetch Weibo hot search ranking and perform keyword filtering.

### 演示步骤 / Demo Steps

#### 步骤1：运行爬虫程序 / Step 1: Run Scraper Program

```bash
cd social-media-scraper
python weibo_hot_search.py
```

**预期输出 / Expected Output:**

```
============================================================
微博热搜爬虫 / Weibo Hot Search Scraper
============================================================

[1/3] 正在获取微博热搜数据...
INFO: 正在获取微博热搜: https://s.weibo.com/top/summary
INFO: 获取到热搜: 1. 某热搜话题 (热度: 1234567)
INFO: 获取到热搜: 2. 另一个热搜话题 (热度: 987654)
...

✅ 成功获取 50 条热话题
```

**输入关键词搜索 / Keyword Search Input:**

```
[2/3] 输入搜索关键词（留空则搜索全部）: 科技
```

**预期输出 / Expected Output:**

```
✅ 关键词 "科技" 过滤后，剩余 8 条数据
✅ 使用全部 8 条数据

[3/3] 导出Excel文件...
INFO: 成功导出 8 条数据到 weibo_hot_search_20260311_225500.xlsx

=== 数据预览 ===
排名  标题                     热度值     链接
1     科技创新大会召开         1234567  https://s.weibo.com/weibo?q=...
5     新科技产品发布           987654   https://s.weibo.com/weibo?q=...

✅ 完成！文件已保存为: weibo_hot_search_20260311_225500.xlsx
```

#### 步骤2：查看导出文件 / Step 2: View Exported Files

```bash
# 查看Excel文件
ls -lh weibo_hot_search_*.xlsx
```

### 演示代码 / Demo Code

```python
from weibo_hot_search import WeiboHotSearchScraper

# 创建爬虫实例
scraper = WeiboHotSearchScraper(delay_range=(1, 2))

# 获取热搜数据
hot_data = scraper.fetch_hot_search()

# 打印前10条
print('=== 微博热搜 Top 10 ===')
for item in hot_data[:10]:
    print(f"{item['排名']}. {item['标题']} (热度: {item['热度值']})")

# 关键词过滤
filtered = scraper.filter_by_keyword(hot_data, '科技')
print(f"\n找到 {len(filtered)} 条科技相关热搜")

# 导出文件
scraper.export_to_excel(filtered, 'demo_weibo_hot.xlsx')
```

---

## 🤔 常见问题 / FAQ

### Q1: 爬虫运行失败，提示网络错误？

**A:** 检查网络连接，确保可以访问目标网站。某些网站可能需要设置代理。

Check network connection and ensure access to target websites. Some sites may require proxy configuration.

### Q2: 导出的Excel文件乱码？

**A:** 确保使用UTF-8编码打开Excel文件，或使用支持中文的Excel版本。

Ensure opening Excel files with UTF-8 encoding or use Excel version that supports Chinese.

### Q3: 价格监控没有生成图表？

**A:** 确保安装了matplotlib库：`pip install matplotlib`

Ensure matplotlib library is installed: `pip install matplotlib`

### Q4: 新闻聚合器获取不到数据？

**A:** 检查RSS源是否可用，某些RSS链接可能需要更新。

Check if RSS sources are available, some RSS links may need updating.

### Q5: 如何设置定时运行？

**A:** 使用cron（Linux/Mac）或任务计划程序（Windows）：

Use cron (Linux/Mac) or Task Scheduler (Windows):

```bash
# Linux/Mac crontab示例
0 */6 * * * cd /path/to/project && python script.py
```

### Q6: 如何修改反爬延时参数？

**A:** 在创建爬虫实例时传入delay_range参数：

Pass delay_range parameter when creating scraper instance:

```python
scraper = WeiboHotSearchScraper(delay_range=(2, 5))
```

### Q7: 数据如何进行二次分析？

**A:** 使用pandas读取导出的Excel或JSON文件：

Use pandas to read exported Excel or JSON files:

```python
import pandas as pd

df = pd.read_excel('results.xlsx')

# 进行数据分析
print(df.describe())
print(df['某列'].value_counts())
```

### Q8: 如何添加新的数据源？

**A:** 参考现有代码结构，在对应项目的源配置中添加新的URL。

Refer to existing code structure and add new URL in source configuration.

---

## 📞 演示支持 / Demo Support

如有问题或建议，欢迎联系：

For questions or suggestions, feel free to contact:

- 📧 邮箱 / Email: [your-email@example.com]
- 💼 GitHub: [https://github.com/yourusername/issues]

---

## 📚 更多资源 / More Resources

- [主README文档](./README.md)
- [安装和运行指南](./setup.md)
- [项目详细文档](./ecommerce-monitor/README.md)
- [项目详细文档](./job-scraper/README.md)
- [项目详细文档](./news-aggregator/README.md)
- [项目详细文档](./social-media-scraper/README.md)

---

**🎉 祝演示顺利！/ Good luck with the demo!** 🎉
