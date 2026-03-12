# 电商价格监控爬虫 / E-commerce Price Monitor

## 项目简介 / Project Introduction

这是一个实用的电商价格监控工具，可以自动跟踪和记录京东、淘宝等主流电商平台的商品价格变化，帮助你抓住最佳购买时机。

A practical e-commerce price monitoring tool that automatically tracks and records price changes on major e-commerce platforms like JD.com and Taobao, helping you catch the best buying opportunities.

## 功能特性 / Features

✅ **多平台支持** / Multi-platform support  
支持京东（JD.com）、淘宝（Taobao）等主流电商平台
Supports major e-commerce platforms like JD.com and Taobao

✅ **价格追踪** / Price tracking  
自动获取商品当前价格，记录历史价格数据
Automatically fetches current product prices and records historical price data

✅ **趋势分析** / Trend analysis  
生成价格趋势图表，直观展示价格变化
Generates price trend charts to visually display price changes

✅ **灵活配置** / Flexible configuration  
通过JSON配置文件管理监控商品列表
Manage monitoring product list through JSON configuration file

✅ **历史记录** / History records  
保存完整的价格历史，支持数据分析
Save complete price history, supports data analysis

## 技术栈 / Tech Stack

- **Python 3.8+**: 主要开发语言 / Main development language
- **Requests**: HTTP请求库 / HTTP request library
- **BeautifulSoup4**: HTML解析 / HTML parsing
- **Matplotlib**: 数据可视化 / Data visualization
- **JSON**: 配置文件格式 / Configuration file format

## 安装说明 / Installation

### 1. 克隆项目 / Clone Project

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo/projects/ecommerce-monitor
```

### 2. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

或逐个安装 / Or install individually:

```bash
pip install requests beautifulsoup4 lxml matplotlib
```

## 使用方法 / Usage

### 1. 配置监控商品 / Configure Products to Monitor

编辑 `config.json` 文件，添加要监控的商品信息：

Edit the `config.json` file to add product information to monitor:

```json
{
  "products": [
    {
      "name": "商品名称",
      "platform": "jd",
      "url": "商品链接",
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

### 2. 运行监控 / Run Monitor

```bash
python ecommerce_monitor.py
```

### 3. 查看价格趋势 / View Price Trends

程序会自动生成价格趋势图，保存在 `product_name_price_trend.png`

The program automatically generates price trend charts, saved as `product_name_price_trend.png`

## 项目结构 / Project Structure

```
ecommerce-monitor/
├── ecommerce_monitor.py      # 主程序 / Main program
├── config.json               # 配置文件 / Configuration file
├── requirements.txt          # 依赖列表 / Dependencies list
├── price_history.json        # 价格历史数据 / Price history data
└── README.md                 # 项目文档 / Project documentation
```

## 核心功能说明 / Core Features

### 价格监控 / Price Monitoring

```python
# 创建监控实例
monitor = EcommerceMonitor('config.json')

# 检查所有商品价格
records = monitor.check_all_products()

# 获取价格统计
monitor.print_summary()
```

### 趋势分析 / Trend Analysis

```python
# 生成价格趋势图
monitor.generate_price_chart('商品名称', 'output.png')
```

### 历史数据查询 / Historical Data Query

```python
# 获取指定商品的价格历史
history = monitor.get_price_history('商品名称')
```

## 使用场景 / Use Cases

💡 **网购比价** / Online shopping price comparison  
监控心仪商品价格，在低价时收到提醒
Monitor favorite product prices and get notified at low prices

💡 **市场分析** / Market analysis  
追踪竞争对手产品价格变化
Track competitor product price changes

💡 **数据分析** / Data analysis  
收集价格数据，进行市场趋势分析
Collect price data for market trend analysis

💡 **自动提醒** / Automated reminders  
结合定时任务，实现价格监控自动化
Combine with scheduled tasks for automated price monitoring

## 价值点 / Value Points

🎯 **实用性强** / High practicality  
直接解决网购价格监控痛点，帮助用户节省购物成本
Directly solves online shopping price monitoring pain points, helping users save shopping costs

🎯 **易于扩展** / Easy to extend  
模块化设计，支持快速添加新的电商平台
Modular design, supports quick addition of new e-commerce platforms

🎯 **数据可视化** / Data visualization  
直观的价格趋势图，便于分析和决策
Intuitive price trend charts for easy analysis and decision-making

🎯 **配置灵活** / Flexible configuration  
JSON配置文件，无需修改代码即可管理监控列表
JSON configuration file, manage monitoring list without code modification

## 注意事项 / Notes

⚠️ **反爬策略** / Anti-scraping strategies  
程序内置了随机延时和User-Agent轮换，建议不要频繁请求
The program includes random delays and User-Agent rotation, avoid frequent requests

⚠️ **网站结构变化** / Website structure changes  
电商网站可能更新页面结构，需要定期维护解析逻辑
E-commerce sites may update page structure, maintain parsing logic regularly

⚠️ **合法合规** / Legal compliance  
请遵守网站的robots.txt规则，合理使用爬虫技术
Please comply with website robots.txt rules, use web scraping technology reasonably

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
- 支持京东、淘宝价格监控 / Supports JD.com and Taobao price monitoring
- 添加价格趋势图功能 / Added price trend chart feature

---

**觉得有用？给个Star吧！/ Find it useful? Give it a Star!** ⭐
