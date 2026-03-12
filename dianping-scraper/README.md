# 大众点评爬虫

一个功能完善的大众点评商家信息爬虫，支持商家搜索、评论获取、数据导出和可视化分析。

## ✨ 功能特性

- 🔍 **商家搜索**
  - 按城市搜索
  - 按关键词搜索（美食、酒店、娱乐等）
  - 按评分筛选
  - 支持分页获取

- 📊 **数据采集**
  - 店名、评分、地址
  - 人均消费、营业时间
  - 评论数等详细信息

- 💬 **评论获取**
  - 获取商家评论列表
  - 支持评论内容、评分、日期等

- 📁 **数据导出**
  - CSV 格式
  - JSON 格式
  - UTF-8 编码支持中文

- 📈 **数据分析**
  - 评分分布统计
  - 人均消费分析
  - 热门商家排行
  - 可视化图表生成

- 🛡️ **反爬策略**
  - 随机延时
  - User-Agent 轮换
  - 请求头伪装
  - 会话管理

## 📋 环境要求

- Python 3.7+
- requests
  - beautifulsoup4
- lxml
- matplotlib（可视化图表）

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install requests beautifulsoup4 lxml matplotlib
```

### 2. 基本使用

#### 简单搜索

```python
from scraper import DianpingScraper

# 创建爬虫实例
scraper = DianpingScraper(city="北京", keyword="美食")

# 搜索商家
merchants = scraper.search_merchants("北京", "美食", page=1)

# 查看结果
for merchant in merchants:
    print(f"{merchant['name']} - 评分: {merchant['rating']}")
```

#### 多页爬取

```python
# 爬取多页数据
scraper = DianpingScraper(city="上海", keyword="酒店")
scraper.crawl_multiple_pages(
    city="上海",
    keyword="酒店",
    start_page=1,
    max_pages=3  # 爬取3页
)
```

#### 评分筛选

```python
# 只爬取评分 >= 4.5 的商家
scraper = DianpingScraper(
    city="广州",
    keyword="餐厅",
    min_rating=4.5
)

merchants = scraper.search_merchants("广州", "餐厅", page=1)
```

### 3. 数据导出

```python
# 导出到 CSV
scraper.export_to_csv('merchants.csv', data_type='merchants')

# 导出到 JSON
scraper.export_to_json('merchants.json', data_type='merchants')
```

### 4. 数据分析报告

```python
# 生成报告
report = scraper.generate_report()
print(report)

# 或者使用高级导出器
from exporter import DataExporter

exporter = DataExporter()

# 生成更详细的报告
report = Merport.generate_text_report(scraper.merchants)
exporter.save_report(report, 'report.txt')

# 绘制图表
exporter.plot_rating_distribution(scraper.merchants, 'rating_dist.png')
exporter.plot_price_distribution(scraper.merchants, 'price_dist.png')
```

### 5. 获取评论

```python
# 获取商家评论
if scraper.merchants:
    merchant_url = scraper.merchants[0].get('url', '')
    if merchant_url:
        reviews = scraper.get_merchant_reviews(merchant_url, limit=10)
        for review in reviews:
            print(f"{review['user']}: {review['content'][:50]}...")
```

## 📖 详细文档

### 核心类说明

#### DianpingScraper

主要的爬虫类，提供所有爬取功能。

**方法：**

- `__init__(city, keyword, min_rating)`: 初始化爬虫
- `search_merchants(city, keyword, page)`: 搜索商家
- `crawl_multiple_pages(city, keyword, start_page, max_pages)`: 爬取多页
- `get_merchant_reviews(merchant_url, limit)`: 获取商家评论
- `export_to_csv(filename, data_type)`: 导出到 CSV
- `export_to_json(filename, data_type)`: 导出到 JSON
- `generate_report()`: 生成分析报告

#### DataExporter

数据导出和分析类，提供更高级的数据处理功能。

**方法：**

- `export_csv(data, filename, encoding)`: 导出到 CSV
- `export_json(data, filename)`: 导出到 JSON
- `generate_text_report(merchants, reviews)`: 生成文本报告
- `save_report(report, filename)`: 保存报告到文件
- `plot_rating_distribution(merchants, filename)`: 绘制评分分布图
- `plot_price_distribution(merchants, filename)`: 绘制人均消费分布图

### 数据结构

#### 商家数据 (Merchant)

```python
{
    'name': '商家名称',
    'rating': 4.5,              # 评分
    'address': '商家地址',
    'avg_price': 100,           # 人均消费
    'business_hours': '营业时间',
    'review_count': 500,        # 评论数
    'url': '商家链接',
    'city': '城市',
    'keyword': '搜索关键词'
}
```

#### 评论数据 (Review)

```python
{
    'user': '用户名',
    'rating': 4.0,              # 用户评分
    'content': '评论内容',
    'date': '评论日期',
    'likes': 10                 # 点赞数
}
```

## 🎯 使用示例

### 示例 1: 爬取北京火锅店数据

```python
from scraper import DianpingScraper
from exporter import DataExporter

# 创建爬虫
scraper = DianpingScraper(city="北京", keyword="火锅")

# 爬取数据
scraper.crawl_multiple_pages(city="北京", keyword="火锅", max_pages=2)

# 导出数据
scraper.export_to_csv('beijing_hotpot.csv')

# 生成报告
exporter = DataExporter()
report = exporter.generate_text_report(scraper.merchants)
print(report)
```

### 示例 2: 筛选高评分商家并分析

```python
from scraper import DianpingScraper
from exporter import DataExporter

