# 新浪微博爬虫

一个功能完整的微博数据爬取和分析工具，支持用户信息获取、微博搜索、话题筛选、数据导出和分析报告生成。

## 功能特性

### 核心功能

1. **用户信息爬取**
   - 用户名、粉丝数、关注数、微博数
   - 个人简介、头像URL
   - 认证信息、地理位置
   - 性别、生日、注册日期

2. **微博搜索**
   - 关键词搜索
   - 分页获取结果
   - 支持高级搜索参数

3. **话题筛选**
   - 获取微博热搜榜
   - 按话题标签筛选（娱乐、科技、体育等）
   - 话题统计分析

4. **微博详情获取**
   - 帖子完整内容
   - 点赞、评论、转发统计
   - 图片、视频等媒体资源
   - 原帖信息（针对转发）

5. **评论获取**
   - 获取帖子评论列表
   - 支持分页和数量限制
   - 评论者信息和点赞数

6. **数据导出**
   - CSV格式（Excel兼容）
   - JSON格式（结构化数据）
   - 批量导出支持

7. **数据分析**
   - 用户排行榜（粉丝数、微博数）
   - 微博热度分析（点赞、评论、转发）
   - 话题统计和热门话题
   - 数据可视化图表

### 反爬策略

- **随机延时**：每次请求间隔2-5秒随机时间
- **User-Agent轮换**：自动切换浏览器标识
- **Session管理**：保持会话连接
- **重试机制**：失败自动重试（指数退避）
- **代理支持**：可选HTTP/HTTPS代理

## 安装

### 环境要求

- Python 3.7+
- pip包管理器

### 安装步骤

1. 克隆或下载项目

```bash
git clone <repository-url>
cd sina-scraper
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

依赖包列表：
- requests: HTTP请求库
- beautifulsoup4: HTML解析
- lxml: XML/HTML解析引擎
- pandas: 数据处理
- matplotlib: 图表绘制
- seaborn: 数据可视化
- fake-useragent: User-Agent轮换
- tqdm: 进度条显示

## 快速开始

### 基本用法

```python
from src.api import WeiboAPI
from src.exporter import DataExporter
from src.analyzer import Data

# 初始化API（可选：提供Cookie以访问需要登录的内容）
api = WeiboAPI(cookie='your_weibo_cookie')

# 获取用户信息
user = api.get_user_info('user_id_or_name')

# 搜索微博
posts = api.search_posts('关键词', page=1, max_results=20)

# 获取热搜话题
hot_topics = api.get_hot_topics()

# 导出数据
exporter = DataExporter('data')
exporter.export_users([user], format='csv')
exporter.export_posts(posts, format='json')

# 数据分析
analyzer = DataAnalyzer('data')
analyzer.generate_report([user], posts)

api.close()
```

### 运行演示脚本

```bash
python examples/demo.py
```

演示脚本会展示所有主要功能，包括：
- 用户信息创建和显示
- 微博帖子数据管理
- CSV/JSON数据导出
- 数据分析和报告生成
- 可视化图表绘制

### 运行测试

```bash
python tests/test_scraper.py
```

## 详细使用说明

### 1. 用户信息获取

```python
from src.api import WeiboAPI

api = WeiboAPI()

# 方式1：通过用户ID
user = api.get_user_info('123456789')

# 方式2：通过用户昵称
user = api.get_user_info('@用户昵称')

# 访问用户数据
print(f"用户名: {user.username}")
print(f"粉丝数: {user.fans_count:,}")
print(f"关注数: {user.follow_count:,}")
print(f"微博数: {user.weibo_count:,}")
print(f"简介: {user.bio}")
print(f"是否认证: {user.verified}")
print(f"认证类型: {user.verified_type}")
print(f"位置: {user.location}")

api.close()
```

### 2. 微博搜索

```python
from src.api import WeiboAPI

api = WeiboAPI()

# 搜索关键词
posts = api.search_posts('人工智能', page=1, max_results=20)

# 遍历搜索结果
for post in posts:
    print(f"{post.username}: {post.content[:50]}")
    print(f"  点赞: {post.likes} | 评论: {post.comments} | 转发: {post.reposts}")
    if post.topics:
        print(f"  话题: {', '.join(post.topics)}")

