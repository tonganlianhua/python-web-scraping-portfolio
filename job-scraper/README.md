# 招聘信息爬虫 / Job Information Scraper

## 项目简介 / Project Introduction

这是一个强大的招聘信息聚合工具，可以自动爬取智联招聘、前程无忧、BOSS直聘等主流招聘平台的职位信息，帮助求职者快速了解市场行情和机会。

A powerful job information aggregation tool that automatically scrapes job listings from major recruitment platforms like Zhaopin, 51job, and BOSS Zhipin, helping job seekers quickly understand market trends and opportunities.

## 功能特性 / Features

✅ **多平台聚合** / Multi-platform aggregation  
支持智联招聘、前程无忧、BOSS直聘等多个平台
Supports multiple platforms including Zhaopin, 51job, and BOSS Zhipin

✅ **智能搜索** / Smart search  
根据关键词、城市、薪资等条件筛选职位
Filter jobs by keywords, location, salary, and other criteria

✅ **数据导出** / Data export  
支持Excel和JSON格式导出，方便数据分析
Export to Excel and JSON formats for easy data analysis

✅ **结构化数据** / Structured data  
统一的数据格式，包含职位、公司、薪资、要求等信息
Unified data format including job title, company, salary, requirements, etc.

✅ **批量处理** / Batch processing  
一键爬取多个平台的数据，提高效率
One-click scraping across multiple platforms for improved efficiency

## 技术栈 / Tech Stack

- **Python 3.8+**: 主要开发语言 / Main development language
- **Requests**: HTTP请求库 / HTTP request library
- **BeautifulSoup4**: HTML解析 / HTML parsing
- **Pandas**: 数据处理和导出 / Data processing and export
- **OpenPyXL**: Excel文件读写 / Excel file read/write
- **JSON**: 数据存储格式 / Data storage format

## 安装说明 / Installation

### 1. 克隆项目 / Clone Project

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo/projects/job-scraper
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
python job_scraper.py
```

按照提示输入关键词和选择平台即可。

Follow the prompts to enter keywords and select platforms.

### 代码示例 / Code Example

```python
from job_scraper import JobScraper

# 创建爬虫实例
scraper = JobScraper()

# 爬取指定关键词的职位
jobs = scraper.scrape_all('Python工程师', ['zhaopin', 'boss'])

# 导出为Excel
scraper.export_to_excel('python_jobs.xlsx')

# 导出为JSON
scraper.export_to_json('python_jobs.json')
```

### 指定平台爬取 / Scrape Specific Platforms

```python
# 只爬取智联招聘
jobs = scraper.scrape_zhaopin('Java开发', city='北京', pages=5)

# 只爬取BOSS直聘
jobs = scraper.scrape_boss('产品经理', city='上海', pages=3)
```

## 项目结构 / Project Structure

```
job-scraper/
├── job_scraper.py            # 主程序 / Main program
├── requirements.txt          # 依赖列表 / Dependencies list
├── job_results.xlsx          # 导出的Excel文件 / Exported Excel file
├── job_results.json          # 导出的JSON文件 / Exported JSON file
└── README.md                 # 项目文档 / Project documentation
```

## 数据格式 / Data Format

导出的数据包含以下字段：

Exported data includes the following fields:

| 字段 / Field | 说明 / Description |
|-------------|-------------------|
| 平台 / Platform | 招聘平台名称 / Recruitment platform name |
| 职位名称 / Job Title | 职位名称 / Job title |
| 公司名称 / Company Name | 公司名称 / Company name |
| 薪资范围 / Salary Range | 薪资范围 / Salary range |
| 城市 / City | 工作城市 / Job location |
| 经验要求 / Experience | 经验要求 / Experience requirement |
| 学历要求 / Education | 学历要求 / Education requirement |
| 发布时间 / Publish Time | 职位发布时间 / Job publish time |
| 职位链接 / Job Link | 职位详情链接 / Job detail link |

## 使用场景 / Use Cases

💡 **求职分析** / Job search analysis  
分析目标职位的薪资分布、公司类型分布
Analyze salary distribution and company type distribution for target positions

💡 **市场调研** / Market research  
了解行业人才需求和市场趋势
Understand industry talent demand and market trends

💡 **薪资对比** / Salary comparison  
对比不同平台、不同城市的薪资水平
Compare salary levels across different platforms and cities

💡 **快速筛选** / Quick filtering  
批量获取职位信息，快速筛选心仪岗位
Batch retrieve job information and quickly filter preferred positions

## 价值点 / Value Points

🎯 **高效便捷** / Efficient and convenient  
一次性获取多个平台数据，节省大量时间
Retrieve data from multiple platforms at once, saving significant time

🎯 **信息聚合** / Information aggregation  
打破平台壁垒，统一查看职位信息
Break platform barriers and view job information in one place

🎯 **数据驱动** / Data-driven决策  
基于真实数据进行求职决策，提高成功率
Make job search decisions based on real data for higher success rate

🎯 **易于分析** / Easy to analyze  
Excel格式便于进行二次分析和可视化
Excel format facilitates secondary analysis and visualization

## 注意事项 / Notes

⚠️ **反爬策略** / Anti-scraping strategies  
程序内置了随机延时和User-Agent轮换，建议合理控制爬取频率
The program includes random delays and User-Agent rotation, control scraping frequency reasonably

⚠️ **网站结构变化** / Website structure changes  
招聘网站可能更新页面结构，需要定期维护解析逻辑
Recruitment sites may update page structure, maintain parsing logic regularly

⚠️ **使用频率** / Usage frequency  
请遵守网站的使用条款，不要过度频繁请求
Please comply with website terms of use, avoid excessive frequent requests

⚠️ **数据准确性** / Data accuracy  
部分数据为模拟数据，实际使用时需要根据真实网站调整
Some data is simulated, adjust based on real websites when in use

## 进阶功能 / Advanced Features

### 数据筛选 / Data Filtering

```python
# 爬取所有数据
jobs = scraper.scrape_all('Python')

# 筛选北京地区
beijing_jobs = [job for job in jobs if job['城市'] == '北京']

# 筛选特定薪资范围
high_salary_jobs = [
    job for job in jobs 
    if '20K' in job['薪资范围'] or '30K' in job['薪资范围']
]
```

### 数据分析 / Data Analysis

```python
import pandas as pd

# 读取导出的Excel
df = pd.read_excel('job_results.xlsx')

# 统计各城市职位数量
city_counts = df['城市'].value_counts()
print(city_counts最)

# 统计平均薪资
# 可以进一步解析薪资范围字段进行统计分析
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
- 支持智联招聘、前程无忧、BOSS直聘 / Supports Zhaopin, 51job, BOSS Zhipin
- Excel和JSON格式导出 / Excel and JSON format export

---

**觉得有用？给个Star吧！/ Find it useful? Give it a Star!** ⭐
