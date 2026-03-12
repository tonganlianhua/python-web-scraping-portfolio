# 网易云音乐爬虫项目总结

## 项目信息

- **项目名称**: music163-scraper
- **版本**: 1.0.0
- **创建时间**: 2026-03-12
- **开发状态**: 已完成
- **项目路径**: D:\openclaw\workspace\projects\music163-scraper

## 已完成功能

### ✅ 1. 获取网易云音乐排行榜
- 支持热歌榜、新歌榜、原创榜、飙升榜、推荐榜
- 可自定义获取歌曲数量
- 实现于: `src/api_client.py` (get_top_list_songs)

### ✅ 2. 获取歌曲信息
- 歌名
- 歌手
- 专辑
- 播放量
- 评论数
- 时长
- 歌曲链接
- 实现于: `src/api_client.py`

### ✅ 3. 爬取歌曲热门评论
- 评论内容
- 点赞数
- 时间戳（原始和格式化）
- 评论用户
- 可自定义获取评论数量
- 实现于: `src/api_client.py` (get_song_comments)

### ✅ 4. 支持关键词搜索歌曲
- 关键词搜索
- 可自定义返回结果数量
- 实现于: `src/api_client.py` (search_songs)

### ✅ 5. 导出为 CSV 和 JSON 格式
- CSV导出: 使用utf-8-sig编码，确保Excel正确显示中文
- JSON导出: 结构化数据，便于程序读取
- 支持歌曲和评论数据分别导出
- 批量导出功能
- 实现于: `src/export.py`

### ✅ 6. 生成数据分析报告
**歌手排行**:
- 统计歌手出现次数
- 按出歌量排序
- 可自定义TOP N

**歌曲热度分析**:
- 按播放量排序
- 显示排名、歌名、歌手、播放量、评论数
- 可自定义TOP N

**词云生成**:
- 从评论中提取关键词
- 支持中文和英文
- 生成PNG格式词云图片
- 导出词频统计JSON
- 实现于: `src/analyzer.py`

**综合报告**:
- 包含所有分析内容
- 基本统计数据（歌曲数、歌手数、总播放量等）
- JSON格式保存

### ✅ 7. 包含详细的 README.md 文档
- 功能特性说明
- 项目结构
- 快速开始指南
- 详细使用示例
- API文档
- 配置说明
- 常见问题解答
- 免责声明

### ✅ 8. 包含演示脚本和测试脚本
**演示脚本** (`demo.py`):
- 演示1: 获取排行榜数据
- 演示2: 搜索歌曲
- 演示3: 获取多个排行榜
- 演示4: 数据导出格式
- 演示5: 数据分析功能

**测试脚本** (`test.py`):
- 配置模块测试
- API客户端测试
- 数据导出测试
- 音乐分析测试
- 爬虫主类测试
- 使用unittest框架

**快速测试** (`quick_test.py`):
- 无需网络请求的快速验证
- 测试项目结构
- 测试基本功能

**示例代码** (`examples/`):
- get_toplist.py: 获取排行榜示例
- search_music.py: 搜索音乐示例
- export_data.py: 数据导出示例
- analyze_data.py: 数据分析示例

### ✅ 9. 使用 requests + BeautifulSoup 或 API 接口
- 使用requests库进行HTTP请求
- 使用网易云音乐API接口
- 不依赖BeautifulSoup（直接使用API返回的JSON数据）

### ✅ 10. 添加反爬策略
- 随机延时: 1-3秒随机延时
- User-Agent轮换: 6个不同的User-Agent随机切换
- 自动重试机制: 失败后自动重试，最多3次
- 重试延时: 5秒
- 实现于: `src/config.py` 和 `src/api_client.py`

## 项目结构

```
music163-scraper/
├── src/                          # 源代码目录
│   ├── __init__.py              # 包初始化
│   ├── config.py                # 配置文件
│   ├── api_client.py            # API客户端 (5670字节)
│   ├── export.py                # 数据导出模块 (4693字节)
│   ├── analyzer.py              # 数据分析模块 (8058字节)
│   └── scraper.py               # 爬虫主模块 (4801字节)
├── examples/                     # 示例代码
│   ├── get_toplist.py           # 获取排行榜示例
│   ├── search_music.py          # 搜索音乐示例
│   ├── export_data.py           # 数据导出示例
│   └── analyze_data.py          # 数据分析示例
├── tests/                        # 测试目录 (空，用于用户扩展)
├── data/                         # 数据导出目录 (自动创建)
├── demo.py                       # 演示脚本 (5135字节)
├── test.py                       # 完整测试脚本 (9599字节)
├── quick_test.py                 # 快速测试脚本 (5462字节)
├── requirements.txt              # 依赖包列表
├── README.md                     # 详细文档 (5304字节)
└── .gitignore                    # Git忽略文件
```

## 核心模块说明

### 1. config.py - 配置模块
- 基础URL配置
- User-Agent池
- 请求头模板
- 榜单ID映射
- 反爬策略配置（延时、重试）
- 数据导出配置
- 分析报告配置

### 2. api_client.py - API客户端
- NetEaseMusicAPI类
- _request(): 统一请求方法，带重试
- get_top_list_songs(): 获取排行榜歌曲
- get_song_comments(): 获取歌曲评论
- search_songs(): 搜索歌曲
- get_all_top_lists_info(): 获取榜单信息
- _format_timestamp(): 时间格式化

### 3. export.py - 数据导出模块
- DataExporter类
- export_songs_to_csv(): 导出歌曲CSV
- export_songs_to_json(): 导出歌曲JSON
- export_comments_to_csv(): 导出评论CSV
- export_comments_to_json(): 导出评论JSON
- export_all(): 批量导出

