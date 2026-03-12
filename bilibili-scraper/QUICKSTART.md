# 快速开始指南

这是一个快速入门指南，帮助你快速上手B站视频爬虫。

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install requests beautifulsoup4 pandas lxml
```

## 2. 基本使用

### 2.1 获取单个视频信息

```python
from bilibili_scraper import BiliBiliScraper

# 创建爬虫实例
scraper = BiliBiliScraper()

# 获取视频信息（支持BV号或URL）
video_info = scraper.get_video_info('BV1xx411c7mD')
print(video_info)

# 使用URL也可以
video_info = scraper.get_video_info('https://www.bilibili.com/video/BV1xx411c7mD')

# 关闭连接
scraper.close()
```

### 2.2 批量获取视频

```python
scraper = BiliBiliScraper()

# 准备视频列表（BV号或URL）
video_list = [
    'BV1xx411c7mD',
    'BV1y44y1K7KL',
    'https://www.bilibili.com/video/BV1bV4y1k7Vp'
]

# 批量获取
results = scraper.batch_get_videos(video_list)

# 遍历结果
for video in results:
    print(f"{video['title']} - {video['views']} 播放")

scraper.close()
```

### 2.3 搜索视频

```python
scraper = BiliBiliScraper()

# 搜索视频
results = scraper.search_videos('Python教程', max_results=5)

for video in results:
    print(f"{video['title']} - {video['author']}")

scraper.close()
```

### 2.4 导出CSV

```python
scraper = BiliBiliScraper()

# 获取数据
results = scraper.batch_get_videos(['BV1xx411c7mD', 'BV1y44y1K7KL'])

# 导出为CSV
scraper.export_to_csv(results, 'my_videos.csv')

scraper.close()
```

### 2.5 生成分析报告

```python
scraper = BiliBiliScraper()

# 获取数据
results = scraper.batch_get_videos(['BV1xx411c7mD', 'BV1y44y1K7KL'])

# 生成HTML报告
scraper.generate_report(results, 'analysis_report.html')

scraper.close()
```

# 用浏览器打开 report.html 查看报告
```

## 3. 运行演示

项目包含完整的演示脚本：

```bash
python demo.py
```

演示脚本会展示所有功能：
- 获取单个视频信息
- 批量获取视频
- 搜索视频
- 生成分析报告
- URL和BV号解析

## 4. 运行测试

项目包含完整的测试套件：

```bash
python test.py
```

测试会验证：
- BV号提取
- 视频信息获取
- 批量处理
- CSV导出
- 报告生成
- 错误处理

## 5. 配置选项

### 调整请求延时

```python
# 创建爬虫时设置延时范围（秒）
scraper = BiliBiliScraper(min_delay=2.0, max_delay=5.0)
```

### 获取的数据字段

每个视频信息包含以下字段：

- `bv`: BV号
- `title`: 视频标题
- `author`: 作者名称
- `author_id`: 作者ID
- `views`: 播放量
- `likes`: 点赞数
- `coins`: 投币数
- `favorites`: 收藏数
- `shares`: 分享数
- `duration`: 视频时长
- `publish_time`: 发布时间
- `url`: 视频URL

## 6. 实用示例

### 示例1：获取热门作者的视频

```python
from bilibili_scraper import BiliBiliScraper

scraper = BiliBiliScraper()

# 搜索特定作者的教程
results = scraper.search_videos('编程教程', max_results=10)

# 按播放量排序
results.sort(key=lambda x: x.get('views', 0), reverse=True)

# 导出
scraper.export_to_csv(results, 'top_tutorials.csv')

scraper.close()
```

### 示例2：分析多个视频的数据

```python
from bilibili_scraper import BiliBiliScraper
import pandas as pd

scraper = BiliBiliScraper()

# 获取数据
results = scraper.batch_get_videos([
    'BV1xx411c7mD',
    'BV1y44y1K7KL',
    'BV1bV4y1k7Vp'
])

# 转换为DataFrame进行进一步分析
df = pd.DataFrame(results)

# 计算互动率（点赞+投币+收藏）/播放量
df['interaction_rate'] = (
    df['likes'] + df['coins'] + df['favorites']
) / df['views'] * 100

# 打印互动率最高的视频
print(df.nlargest(5, 'interaction_rate')[['title', 'interaction_rate']])

scraper.close()
```

### 示例3：使用上下文管理器

```python
from bilibili_scraper import BiliBiliScraper

# 使用with语句自动关闭连接
with BiliBiliScraper() as scraper:
    results = scraper.get_video_info('BV1xx411c7mD')
    print(results['title'])
```

## 7. 注意事项

1. **请求频率**：请合理设置延时，避免给B站服务器造成压力
2. **错误处理**：爬虫会自动重试失败的请求
3. **数据验证**：某些视频可能无法获取完整数据
4. **网络问题**：如遇网络问题，检查代理设置

## 8. 常见问题

### Q: 为什么有些视频无法获取信息？

A: 可能的原因：
- 视频已被删除或设置为私有
- 网络连接问题
- B站API更新（爬虫会尝试多种方式获取数据）

### Q: 如何加快爬取速度？

A: 可以减小延时范围，但不建议设置得太低：

```python
scraper = BiliBiliScraper(min_delay=0.5, max_delay=1.5)
```

### Q: 数据不准确怎么办？

A: B站的统计数据可能有延迟，这是正常现象。

## 获取更多帮助

- 查看 `README.md` 了解完整功能
- 查看 `demo.py` 查看更多示例
- 运行 `python test.py` 查看测试用例

祝你使用愉快！🎉
