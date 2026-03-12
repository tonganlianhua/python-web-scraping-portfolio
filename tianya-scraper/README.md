# 天涯论坛爬虫 (Tianya Forum Scraper)

一个功能完整的天涯论坛爬虫工具，支持帖子列表爬取、详情获取、数据分析和多格式导出。

## 功能特性

✅ **帖子列表爬取** - 获取标题、作者、回复数、点击数、发布时间、链接  
✅ **帖子详情获取** - 抓取完整内容和楼层回复  
✅ **版块筛选** - 支持天涯杂谈、情感天地、娱乐八卦等热门版块  
✅ **关键词搜索** - 根据关键词过滤帖子  
✅ **分页获取** - 支持多页数据爬取  
✅ **多格式导出** - CSV 和 JSON 格式  
✅ **数据分析** - 热帖排行、版块活跃度统计  
✅ **反爬策略** - 随机延时、User-Agent轮换  
✅ **完整文档** - 详细的使用说明和API文档  

## 项目结构

```
tianya-scraper/
├── README.md                 # 项目文档
├── requirements.txt          # 依赖包
├── tianya_scraper.py        # 主爬虫模块
├── data_exporter.py         # 数据导出模块
├── data_analyzer.py         # 数据分析模块
├── demo.py                  # 演示脚本
└── test.py                  # 测试脚本
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 基本使用 -

```python
from tianya_scraper import TianyaScraper

# 创建爬虫实例
scraper = TianyaScraper()

# 爬取天涯杂谈第一页帖子
posts = scraper.get_posts(board='zatan', page=1)
print(f"获取到 {len(posts)} 个帖子")
```

### 2. 获取帖子详情

```python
# 获取帖子详情
detail = scraper.get_post_detail(post_url)
print(f"标题: {detail['title']}")
print(f"内容: {detail['content'][:100]}...")
```

### 3. 关键词搜索

```python
# 搜索包含"AI"的帖子
results = scraper.search_posts(keyword='AI', board='zatan', page=1)
for post in results:
    print(f"{post['title']} - {post['author']}")
```

### 4. 批量爬取并导出

```python
# 爬取多页数据
all_posts = []
for page in range(1, 4):
    posts = scraper.get_posts(board='zatan', page=page)
    all_posts.extend(posts)
    scraper.random_delay()  # 随机延时

# 导出为CSV
exporter = DataExporter()
exporter.to_csv(all_posts, 'tianya_posts.csv')

# 导出为JSON
exporter.to_json(all_posts, 'tianya_posts.json')
```

### 5. 数据分析

```python
from data_analyzer import DataAnalyzer

analyzer = DataAnalyzer(all_posts)

# 生成热帖排行
hot_posts = analyzer.get_top_posts(limit=10)
print("🔥 热帖排行 Top 10:")
for i, post in enumerate(hot_posts, 1):
    print(f"{i}. {post['title']} (回复: {post['reply_count']})")

# 版块活跃度分析
activity = analyzer.get_board_activity()
print("\n📊 版块活跃度:")
for board, count in activity.items():
    print(f"{board}: {count} 帖")
```

## API 文档

### TianyaScraper 类

主要爬虫类，提供所有数据获取功能。

#### 方法

- `__init__(delay_range=(2, 5))` - 初始化爬虫，设置延时范围
- `get_posts(board, page=1, keyword=None)` - 获取帖子列表
- `get_post_detail(post_url)` - 获取帖子详情
- `search_posts(keyword, board=None, page=1)` - 搜索帖子
- `random_delay()` - 随机延时

#### 支持的版块

| 版块ID | 版块名称 |
|--------|----------|
| zatan  | 天涯杂谈 |
| feelings | 情感天地 |
| ent    | 娱乐八卦 |
| tech   | 资讯科技 |
| sports | 体育休闲 |
| finance | 财经风云 |

### DataExporter 类

数据导出类，支持多种格式。

#### 方法

- `to_csv(data, filename)` - 导出为CSV格式
- `to_json(data, filename)` - 导出为JSON格式
- `to_excel(data, filename)` - 导出为Excel格式（需要openpyxl）

### DataAnalyzer 类

数据分析类，提供统计和分析功能。

#### 方法

- `__init__(data)` - 初始化分析器
- `get_top_posts(limit=10, by='reply_count')` - 获取热门帖子
- `get_board_activity()` - 获取版块活跃度
- `get_author_stats(limit=10)` - 获取活跃作者统计
- `generate_report(output_file)` - 生成完整分析报告

## 运行演示

```bash
python demo.py
```

演示脚本会展示：
1. 爬取帖子列表
2. 获取帖子详情
3. 关键词搜索
4. 数据导出
5. 数据分析报告

## 运行测试

```bash
python test.py
```

测试脚本会验证：
1. 爬虫基本功能
2. 数据导出功能
3. 数据分析功能
4. 错误处理

## 反爬策略

1. **随机延时** - 请求间隔2-5秒随机
2. **User-Agent轮换** - 模拟不同浏览器
3. **请求头伪装** - 添加常见HTTP头
4. **异常重试** - 失败后自动重试

## 注意事项

⚠️ **爬虫使用须知**：

- 请遵守robots.txt协议
- 控制爬取频率，避免给服务器造成压力
- 数据仅供个人学习研究使用
- 请勿用于商业用途
- 建议添加适当的延时（默认2-5秒）

## 常见问题

### Q: 为什么有些帖子抓取失败？

A: 可能原因：
- 帖子已被删除
- 网络连接问题
- 触发了反爬机制
- 页面结构变化

建议：
- 增加延时时间
- 检查网络连接
- 查看错误日志

### Q: 如何提高爬取效率？

A: 
- 减少延时范围（但不建议低于1秒）
- 使用多线程（需自行实现）
- 只爬取必要的数据字段

### Q: 数据不完整怎么办？

A:
- 检查是否网络超时
- 增加重试次数
- 检查天涯网页面结构是否变化

## 更新日志

### v1.0.0 (2026-03-12)

- ✨ 初始版本发布
- ✅ 实现帖子列表爬取
- ✅ 实现帖子详情获取
- ✅ 支持版块筛选
- ✅ 支持关键词搜索
- ✅ 实现分页功能
- ✅ CSV/JSON导出
- ✅ 数据分析功能
- ✅ 反爬策略
- ✅ 完整文档和测试

## 许可使用

本项目仅供学习和研究使用。使用本工具爬取数据时，请遵守相关法律法规和网站使用条款。

## 联系方式

如有问题或建议，欢迎提Issue。

---

**Happy Scraping! 🕷️**
