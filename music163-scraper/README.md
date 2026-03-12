# 网易云音乐爬虫 (NetEase Music Scraper)

一个功能强大的网易云音乐数据爬虫工具，支持获取排行榜、搜索歌曲、爬取评论、数据导出和可视化分析。

## ✨ 功能特性

- 🎵 **排行榜爬取**: 支持热歌榜、新歌榜、原创榜、飙升榜、推荐榜
- 🔍 **歌曲搜索**: 支持关键词搜索歌曲
- 💬 **评论爬取**: 获取歌曲热门评论
- 📊 **数据分析**: 生成歌手排行、歌曲热度分析、词云
- 📁 **多格式导出**: 支持CSV和JSON格式导出
- 🛡️ **反爬策略**: 随机延时、User-Agent轮换、自动重试

## 📁 项目结构

```
music163-scraper/
├── src/                    # 源代码目录
│   ├── config.py          # 配置文件
│   ├── api_client.py      # API客户端
│   ├── export.py          # 数据导出模块
│   ├── analyzer.py        # 数据分析模块
│   └── scraper.py         # 爬虫主模块
├── tests/                  # 测试目录
├── data/                   # 数据导出目录
├── examples/               # 示例代码
├── demo.py                 # 演示脚本
├── test.py                 # 测试脚本
├── requirements.txt        # 依赖包列表
└── README.md              # 本文档
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.7+
- 依赖包见 `requirements.txt`

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行演示脚本

```bash
python demo.py
```

演示脚本将展示所有主要功能：
1. 获取热歌榜数据
2. 搜索歌曲
3. 获取多个排行榜
4. 数据导出
5. 数据分析

### 4. 运行测试

```bash
python test.py
```

## 📖 使用指南

### 基本用法

```python
from src.scraper import Music163Scraper

# 创建爬虫实例
scraper = Music163Scraper()

# 获取热歌榜前50首歌曲
result = scraper.scrape_top_list(
    list_type="hot",      # 榜单类型: hot, new, original, soar, recommend
    limit=50,             # 获取歌曲数量
    fetch_comments=True,  # 是否获取评论
    comments_limit=20,    # 每首歌获取评论数
    export=True,          # 是否导出数据
    analyze=True          # 是否生成分析报告
)

# 查看结果
print(f"获取到 {len(result['songs'])} 首歌曲")
print(f"获取到 {len(result['comments'])} 条评论")
```

### 搜索歌曲

```python
# 搜索歌曲
result = scraper.search_and_scrape(
    keyword="周杰伦",      # 搜索关键词
    limit=30,             # 搜索结果数量
    fetch_comments=True,  # 是否获取评论
    comments_limit=20,    # 每首歌获取评论数
    export=True           # 是否导出数据
)
```

### 高级用法

#### 单独使用各模块

```python
from src.api_client import NetEaseMusicAPI
from src.export import DataExporter
from src.analyzer import MusicAnalyzer

# 1. 使用API客户端获取数据
api = NetEaseMusicAPI()
songs = api.get_top_list_songs("hot", limit=50)
comments = api.get_song_comments(song_id=123456, limit=20)

# 2. 导出数据
exporter = DataExporter()
exporter.export_songs_to_csv(songs, "my_songs.csv")
exporter.export_songs_to_json(songs, "my_songs.json")

# 3. 数据分析
analyzer = MusicAnalyzer()
artist_ranking = analyzer.analyze_artists_ranking(songs, top_n=20)
song_popularity = analyzer.analyze_songs_popularity(songs, top_n=50)
wordcloud_results = analyzer.generate_wordcloud(comments)
```

## 📊 数据分析功能

### 歌手排行

```python
# 分析歌手出现次数排行
analyzer = MusicAnalyzer()
ranking = analyzer.analyze_artists_ranking(songs, top_n=20)

for item in ranking:
    print(f"{item['rank']}. {item['artist']}: {item['song_count']}首")
```

### 歌曲热度分析

```python
# 按播放量分析歌曲热度
popularity = analyzer.analyze_songs_popularity(songs, top_n=50)