### 4. analyzer.py - 数据分析模块
- MusicAnalyzer类
- analyze_artists_ranking(): 歌手排行分析
- analyze_songs_popularity(): 歌曲热度分析
- generate_wordcloud(): 生成词云
- generate_report(): 生成完整报告
- _extract_words(): 提取词汇
- _calculate_statistics(): 计算统计信息

### 5. scraper.py - 爬虫主模块
- Music163Scraper类（整合所有功能）
- scrape_top_list(): 爬取排行榜（完整流程）
- search_and_scrape(): 搜索并爬取（完整流程）
- get_available_top_lists(): 获取可用榜单

## 技术栈

- **Python 3.7+**
- **requests**: HTTP请求
- **beautifulsoup4**: HTML解析（备用）
- **pandas**: 数据处理
- **matplotlib** (可选): 数据可视化
- **wordcloud** (可选): 词云生成

## 依赖包

核心依赖（必需）:
- requests>=2.31.0
- beautifulsoup4>=4.12.0
- pandas>=2.0.0

可选依赖（用于高级功能）:
- matplotlib>=3.7.0
- wordcloud>=1.9.0
- jieba>=0.42.0

## 测试结果

### 快速测试 (quick_test.py)
```
✅ 所有测试通过!

项目结构完整,基础功能正常。

测试项目:
- 模块导入: 通过
- 文件结构: 通过（13个文件全部验证）
- 配置模块: 通过（User-Agent、请求头、榜单配置、随机延时）
- 数据导出: 通过（CSV和JSON导出、数据读取验证）
- 音乐分析: 通过（歌手排行、歌曲热度、统计计算）
```

## 使用方法

### 基本使用

```python
from src.scraper import Music163Scraper

# 创建爬虫实例
scraper = Music163Scraper()

# 获取热歌榜
result = scraper.scrape_top_list(
    list_type="hot",
    limit=50,
    fetch_comments=True,
    export=True,
    analyze=True
)
```

### 运行演示

```bash
# 完整功能演示
python demo.py

# 快速测试
python quick_test.py

# 完整测试（需要网络）
python test.py
```

### 运行示例

```bash
# 获取排行榜
python examples/get_toplist.py

# 搜索音乐
python examples/search_music.py

# 数据导出
python examples/export_data.py

# 数据分析
python examples/analyze_data.py
```

## 反爬策略详情

1. **随机延时**: 每次请求前随机等待1-3秒
2. **User-Agent轮换**: 从6个不同的User-Agent中随机选择
3. **自动重试**: 请求失败后自动重试，最多3次
4. **重试延时**: 重试间隔5秒
5. **超时设置**: 单个请求超时30秒

## 数据格式

### 歌曲数据格式
```json
{
  "id": 123456,
  "name": "歌曲名称",
  "artist": "歌手1, 歌手2",
  "album": "专辑名称",
  "play_count": 1000000,
  "comment_count": 5000,
  "duration": 300000,
  "url": "https://music.163.com/#/song?id=123456"
}
```

### 评论数据格式
```json
{
  "id": 789012,
  "song_id": 123456,
  "content": "评论内容",
  "liked_count": 100,
  "time": 1704067200000,
  "time_str": "2024-01-01 00:00:00",
  "user": "用户昵称"
}
```

## 可用榜单

| 类型 | 名称 | 说明 |
|------|------|:------|
| hot | 热歌榜 | 网易云音乐热歌排行榜 |
| new | 新歌榜 | 新歌速递排行榜 |
| original | 原创榜 | 原创音乐排行榜 |
| soar | 飙升榜 | 飙升音乐排行榜 |
| recommend | 推荐榜 | 推荐音乐排行榜 |

## 输出文件位置

所有导出文件默认保存在 `data/` 目录:

- CSV文件: UTF-8 with BOM编码，Excel可直接打开
- JSON文件: UTF-8编码，结构化数据
- 词云图片: PNG格式
- 分析报告: JSON格式

## 注意事项

1. **网络请求**: 需要稳定的网络连接
2. **API限制**: 请合理设置请求频率
3. **字体要求**: 词云生成需要系统支持中文的字体
4. **数据用途**: 仅供学习研究使用
5. **依赖安装**: 可选功能需要安装相应依赖

## 项目亮点

1. **模块化设计**: 功能分离，易于维护和扩展
2. **完整的文档**: 详细的README和代码注释
3. **丰富的示例**: 多个使用示例和演示脚本
4. **完善的测试**: 包含快速测试和完整测试
5. **反爬策略免于被识别和封禁**: 多重保护措施
6. **数据分析功能**: 不仅仅是爬取，还提供分析能力
7. **灵活的导出**: 支持多种格式和批量导出

## 后续改进建议

1. **数据持久化**: 添加数据库支持（SQLite/MySQL）
2. **增量更新**: 支持增量获取数据
3. **多线程**: 加速大量数据爬取
4. **更多榜单**: 添加更多类型的榜单
5. **用户信息**: 支持获取用户信息
4. **歌词爬取**: 添加歌词获取功能
5. **可视化**: 增强数据可视化能力
6. **API优化**: 添加更多API接口支持

## 许可证

MIT License

## 免责声明

本工具仅供学习和研究使用。使用者应遵守网易云音乐的服务条款和相关法律法规。请勿将爬取的数据用于商业用途或侵犯他人权益。

---

**项目状态**: 已完成 ✅
**最后更新**: 2026-03-12
**开发人员**: AI Assistant
