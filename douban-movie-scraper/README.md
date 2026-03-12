# 豆瓣电影爬虫

一个功能完善的豆瓣电影爬虫项目，支持爬取 Top250 榜单、搜索电影、获取详情和评论，并提供数据导出和可视化分析功能。

## ✨ 功能特性

- 🎬 **爬取 Top250**: 爬取豆瓣电影 Top250 榜单完整信息
- 🔍 **智能搜索**: 支持按关键词搜索电影
- 📝 **详情获取**: 获取电影详细信息（剧情简介、标签等）
- 💬 **评论爬取**: 支持分页获取电影评论（最新/热门）
- 📊 **数据导出**: 支持导出为 CSV 和 JSON 格式
- 📈 **数据分析**: 生成评分分布、年份分布、导演排行等分析报告
- 🎨 **可视化**: 自动生成数据可视化图表
- 🛡️ **反爬策略**: 内置随机延时、User-Agent 轮换等反爬虫措施

## 📋 系统要求

- Python 3.7+
- 依赖库：见 requirements.txt

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行演示脚本

```bash
python demo.py
```

演示菜单：

```
请选择演示功能:
  1. 爬取豆瓣电影 Top250
  2. 搜索电影
  3. 获取电影详细信息
  4. 获取电影评论
  5. 完整工作流（爬取 + 导出 + 分析）
  0. 退出
```

### 3. 运行测试

```bash
python test.py
```

## 📖 使用指南

### 爬取 Top250

```python
from scraper import DoubanMovieScraper
from utils import DataExporter, DataAnalyzer

scraper = DoubanMovieScraper()

# 爬取 Top250
movies = scraper.get_top250()
print(f"成功爬取 {len(movies)} 部电影")

# 导出为 CSV
DataExporter.to_csv(movies, 'top250.csv')

# 导出为 JSON
DataExporter.to_json(movies, 'top250.json')

# 生成分析报告
DataAnalyzer.generate_report(movies, 'output')

scraper.close()
```

### 搜索电影

```python
from scraper import DoubanMovieScraper

scraper = DoubanMovieScraper()

# 搜索电影
results = scraper.search_movies('肖申克的救赎', limit=10)

for movie in results:
    print(f"{movie['title']} - {movie['rating']}")

scraper.close()
```

### 获取电影详情

```python
from scraper import DoubanMovieScraper

scraper = DoubanMovieScraper()

# 获取电影详情（1292052 是肖申克的救赎的 ID）
detail = scraper.get_movie_detail('1292052')

print(f"电影: {detail['title']}")
print(f"评分: {detail['rating']}")
print(f"导演: {', '.join(detail['directors'])}")
print(f"剧情: {detail['summary']}")

scraper.close()
```

### 获取电影评论

```python
from scraper import DoubanMovieScraper

scraper = DoubanMovieScraper()

# 获取最新评论（20条）
comments = scraper.get_comments('1292052', limit=20, sort='new_score')

for comment in comments:
    print(f"{comment['user']}: {comment['rating']}/5")
    print(f"{comment['content']}\n")

scraper.close()
```

### 数据分析

```python
from utils import DataAnalyzer

# 评分分布分析
rating_analysis = DataAnalyzer.analyze_rating_distribution(movies)
print(f"平均评分: {rating_analysis['stats']['mean']}")

# 年份分布分析
year_analysis = DataAnalyzer.analyze_year_distribution(movies)
print(f"年份范围: {year_analysis['stats']['earliest']} - {year_analysis['stats']['latest']}")

# 导演排行
director_ranking = DataAnalyzer.analyze_director_ranking(movies, top_n=10)
for d in director_ranking:
    print(f"{d['director']}: {d['count']} 部作品")

# 生成完整报告
DataAnalyzer.generate_report(movies, 'output')
```

## 📁 项目结构

```
douban-movie-scraper/
├── scraper.py          # 主爬虫模块
├── utils.py            # 工具函数（反爬、导出、分析）
├── demo.py             # 演示脚本
├── test.py             # 测试脚本
├── requirements.txt    # 依赖库
├── README.md          # 本文档
├── output/             # 输出目录（自动生成）
│   ├── top250.csv     # 导出的 CSV 文件
│   ├── top250.json    # 导出的 JSON 文件
│   └── charts/        # 可视化图表目录
│       ├── rating_distribution.png
│       ├── year_distribution.png
│       └── director_ranking.png
└── test_output/        # 测试输出目录
```

## 🛡️ 反爬策略

项目内置以下反爬策略：

1. **随机延时**: 每次请求之间随机延时 0.5-2 秒
2. **User-Agent 轮换**: 从预定义的 User-Agent 池中随机选择
3. **请求头伪装**: 设置完整的 HTTP 请求头
4. **自动重试**: 请求失败时自动重试 3 次
5. **会话保持**: 使用 requests.Session 保持会话

在 `utils.py` 中的 `AntiSpider` 类中可以自定义：

```python
# 添加更多 User-Agent
AntiSpider.USER_AGENTS.append('你的 User-Agent')

# 调整延时范围
AntiSpider.random_delay(1.0, 3.0)
```

## 📊 数据字段

### Top250 电影字段

| 字段 | 类型 | 说明 |
|------|------|------|
| rank | int | 排名 |
| title | str | 电影标题 |
| movie_id | str | 豆瓣电影 ID |
| rating | float | 评分 |
| rating_people | int | 评价人数 |
| year | int | 上映年份 |
| directors | list | 导演列表 |
| actors | list | 主演列表 |
| quote | str | 一句话评价 |
| url | str | 豆瓣链接 |

### 电影详情字段

| 字段 | 类型 | 说明 |
|------|------|------|
| movie_id | str | 豆瓣电影 ID |
| title | str | 电影标题 |
| year | int | 上映年份 |
| rating | float | 评分 |
| rating_people | int | 评价人数 |
| directors | list | 导演列表 |
| actors | list | 主演列表 |
| genres | list | 类型/标签列表 |
| summary | str | 剧情简介 |
| quote | str | 一句话评价 |
| imdb_id | str | IMDb ID |
| url | str | 豆瓣链接 |

### 评论字段

| 字段 | 类型 | 说明 |
|------|------|------|
| user | str | 用户名 |
| rating | int | 评分（1-5） |
| rating_str | str | 评分文字（很差、较差、还行、推荐、力荐） |
| time | str | 评论时间 |
| content | str | 评论内容 |
| votes | int | 有用票数 |

## 🧪 测试

运行完整测试套件：

```bash
python test.py
```

测试覆盖：

- ✅ 反爬策略测试
- ✅ 数据导出测试
- ✅ 爬虫功能测试
- ✅ 数据分析测试

## ⚠️ 注意事项

1. **请求频率**: 请适当增加请求间隔，避免给豆瓣服务器造成压力
2. **IP 限制**: 如遇到 IP 限制，请等待一段时间再试
3. **数据更新**: 豆瓣数据会实时更新，请定期重新爬取
4. **合法使用**: 本项目仅供学习研究使用，请遵守豆瓣网站的使用条款

## 📄 License

MIT License

## 🙏 致谢

- [豆瓣电影](https://movie.douban.com/) - 数据来源
- [requests](https://requests.readthedocs.io/) - HTTP 库
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析
- [pandas](https://pandas.pydata.org/) - 数据处理
- [matplotlib](https://matplotlib.org/) - 数据可视化
- [seaborn](https://seaborn.pydata.org/) - 数据可视化

## 📞 问题反馈

如有问题或建议，欢迎提交 Issue。

---

**Enjoy Scraping! 🎬**