for item in popularity:
    print(f"{item['rank']}. {item['name']} - {item['artist']}")
    print(f"   播放量: {item['play_count']:,}")
    print(f"   评论数: {item['comment_count']:,}")
```

### 词云生成

```python
# 生成评论词云
wordcloud_results = analyzer.generate_wordcloud(comments, max_words=100)

# 结果包含:
# - wordcloud_image: 词云图片路径
# - word_freq_json: 词频统计JSON路径
```

### 生成完整报告

```python
# 生成包含所有分析内容的报告
report_path = analyzer.generate_report(
    songs=songs,
    comments=comments,
    include_wordcloud=True,
    filename="my_report.json"
)
```

## 📁 数据导出格式

### CSV格式

导出的CSV文件包含以下字段：

**songs.csv**:
- id: 歌曲ID
- name: 歌曲名称
- artist: 歌手名称
- album: 专辑名称
- play_count: 播放量
- comment_count: 评论数
- duration: 时长（毫秒）
- url: 歌曲链接

**comments.csv**:
- id: 评论ID
- song_id: 歌曲ID
- content: 评论内容
- liked_count: 点赞数
- time: 时间戳
- time_str: 格式化时间
- user: 评论用户

### JSON格式

JSON格式包含完整的结构化数据，可以直接用Python读取：

```python
import json

with open("data/songs_xxx.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

for song in songs:
    print(f"{song['name']} - {song['artist']}")
```

## 🔧 配置说明

配置文件 `src/config.py` 包含以下可调参数：

```python
# 反爬策略
MIN_DELAY = 1.0       # 最小延时（秒）
MAX_DELAY = 3.0       # 最大延时（秒）
MAX_RETRIES = 3       # 最大重请求次数
RETRY_DELAY = 5.0     # 重试延时（秒）

# 分析配置
WORDCLOUD_MAX_WORDS = 100  # 词云最大词汇数
TOP_N_ARTISTS = 20         # 歌手排行数量
TOP_N_SONGS = 50           # 歌曲热度排行数量
```

## 📋 榜单类型

| 类型 | 名称 | 说明 |
|------|------|------|
| hot | 热歌榜 | 网易云音乐热歌排行榜 |
| new | 新歌榜 | 新歌速递排行榜 |
| original | 原创榜 | 原创音乐排行榜 |
| soar | 飙升榜 | 飙升音乐排行榜 |
| recommend | 推荐榜 | 推荐音乐排行榜 |

## ⚠️ 注意事项

1. **请求频率**: 请合理设置请求间隔，避免过于频繁的请求
2. **数据来源**: 本工具使用非官方API接口，请勿用于商业用途
3. **版权**: 爬取的数据仅供学习研究使用
4. **网络**: 需要稳定的网络连接
5. **字体**: 词云生成需要系统安装支持中文的字体（Windows默认支持）

## 🐛 常见问题

### 1. 请求失败

**问题**: 出现连接错误或超时

**解决方案**:
- 检查网络连接
- 增加 `config.py` 中的延时设置
- 增加重试次数

### 2. 中文乱码

**问题**: CSV文件在Excel中显示乱码

**解决方案**:
- 使用 `utf-8-sig` 编码（默认已设置）
- 用文本编辑器打开查看
- 使用导入功能而非直接打开

### 3. 词云无法生成

**问题**: 提示 "wordcloud库未安装"

**解决方案**:
```bash
pip install wordcloud matplotlib
```

### 4. JSON解析失败

**问题**: API返回格式变化

**解决方案**:
- API接口可能已更新
- 检查错误日志中的响应内容
- 等待或联系维护者更新

## 📄 示例代码

查看 `examples/` 目录获取更多使用示例：

- `get_toplist.py`: 获取排行榜示例
- `search_music.py`: 搜索音乐示例
- `export_data.py`: 数据导出示例
- `analyze_data.py`: 数据分析示例

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📝 License

MIT License

## ⭐ 免责声明

本工具仅供学习和研究使用。使用者应遵守网易云音乐的服务条款和相关法律法规。请勿将爬取的数据用于商业用途或侵犯他人权益。

---

**作者**: AI Assistant
**版本**: 1.0.0
**最后更新**: 2026-03-12