# 只爬取高评分商家
scraper = DianpingScraper(city="上海", keyword="日料", min_rating=4.5)
scraper.search_merchants("上海", "日料", page=1)

# 生成分析报告
exporter = DataExporter()
report = exporter.generate_text_report(scraper.merchants)
exporter.save_report(report, 'high_rating_report.txt')

# 绘制图表
exporter.plot_rating_distribution(scraper.merchants, 'high_rating_rating.png')
exporter.plot_price_distribution(scraper.merchants, 'high_rating_price.png')
```

### 示例 3: 批量爬取多个城市

```python
from scraper import DianpingScraper
from exporter import DataExporter
import time

cities = ['北京', '上海', '广州', '深圳']
keyword = '咖啡馆'

exporter = DataExporter()
all_merchants = []

for city in cities:
    print(f"\n正在爬取 {city} 的 {keyword}...")
    scraper = DianpingScraper(city=city, keyword=keyword)
    scraper.search_merchants(city, keyword, page=1)

    all_merchants.extend(scraper.merchants)

    # 城市间延时
    time.sleep(2)

# 导出所有数据
exporter.export_csv(all_merchants, 'all_cities_coffeeshop.csv')
exporter.export_json(all_merchants, 'all_cities_coffeeshop.json')

# 生成综合报告
report = exporter.generate_text_report(all_merchants)
exporter.save_reportser(report, 'all_cities_report.txt')

print(f"\n总共爬取 {len(all_merchants)} 个商家")
```

## 🧪 测试

运行测试套件：

```bash
python test.py
```

测试覆盖：
- 爬虫类功能测试
- 导出器类功能测试
- 集成测试

## 🎬 演示

运行演示程序：

```bash
python demo.py
```

演示内容包括：
1. 基本搜索
2. 多页爬取
3. 评分筛选
4. 数据导出
5. 数据分析报告
6. 高级导出和分析
7. 完整工作流程

## ⚙️ 配置说明

### User-Agent 配置

在 `scraper.py` 中的 `USER_AGENTS` 列表可以自定义 User-Agent：

```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...',
    # 添加更多 User-Agent
]
```

### 延时配置

修改 `random_delay` 方法的参数来调整延时范围：

```python
def _random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
    delay = random.uniform(min_seconds, max_seconds)
    time.time.sleep(delay)
```

### 字体配置

用于图表的中文字体配置在 `exporter.py` 中：

```python
font_names = ['SimHei', 'Microsoft YaHei', 'SimSun', 'KaiTi']
```

## ⚠️ 注意事项

1. **遵守网站规则**: 使用本爬虫时，请遵守大众点评网站的 robots.txt 规定和使用条款

2. **请求频率**: 不要过度频繁地请求，使用内置的延时功能避免对服务器造成压力

3. **数据使用**: 爬取的数据仅用于学习和研究目的，不得用于商业用途

4. **反爬机制**: 大众点评可能有反爬机制，如遇到问题：
   - 增加延时时间
   - 更换 User-Agent
   - 使用代理 IP（需自行实现）

5. **数据准确性**: 网站结构可能变化，导致解析失败，需要及时更新代码

## 📊 输出示例

### 分析报告示例

```
======================================================================
                        大众点评数据分析报告
======================================================================

📋 基本信息
  • 商家总数: 50
  • 城市: 北京
  • 搜索关键词: 火锅
  • 评论数: 0

⭐ 评分分析
  • 平均评分: 4.25
  • 最高评分: 5.0
  • 最低评分: 3.5
  • 评分分布:
      5星:  10家 (20.0%) ████████████
      4星:  25家 (50.0%) ████████████████████████████
      3星:  15家 (30.0%) ████████████████

💰 人均消费分析
  • 平均人均: 120元
  • 最高人均: 300元
  • 最低人均: 50元
  • 价格分布:
      50元以下 :   5家 (10.0%) ██
      50-100元  :  15家 (30.0%) ████████████████
      100-200元 :  20家 (40.0%) ████████████████████████
      200-300元 :   8家 (16.0%) ████████
      300元以上  :   2家 ( 4.0%) █

🏆 评分TOP10商家
   1. 海底捞火锅     - 5.0分 (1000评论, 150元)
   2. 呷哺呷哺       - 4.8分 ( 800评论,  80元)
   ...
```

## 🐛 常见问题问题

**Q: 爬取不到数据怎么办？**

A: 可能的原因：
1. 网站结构变化，需要更新解析逻辑
2. 被反爬机制拦截，增加延时或更换 IP
3. 网络连接问题，检查网络设置

**Q: 导出的 CSV 文件乱码怎么办？**

A: 使用 UTF-8-BOM 编码打开，或在 Excel 中选择正确的编码格式。

**Q: 图表中文显示为方块怎么办？**

A: 检查系统中是否安装了中文字体，或修改 `exporter.py` 中的字体配置。

**Q: 如何使用代理 IP？**

A: 需要在 `requests.Session` 中配置代理，示例：

```python
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080',
}
session = requests.Session()
session.proxies.update(proxies)
```

## 📝 更新日志

### v1.0.0 (2026-03-12)
- 初始版本发布
- 支持商家搜索和分页爬取
- 支持评论获取
- 支持 CSV 和 JSON 导出
- 支持数据分析和可视化
- 包含完整测试和演示

## 📄 许可证

本项目仅供学习和研究使用。使用本爬虫时请遵守相关法律法规和网站规定。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请通过 Issue 联系。

---

**免责声明**: 本爬虫仅用于技术学习和研究目的。使用者需自行承担使用本工具产生的一切后果，开发者不承担任何责任。请遵守大众点评网站的服务条款和 robots.txt 规定。
