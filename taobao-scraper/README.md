# 淘宝商品爬虫 (Taobao Product Scraper)

一个功能强大的淘宝商品爬虫工具，支持关键词搜索、分类筛选、价格区间筛选、排序等功能，并提供数据导出和智能分析报告。

## 功能特性

### 核心功能
- ✅ **商品信息爬取**: 商品名称、价格、销量、店铺名称、店铺评分、店铺地址、商品链接等
- ✅ **关键词搜索**: 支持任意关键词搜索商品
- ✅ **分类筛选**: 支持服装、数码、家电、美妆等多种分类
- ✅ **价格区间筛选**: 精确筛选特定价格范围的商品
- ✅ **智能排序**: 支持按销量、价格升序/降序排序
- ✅ **分页获取**: 支持翻页批量获取商品数据
- ✅ **数据导出**: 支持导出为 CSV 和 JSON 格式
- ✅ **数据分析**: 自动生成价格分布、销量排行、店铺排行等分析报告

### 反爬策略
- 🛡️ 随机延时 (避免频繁请求)
- 🛡️ User-Agent 轮换 (模拟不同浏览器)
- 🛡️ Session 管理 (保持连接复用)
- 🛡️ 请求重试机制 (网络异常自动重试)
- 🛡️ 异常处理和日志记录

## 项目结构

```
taobao-scraper/
├── src/                    # 源代码目录
│   ├── __init__.py
│   ├── scraper.py         # 核心爬虫模块
│   ├── anti_spider.py     # 反爬策略模块
│   ├── exporter.py        # 数据导出模块
│   └── analyzer.py        # 数据分析模块
├── tests/                  # 测试目录
│   └── test_scraper.py    # 单元测试
├── examples/               # 示例目录
│   ├── demo.py            # 演示脚本
│   └── demo_report.html   # 示例报告
├── data/                   # 数据目录
│   ├── products.json      # 导出的 JSON 数据
│   └── products.csv       # 导出的 CSV 数据
├── reports/                # 报告目录
│   └── analysis.html      # 分析报告
├── README.md              # 项目文档
├── requirements.txt       # 依赖列表
└── .gitignore            # Git 忽略文件
```

## 安装依赖

```bash
pip install -r requirements.txt
```

### 依赖包
- requests: HTTP 请求库
- beautifulsoup4: HTML 解析库
- pandas: 数据处理和分析
- lxml: XML/HTML 解析器
- matplotlib: 数据可视化

## 快速开始

### 基础使用

```python
from src.scraper import TaobaoScraper

# 创建爬虫实例
scraper = TaobaoScraper()

# 搜索商品
products = scraper.search(
    keyword="手机",
    page_num=1,
    page_size=20
)

# 导出数据
from src.exporter import DataExporter
exporter = DataExporter()
exporter.export_csv(products, "data/products.csv")
exporter.export_json(products, "data/products.json")
```

### 高级使用

```python
from src.scraper import TaobaoScraper
from src.exporter import DataExporter
from src.analyzer import DataAnalyzer

# 创建爬虫实例
scraper = TaobaoScraper()

# 高级搜索（带筛选和排序）
products = scraper.search(
    keyword="羽绒服",
    category="clothing",      # 分类
    price_range=(100, 500),  # 价格区间
    sort_by="sales",         # 排序方式: sales/price
    sort_order="desc",       # 排序顺序: asc/desc
    page_num_pages=3         # 爬取3页
)

# 导出数据
exporter = DataExporter()
exporter.export_csv(products, "data/dujia_down_jackets.csv")
exporter.export_json(products, "data/dujia_down_jackets.json")

# 生成分析报告
analyzer = DataAnalyzer(products)
report = analyzer.generate_report("reports/analysis.html")
print(f"报告已生成: {report}")
```

## API 文档

### TaobaoScraper 类

#### 构造函数
```python
TaobaoScraper(delay_range=(1, 3), max_retries=3, timeout=30)
```

参数:
- `delay_range`: 请求延时范围（秒），默认 (1, 3)
- `max_retries`: 最大重试次数，默认 3
- `timeout`: 请求超时时间（秒），默认 30

#### search 方法
```python
search(keyword, category=None, price_range=None, sort_by="sales", 
       sort_order="desc", page_num=1, page_size=20)
```