api.close()
```

### 3. 获取热搜话题

```python
from src.api import WeiboAPI

api = WeiboAPI()

# 获取热搜榜
hot_topics = api.get_hot_topics()

# 显示Top 10热搜
for topic in hot_topics[:10]:
    print(f"{topic['rank']}. {topic['word']} (热度: {topic['hot']})")
    print(f"   分类: {topic['category']}")

api.close()
```

### 4. 获取用户微博

```python
from src.api import WeiboAPI

api = WeiboAPI()

# 获取用户微博列表
posts = api.get_user_posts('user_id', page=1, max_posts=20)

for post in posts:
    print(f"发布时间: {post.created_at}")
    print(f"内容: {post.content}")
    print(f"互动: {post.likes} 赞 / {post.comments} 评 / {post.reposts} 转")

api.close()
```

### 5. 获取微博详情和评论

```python
from src.api import WeiboAPI

api = WeiboAPI()

# 获取帖子详情
post = api.get_post_detail('post_id')
print(f"帖子内容: {post.content}")

# 获取帖子评论
comments = api.get_post_comments('post_id', max_comments=50)

for comment in comments:
    print(f"{comment['username']}: {comment['content']}")
    print(f"  点赞: {comment['likes']}")

api.close()
```

### 6. 数据导出

```python
from src.api import WeiboAPI
from src.exporter import DataExporter

api = WeiboAPI()
exporter = DataExporter('data')  # 指定输出目录

# 获取数据
users = [api.get_user_info('user_id')]
posts = api.search_posts('关键词')

# 导出为CSV（Excel兼容）
csv_file = exporter.export_users(users, filename='users', format='csv')
csv_file = exporter.export_posts(posts, filename='posts', format='csv')

# 导出为JSON
json_file = exporter.export_users(users, filename='users', format='json')
json_file = exporter.export_posts(posts, filename='posts', format='json')

print(f"CSV导出: {csv_file}")
print(f"JSON导出: {json_file}")

api.close()
```

### 7. 数据分析

```python
from src.api import WeiboAPI
from src.exporter import DataExporter
from src.analyzer import DataAnalyzer

api = WeiboAPI()
exporter = DataExporter('data')
analyzer = DataAnalyzer('data')

# 获取数据
users = [api.get_user_info('user_id')]
posts = api.search_posts('关键词')

# 导出数据
exporter.export_users(users, 'users', 'json')
exporter.export_posts(posts, 'posts', 'json')

# 生成分析报告
report_file = analyzer.generate_report(users, posts)
print(f"分析报告: {report_file}")

# 生成可视化图表
fans_chart = analyzer.plot_user_fans(users)
interaction_chart = analyzer.plot_post_interaction(posts)

print(f"粉丝排行图: {fans_chart}")
print(f"互动分布图: {interaction_chart}")

