# 安装和运行指南 / Installation and Running Guide

> **本文档提供详细的安装和运行说明，帮助你快速上手所有项目**  
> **This document provides detailed installation and running instructions to help you get started with all projects**

---

## 📋 目录 / Table of Contents

- [环境准备](#环境准备--environment-preparation)
- [安装步骤](#安装步骤--installation-steps)
- [运行指南](#运行指南--running-guide)
- [常见问题排查](#常见问题排查--troubleshooting)
- [进阶配置](#进阶配置--advanced-configuration)

---

## 🖥️ 环境准备 / Environment Preparation

### 1. 检查Python版本 / Check Python Version

确保已安装Python 3.8或更高版本：

Ensure Python 3.8 or higher is installed:

```bash
# Windows
python --version

# Linux/Mac
python3 --version
```

**预期输出 / Expected Output:**

```
Python 3.8.0 或更高 / Python 3.8.0 or higher
```

如果未安装Python，请访问 [Python官网](https://www.python.org/downloads/) 下载安装。

If Python is not installed, visit [Python官网](https://www.python.org/downloads/) to download and install.

### 2. 检查pip / Check pip

```bash
# Windows
python -m pip --version

# Linux/Mac
python3 -m pip --version
```

### 3. 创建虚拟环境（推荐）/ Create Virtual Environment (Recommended)

虚拟环境可以隔离项目依赖，避免冲突：

Virtual environments isolate project dependencies and avoid conflicts:

```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

**激活虚拟环境 / Activate Virtual Environment:**

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**提示：** / **Tips:**  
激活成功后，命令行前面会显示 `(venv)` 标记。

After activation, `(venv)` tag will appear at the beginning of the command line.

---

## 📦 安装步骤 / Installation Steps

### 方法一：安装所有依赖（推荐）/ Method 1: Install All Dependencies (Recommended)

在 `projects` 目录下运行：

Run in the `projects` directory:

```bash
# Windows
pip install -r requirements-all.txt

# Linux/Mac
pip3 install -r requirements-all.txt
```

**预期输出 / Expected Output:**

```
Collecting requests==2.31.0
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Collecting beautifulsoup4==4.12.3
  Downloading beautifulsoup4-4.12.3-py3-none-any.whl (142 kB)
...
Successfully installed requests-2.31.0 beautifulsoup4-4.12.3 ...
```

### 方法二：逐个安装项目依赖 / Method 2: Install Project Dependencies Individually

如果只想运行特定项目，可以只安装该项目的依赖：

If you only want to run a specific project, install only that project's dependencies:

```bash
# 电商价格监控爬虫 / E-commerce Price Monitor
cd ecommerce-monitor
pip install -r requirements.txt
cd ..

# 招聘信息爬虫 / Job Scraper
cd job-scraper
pip install -r requirements.txt
cd ..

# 新闻聚合器 / News Aggregator
cd news-aggregator
pip install -r requirements.txt
cd ..

# 微博热搜爬虫 / Weibo Hot Search Scraper
cd social-media-scraper
pip install -r requirements.txt
cd ..
```

### 验证安装 / Verify Installation

检查所有依赖是否安装成功：

Check if all dependencies are installed successfully:

```bash
# Windows
pip list

# Linux/Mac
pip3 list
```

**应该包含以下库 / Should include:**

```
requests (2.31.0)
beautifulsoup4 (4.12.3)
lxml (5.1.0)
pandas (2.2.0)
openpyxl (3.1.2)
matplotlib (3.8.2)
feedparser (6.0.10)
```

---

## 🚀 运行指南 / Running Guide

### 项目1：电商价格监控爬虫 / E-commerce Price Monitor

#### 基本运行 / Basic Run

```bash
cd ecommerce-monitor
python ecommerce_config.json.py
```

#### 配置说明 / Configuration

编辑 `config.json` 文件配置监控商品：

Edit `config.json` file to configure monitored products:

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

#### 命令行参数 / Command Line Arguments

目前版本不支持命令行参数，请使用配置文件。

Current version doesn't support command-line arguments, please use configuration file.

---

### 项目2：招聘信息爬虫 / Job Scraper

#### 基本运行 / Basic Run

```bash
cd job-scraper
python job_scraper.py
```

#### 交互式输入 / Interactive Input

运行后会提示输入：

After running, you will be prompted to input:

1. 职位关键词 / Job keyword
2. 选择平台（留空选择全部）/ Select platforms (leave empty for all)

**示例 / Example:**

```
请输入职位关键词 / Enter job keyword: Python工程师

请选择平台（多选用逗号分隔，留空则选择全部）:
Please select platforms (comma-separated, leave empty for all): zhaopin,boss
```

#### 可用平台 / Available Platforms

- `zhaopin`: 智联招聘 / Zhaopin
- `qiancheng`: 前程无忧 / 51job
- `boss`: BOSS直聘 / BOSS Zhipin

---

### 项目3：新闻聚合器 / News Aggregator

#### 基本运行 / Basic Run

```bash
cd news-aggregator

python news_aggregator.py
```

#### 交互式输入 / Interactive Input

运行后会提示输入关键词进行筛选（可选）：

After running, you will be prompted to input keyword for filtering (optional):

```
请输入搜索关键词（留空则搜索全部）/ Enter keyword (empty for all): 科技
```

#### 可用新闻源 / Available News Sources

- `people`: 人民网 / People's Daily
- `xinhua`: 新华网 / Xinhua News
- `thepaper`: 澎湃新闻 / The Paper

---

### 项目4：微博热搜爬虫 / Weibo Hot Search Scraper

#### 基本运行 / Basic Run

```bash
cd social-media-scraper
python weibo_hot_search.py
```

#### 交互式输入 / Interactive Input

运行后会提示输入关键词进行筛选（可选）：

After running, you will be prompted to input keyword for filtering (optional):

```
[2/3] 输入搜索关键词（留空则搜索全部）: 科技
```

#### 输出文件 / Output Files

- `weibo_hot_search_YYYYMMDD_HHMMSS.xlsx`: Excel格式的热搜数据 / Hot search data in Excel format

---

## 🔍 常见问题排查 / Troubleshooting

### 问题1：ModuleNotFoundError: No module named 'xxx'

**原因：** / **Cause:** 缺少依赖库

Missing dependency library

**解决方案：** / **Solution:**

```bash
# 安装缺少的库 / Install missing library
pip install xxx

# 或重新安装所有依赖 / Or reinstall all dependencies
pip install -r requirements-all.txt
```

---

### 问题2：网络连接错误 / Network Connection Error

**原因：** / **Cause:** 无法访问目标网站或网络不稳定

Cannot access target website or unstable network

**解决方案：** / **Solution:**

1. 检查网络连接 / Check network connection
2. 某些网站可能需要代理 / Some websites may require proxy
3. 检查防火墙设置 / Check firewall settings
4. 尝试增加延时参数 / Try increasing delay parameters

```python
# 示例：增加延时 / Example: increase delay
scraper = WeiboHotSearchScraper(delay_range=(3, 5))
```

---

### 问题3：编码错误 / Encoding Error

**原因：** / **Cause:** Windows系统默认编码问题

Windows system default encoding issue

**解决方案：** / **Solution:**

确保使用UTF-8编码打开文件：

Ensure using UTF-8 encoding to open files:

```python
# Python代码中 / In Python code
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
```

---

### 问题4：权限错误 / Permission Error

**原因：** / **Cause:** 没有写入权限

No write permission

**解决方案：** / **Solution:**

1. 确保当前用户有写入目录的权限 / Ensure current user has write permission to directory
2. 在Linux/Mac上可能需要使用sudo / On Linux/Mac may need to use sudo
3. 选择其他有写入权限的目录 / Choose other directories with write permission

```bash
# Linux/Mac
chmod +w directory_name
```

---

### 问题5：pip安装速度慢 / pip Installation Slow

**原因：** / **Cause:** 使用默认的PyPI源可能较慢

Using default PyPI source may be slow

**解决方案：** / **Solution:**

使用国内镜像源加速：

Use domestic mirror source to speed up:

```bash
# 使用清华镜像 / Use Tsinghua mirror
pip install -r requirements-all.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或永久配置 / Or permanently configure
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### 问题6：Excel文件无法打开 / Excel File Cannot Open

**原因：** / **Cause:** Excel版本不兼容或文件损坏

Excel version incompatible or file corrupted

**解决方案：** / **Solution:**

1. 确保安装了openpyxl库 / Ensure openpyxl library is installed
2. 使用较新的Excel版本（2010+）/ Use newer Excel version (2010+)
3. 尝试用其他工具打开（如WPS）/ Try opening with other tools (like WPS)

```bash
pip install openpyxl==3.1.2
```

---

### 问题7：matplotlib图表显示问题 / Matplotlib Chart Display Issue

**原因：** / **Cause:** 中文字体未正确配置

Chinese font not properly configured

**解决方案：** / **Solution:**

已在代码中配置中文字体，但如果仍有问题，可以手动安装字体：

Chinese font is already configured in code, but if issues persist, manually install fonts:

```bash
# Windows
# 确保系统中安装了SimHei字体 / Ensure SimHei font is installed in system

# Linux/Mac
sudo apt-get install fonts-wqy-microhei  # Ubuntu/Debian
# 或 / Or
brew install --cask font-source-han-sans  # Mac
```

---

## ⚙️ 进阶配置 / Advanced Configuration

### 1. 设置代理 / Set Proxy

如果需要通过代理访问网站：

If need to access websites through proxy:

```python
import requests

proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080',
}

response = requests.get(url, proxies=proxies)
```

---

### 2. 配置日志级别 / Configure Logging Level

修改代码中的日志级别以控制输出详细程度：

Modify logging level in code to control output verbosity:

```python
import logging

# DEBUG: 最详细 / Most detailed
logging.basicConfig(level=logging.DEBUG)

# INFO: 一般信息（默认）/ General information (default)
logging.basicConfig(level=logging.INFO)

# WARNING: 仅警告和错误 / Only warnings and errors
logging.basicConfig(level=logging.WARNING)

# ERROR: 仅错误 / Only errors
logging.basicConfig(level=logging.ERROR)
```

---

### 3. 自定义User-Agent / Custom User-Agent

修改默认的User-Agent列表：

Modify default User-Agent list:

```python
# 在类中修改 / Modify in class
user_agents = [
    '你的自定义User-Agent1 / Your custom User-Agent 1',
    '你的自定义User-Agent2 / Your custom User-Agent 2',
]
```

---

### 4. 定时运行设置 / Scheduled Run Configuration

#### Windows使用任务计划程序 / Windows Task Scheduler

1. 打开"任务计划程序" / Open "Task Scheduler"
2. 创建基本任务 / Create basic task
3. 设置触发器（如每天/每周）/ Set trigger (e.g., daily/weekly)
4. 设置操作：启动程序 / Set action: Start a program
5. 程序：`python.exe` 路径 / Program: `python.exe` path
6. 参数：脚本完整路径 / Arguments: Full path to script
7. 起始于：脚本所在目录 / Start in: Directory where script is located

#### Linux/Mac使用cron / Linux/Mac Using cron

```bash
# 编辑crontab
crontab -e

# 添加定时任务 / Add scheduled task
# 每天早上8点运行 / Run every day at 8 AM
0 8 * * * cd /path/to/projects/ecommerce-monitor && python ecommerce_monitor.py

# 每6小时运行一次 / Run every 6 hours
0 */6 * * * cd /path/to/projects/news-aggregator && python news_aggregator.py

# 保存并退出 / Save and exit
```

---

### 5. 数据存储路径自定义 / Custom Data Storage Path

修改代码中的文件保存路径：

Modify file save path in code:

```python
# 原始代码 / Original code
filename = 'output.xlsx'

# 修改为自定义路径 / Modify to custom path
filename = '/path/to/your/output.xlsx'
```

---

### 6. 数据库集成（进阶）/ Database Integration (Advanced)

可以将爬取的数据存储到数据库：

Store scraped data in database:

```python
import sqlite3
import pandas as pd

# 创建数据库连接 / Create database connection
conn = sqlite3.connect('data.db')

# 将DataFrame存入数据库 / Save DataFrame to database
df = pd.read_excel('output.xlsx')
df.to_sql('table_name', conn, if_exists='replace', index=False)

# 查询数据 / Query data
result = pd.read_sql('SELECT * FROM table_name', conn)

# 关闭连接 / Close connection
conn.close()
```

---

## 📚 更多资源 / More Resources

- [项目主文档](./README.md)
- [演示文档](./DEMO.md)
- [各项目详细文档 / Detailed project documentation]
  - [电商价格监控](./ecommerce-monitor/README.md)
  - [招聘信息爬虫](./job-scraper/README.md)
  - [新闻聚合器](./news-aggregator/README.md)
  - [微博热搜爬虫](./social-media-scraper/README.md)

---

## 🆘 获取帮助 / Get Help

如果遇到本文档未涵盖的问题：

If you encounter issues not covered in this document:

- 📧 邮箱 / Email: [your-email@example.com]
- 💼 GitHub Issues: [https://github.com/yourusername/issues]
- 📖 查看各项目的README文档 / Check each project's README documentation

---

**🎉 祝使用愉快！/ Enjoy using!** 🎉

**如有问题，请查看[FAQ](#常见问题排查--troubleshooting)部分 / For questions, see [FAQ](#常见问题排查--troubleshooting) section**