参数:
- `keyword`: 搜索关键词（必需）
- `category`: 商品分类（可选）
- `price_range`: 价格区间，格式 (min_price, max_price)
- `sort_by`: 排序方式，"sales" 或 "price"
- `sort_order`: 排序顺序，"asc" 或 "desc"
- `page_num`: 页码，从 1 开始
- `page_size`: 每页数量，默认 20

返回: 商品列表（字典列表）

### DataExporter 类

#### export_csv 方法
```python
export_csv(products, filename)
```

参数:
- `products`: 商品数据列表
- `filename`: 输出文件名

#### export_json 方法
```python
export_json(products, filename)
```

参数:
- `products`: 商品数据列表
- `filename`: 输出文件名

### DataAnalyzer 类

#### generate_report 方法
```python
generate_report(output_file="reports/analysis.html")
```

参数:
- `output_file`: 报告输出文件名

返回: 报告文件路径

## 示例脚本

### 运行演示脚本

```bash
# 基础演示（搜索手机，爬取1页）
python examples/demo.py --keyword "手机" --pages 1

# 高级演示（搜索羽绒服，价格区间筛选，爬取3页）
python examples/demo.py --keyword "羽绒服" --category "clothing" --min-price 100 --max-price 500 --pages 3 --sort-by sales

# 查看帮助
python examples/demo.py --help
```

## 运行测试

```bash
# 运行所有测试
python tests/test_scraper.py

# 运行测试并显示详细信息
python tests/test_scraper.py -v
```

## 数据字段说明

每个商品数据包含以下字段：

| 字段 | 说明 | 类型 |
|------|------|------|
| title | 商品名称 | string |
| price | 商品价格（元） | float |
| sales | 销量（件） | int |
| shop_name | 店铺名称 | string |
| shop_score | 店铺评分 | float |
| shop_location | 店铺地址 | string |
| product_url | 商品链接 | string |
| shop_url | 店铺链接 | string |
| image_url | 商品图片链接 | string |

## 分类列表

支持的分类：
- `clothing`: 服装
- `digital`: 数码
- `home_appliance`: 家电
- `beauty`: 美妆
- `food`: 食品
- `sports`: 运动
- `books`: 图书
- `all`: 全部分类

## 排序选项

支持的排序方式：
- `sales`: 按销量排序
- `price`: 按价格排序

支持的排序顺序：
- `asc`: 升序
- `desc`: 降序

## 分析报告内容

分析报告包含以下内容：

### 价格分布
- 价格区间统计
- 价格分布直方图
- 平均价格、中位数价格

### 销量排行
- TOP 20 畅销商品
- 销量分布统计

### 店铺排行
- TOP 20 店铺（按销量）
- 店铺评分分布

### 综合统计
- 商品总数
- 价格范围
- 销量范围
- 店铺数量

## 注意事项

### 使用限制
1. ⚠️ 淘宝有反爬机制，请勿频繁请求
2. ⚠️ 建议每次请求间隔 2-5 秒
3. ⚠️ 大量爬取可能导致 IP 被封
4. ⚠️ 本工具仅供学习研究使用

### 免责声明
- 本工具仅用于学习研究目的
- 请遵守淘宝网站的使用条款
- 不得用于商业用途
- 使用本工具产生的一切后果由使用者自行承担

## 常见问题

### Q: 为什么爬取失败？
A: 可能原因：
- 网络连接问题
- 淘宝反爬机制触发（建议增加延时）
- User-Agent 被识别（建议更新 User-Agent 列表）

### Q: 如何提高爬取成功率？
A: 建议：
- 增加请求延时（delay_range=(3, 5)）
- 减少并发请求
- 使用代理 IP
- 定期更新 User-Agent

### Q: 数据不完整？
A: 淘宝页面结构可能变化，需要更新解析逻辑

## 更新日志

### v1.0.0 (2026-03-12)
- ✅ 初始版本发布
- ✅ 支持基础搜索功能
- ✅ 支持分类、价格、排序筛选
- ✅ 支持数据导出（CSV/JSON）
- ✅ 支持数据分析报告
- ✅ 添加反爬策略
- ✅ 完善文档和测试

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue。

---

**注意**: 本项目仅供学习研究使用，请遵守相关法律法规和网站使用条款。