api.close()
```

## 项目结构

```
sina-scraper/
├── README.md                 # 项目文档
├── requirements.txt          # 依赖列表
├── src/                      # 源代码目录
│   ├── __init__.py          # 包初始化
│   ├── scraper.py           # 爬虫基础类（反爬策略）
│   ├── user.py              # 用户信息类
│   ├── weibo.py             # 微博帖子类
│   ├── api.py               # 微博API接口
│   ├── exporter.py          # 数据导出器
│   └── analyzer.py          # 数据分析器
├── examples/                 # 示例脚本
│   └── demo.py              # 功能演示
├── tests/                    # 测试脚本
│   └── test_scraper.py      # 单元测试
├── docs/                     # 文档目录
├── data/                     # 数据输出目录（自动创建）
│   ├── *.json               # JSON格式数据
│   ├── *.csv                # CSV格式数据
│   ├── *.png                # 可视化图表
│   └── *.txt                # 分析报告
```

## 数据模型

### WeiboUser（用户）

```python
{
    'user_id': str,           # 用户ID
    'username': str,          # 用户名
    'nickname': str,          # 昵称
    'avatar': str,            # 头像URL
    'fans_count': int,        # 粉丝数
    'follow_count': int,      # 关注数
    'weibo_count': int,       # 微博数
    'bio': str,               # 个人简介
    'verified': bool,         # 是否认证
    'verified_type': str,     # 认证类型
    'location': str,          # 地理位置
    'gender': str,            # 性别
    'birthday': str,          # 生日
    'register_date': str,      # 注册日期
    'url': str,               # 用户主页URL
    'crawled_at': str         # 爬取时间
}
```

### WeiboPost（微博帖子）

```python
{
    'post_id': str,           # 帖子ID
    'user_id': str,           # 用户ID
    'username': str,          # 用户名
    'content': str,           # 帖子内容
    'created_at': str,        # 发布时间
    'likes': int,             # 点赞数
    'comments': int,          # 评论数
    'reposts': int,           # 转发数
    'is_repost': bool,        # 是否转发
    'original_post_id': str,  # 原帖ID
    'images': list,           # 图片URL列表
    'topics': list,           # 话题标签列表
    'url': str,               # 帖子URL
    'device': str,            # 发布设备
    'location': str,          # 位置
    'crawled_at': str         # 爬取时间
}
```

## Cookie获取方法

要访问需要登录的内容，需要提供微博Cookie。获取方法：

1. 使用浏览器登录微博（weibo.com）
2. 按F12打开开发者工具
3. 进入 Network 标签
4. 刷新页面，找到任意请求
5. 在请求头中找到 Cookie
6. 复制完整的 Cookie 值

示例：
```python
api = WeiboAPI(cookie='your_cookie_here')
```

## 注意事项

### 使用限制

1. **登录要求**：大部分功能需要登录Cookie才能使用
2. **访问频率**：内置随机延时（2-5秒），避免触发反爬
3. **数据准确性**：部分数据可能因隐私设置无法获取
4. **API变更**：微博API可能更新，需要及时调整

### 反爬建议

1. **设置Cookie**：使用真实用户Cookie
2. **使用代理**：通过代理服务器访问
3. **合理延时**：不要减少内置延时时间
4. **错误处理**：捕获异常并记录日志
5. **数据验证**：检查返回数据的完整性

### 法律声明

- 本工具仅供学习和研究使用
- 请遵守微博服务条款和隐私政策
- 不得用于商业用途或大规模爬取
- 使用本工具产生的一切后果由使用者自负

## 常见问题

### Q1: 为什么某些功能无法使用？

A: 微博大部分接口需要登录，请提供有效的Cookie。

### Q2: 如何获取Cookie？

A: 参考上文的"Cookie获取方法"章节。

### Q3: 如何使用代理？

A: 初始化时传入proxy参数：
```python
proxy = {
    'http': 'http://proxy_address:port',
    'https': 'https://proxy_address:port'
}
api = WeiboAPI(cookie='cookie', proxy=proxy)
```

### Q4: 数据导出格式？

A: 支持CSV和JSON两种格式，CSV使用utf-8-sig编码，Excel可直接打开。

### Q5: 如何批量爬取？

A: 使用循环结构，注意控制频率：
```python
user_ids = ['uid1', 'uid2', 'uid3']
users = []
for uid in user_ids:
    user = api.get.get_user_info(uid)
    if user:
        users.append(user)
exporter.export_users(users)
```

## 性能优化建议

1. **批量导出**：一次导出多条记录，减少IO操作
2. **数据缓存**：避免重复请求相同数据
3. **异步请求**：考虑使用异步库提高并发
4. **错误重试**：利用内置重试机制
5. **日志控制**：生产环境可降低日志级别

## 扩展开发

### 添加新的数据字段

在 `src/user.py` 或 `src/weibo.py` 中添加字段。

### 自定义分析功能

在 `src/analyzer.py` 中添加分析方法。

### 实现新的导出格式

在 `src/exporter.py` 中添加导出方法。

## 更新日志

### v1.0.0 (2024-01-15)

- 初始版本发布
- 实现基础爬虫功能
- 支持用户信息和微博帖子获取
- 实现数据导出（CSV/JSON）
- 实现数据分析报告
- 添加反爬策略
- 完善文档和示例

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 联系方式

- 项目主页：[GitHub仓库地址]
- 问题反馈：[Issues地址]
- 邮箱：[联系邮箱]

## 致谢

感谢以下开源项目的支持：

- requests: HTTP for Humans
- BeautifulSoup: Pythonic HTML/XML parser
- pandas: Data manipulation library
- matplotlib: Python plotting
- seaborn: Statistical data visualization

---

**最后更新**: 2024-01-15
