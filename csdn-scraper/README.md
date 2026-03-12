# CSDN 博客爬虫

一个功能强大的 CSDN 博客文章爬虫，支持搜索、分类筛选、数据分析和导出功能。

## 功能特性

✅ **基础爬取**
- 爬取 CSDN 博客文章（标题、作者、阅读量、点赞数、、评论数、发布时间、链接）
- 获取文章详情（完整内容）
- 获取文章评论

✅ **搜索与筛选**
- 按关键词搜索文章
- 按分类筛选（Python、Java、前端、后端等）

✅ **数据导出**
- 导出为 CSV 格式
- 支持自定义导出字段

✅ **数据分析**
- 热门文章排行（按阅读量、点赞数等）
- 作者活跃度排行
- 发布时间分布分析

✅ **反爬策略**
- 随机延时（避免频繁请求）
- User-Agent 轮换
- 请求失败重试机制

## 安装

### 环境要求
- Python 3.7+
- 依赖库：requests, beautifulsoup4, pandas, lxml

### 安装步骤

1. 克隆或下载项目到本地：
```bash
git clone <repository-url>
cd csdn-scraper
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 快速开始

### 基础使用

```python
from csdn_scraper import CSDNScraper

# 创建爬虫实例
scraper = CSDNScraper()

# 搜索文章
articles = scraper.search_articles("Python爬虫", max_pages=2)

# 导出为 CSV
scraper.export_to_csv(articles, "python_articles.csv")

# 生成分析报告
report = scraper.analyze_articles(articles)
print(report)
```

### 按分类爬取

```python
# 按分类爬取
categories = ['Python', 'Java', '前端', '后端']
for category in categories:
    articles = scraper.scrape_by_category(category, max_pages=1)
    scraper.export_to_csv(articles, f"{category}_articles.csv")
```

### 获取文章详情和评论

```python
# 获取文章详情
article_url = "https://blog.csdn.net/xxx/article/details/xxx"
detail = scraper.get_article_detail(article_url)
print(f"标题: {detail['title']}")
print(f"内容: {detail['content'][:200]}...")

# 获取评论
comments = scraper.get_comments(article_url)
for comment in comments:
    print(f"{comment['user']}: {comment['content']}")
```

## 项目结构

```
csdn-scraper/
├── csdn_scraper/          # 主包
│   ├── __init__.py       # 包初始化
│   ├── crawler.py         # 核心爬虫类
│   ├── parser.py          # HTML解析器
│   ├── exporter.py        # 数据导出
│   ├── analyzer.py        # 数据分析
│   └── utils.py           # 工具函数（反爬策略等）
├── demo.py                # 演示脚本
├── test.py                # 测试脚本
├── requirements.txt       # 依赖列表
└── README.md              # 项目文档
```

## API 文档

### CSDNScraper 类

主要爬虫类，提供所有核心功能。

#### 初始化参数

```python
CSDNScraper(
    delay_range=(1, 3),           # 随机延时范围（秒）
    max_retries=3,                # 最大重试次数
    timeout=30                    # 请求超时时间（秒）
)
```

#### 主要方法

| 方法 | 说明 |
|------|------|
| `search_articles(keyword, max_pages=1)` | 按关键词搜索文章 |
| `scrape_by_category(category, max_pages=1)` | 按分类爬取文章 |
| `get_article_detail(url)` | 获取文章详情 |
| `get_comments(url)` | 获取文章评论 |
| `export_to_csv(articles, filename)` | 导出为 CSV |
| `analyze_articles(articles)` | 生成分析报告 |

## 使用示例

### 示例 1: 搜索并导出

```python
from csdn_scraper import CSDNScraper

scraper = CSDNScraper()
articles = scraper.search_articles("机器学习", max_pages=3)
scraper.export_to_csv(articles, "machine_learning.csv")
```

### 示例 2: 获取完整文章内容

```python
from csdn_scraper import CSDNScraper

scraper = CSDNScraper()
articles = scraper.search_articles("数据分析", max_pages=1)

for article in articles[:3]:  # 获取前3篇文章的详情
    detail = scraper.get_article_detail(article['url'])
    print(f"完整内容长度: {len(detail['content'])} 字符")
```

### 示例 3: 数据分析

```python
from csdn_scraper import CSDNScraper

scraper = CSDNScraper()
articles = scraper.search_articles("Web开发", max_pages=5)

# 生成分析报告
report = scraper.analyze_articles(articles)
print("=== 热门文章 Top 10 ===")
for idx, article in enumerate(report['top_articles'][:10], 1):
    print(f"{idx}. {article['title']} - 阅读: {article['views']}")

print("\n=== 活跃作者 Top 5 ===")
for idx, author in enumerate(report['top_authors'][:5], 1):
    print(f"{idx}. {author['name']} - 文章数: {author['count']}")
```

## 运行演示

运行内置演示脚本：

```bash
python demo.py
```

这将展示：
- 搜索功能
- 分类爬取
- 获取文章详情
- 导出 CSV
- 生成分析报告

## 运行测试

运行测试脚本：

```bash
python test.py
```

## 注意事项

⚠️ **使用须知**

1. **遵守网站规则**: 请合理使用，避免频繁请求，尊重 CSDN 的服务条款
2. **数据用途**: 爬取的数据仅用于个人学习和研究，不得用于商业用途
3. **反爬策略**: 项目已内置反爬策略，但请勿恶意滥用
4. **网络延迟**: 随机延时可能导致爬取速度较慢，这是正常现象
5. **结构变化**: CSDN 网页结构可能变化，如遇问题请更新解析器

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系。

---

**免责声明**: 本项目仅用于学习和研究目的。使用本项目爬取数据时，请遵守相关法律法规和网站服务条款。作者不对使用本项目造成的任何后果负责。
