# B站视频信息爬虫

一个功能完整的B站视频信息爬虫，支持获取视频详细信息、批量处理、搜索、导出和分析。

## 功能特性

- ✅ 根据视频链接或BV号获取视频详细信息（标题、作者、播放量、点赞数、投币数、收藏数、分享数等）
- ✅ 支持批量获取多个视频信息
- ✅ 支持关键词搜索视频
- ✅ 导出为CSV格式
- ✅ 生成数据分析报告（播放量分布、作者排行等）
- ✅ 使用 requests + BeautifulSoup
- ✅ 添加反爬策略（随机延时、User-Agent轮换）
- ✅ 完整的错误处理和日志记录

## 安装依赖

```bash
pip install requests beautifulsoup4 pandas
```

## 项目结构

```
bilibili-scraper/
├── README.md                 # 项目文档
├── bilibili_scraper.py       # 主爬虫模块
├── demo.py                   # 演示脚本
├── test.py                   # 测试脚本
├── requirements.txt          # 依赖列表
└── examples/                 # 示例输出目录
```

## 使用方法

### 基本使用

```python
from bilibili_scraper import BiliBiliScraper

# 创建爬虫实例
scraper = BiliBiliScraper()

# 获取单个视频信息
video_info = scraper.get_video_info('BV1xx411c7mD')
print(video_info)

# 批量获取视频信息
video_list = ['BV1xx411c7mD', 'BV1y44y1K7KL']
results = scraper.batch_get_videos(video_list)

# 搜索视频
search_results = scraper.search_videos('Python教程', max_results=5)

# 导出为CSV
scraper.export_to_csv(results, 'videos.csv')

# 生成分析报告
scraper.generate_report(results, 'report.html')
```

### 运行演示

```bash
python demo.py
```

### 运行测试

```bash
python test.py
```

## API 说明

### BiliBiliScraper 类

主要方法：

- `get_video_info(bv_or_url)` - 获取单个视频信息
- `batch_get_videos(video_list)` - 批量获取视频信息
- `search_videos(keyword, max_results=10)` - 搜索视频
- `export_to_csv(data, filename)` - 导出为CSV
- `generate_report(data, filename)` - 生成HTML分析报告

## 返回数据格式

```json
{
  "bv": "BV1xx411c7mD",
  "title": "视频标题",
  "author": "作者名称",
  "author_id": "123456789",
  "views": 1000000,
  "likes": 50000,
  "coins": 20000,
  "favorites": 10000,
  "shares": 5000,
  "duration": "10:30",
  "publish_time": "2024-01-01",
  "url": "https://www.bilibili.com/video/BV1xx411c7mD"
}
```

## 注意事项

1. 请合理设置请求间隔，避免给B站服务器造成压力
2. 本项目仅用于学习和研究目的
3. B站API可能会更新，如遇问题请检查接口变化
4. 建议使用代理池进行大规模爬取

## 反爬策略

- 随机User-Agent轮换
- 随机请求延时（2-5秒）
- 请求失败自动重试
- 遵守robots.txt规则

## 许可证

MIT License

## 作者

新新

## 更新日志

### v1.0.0 (2026-03-12)

- 初始版本发布
- 支持基本视频信息获取
- 支持批量处理和搜索
- 支持CSV导出和数据分析
