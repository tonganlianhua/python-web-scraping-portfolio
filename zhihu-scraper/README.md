# 知乎爬虫

一个功能完整的知乎爬虫项目，支持搜索问题、获取问题详情、抓取回答、数据导出和数据分析。

## ✨ 功能特性

- 🔍 **搜索问题** - 支持关键词搜索知乎问题
- 📁 **话题筛选** - 按话题（技术、生活、娱乐等）获取热门问题
- 📄 **问题详情** - 获取完整的问题信息（标题、作者、描述、回答数、关注数、浏览量、创建时间）
- 💬 **回答抓取** - 获取问题的所有回答，支持分页
- 📊 **数据分析** - 生成热门问题排行、作者排行、回答分析等报告
- 💾 **多格式导出** - 支持 CSV 和 JSON 格式导出
- 🛡️ **反爬策略** - 随机延时、User-Agent 轮换、请求头伪装
- 📝 **详细文档** - 完整的 README 和代码注释

## 📦 依赖要求

```bash
requests>=2.31.0
beautifulsoup4>=4.12.0
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests beautifulsoup4
```

### 2. 基本使用

#### 搜索问题

```python
from zhihu_scraper import ZhihuScraper

scraper = ZhihuScrScraper()
questions = scraper.search_questions("Python编程", limit=5)

for q in questions:
    print(f"问题: {q['title']}")
    print(f"链接: {q['url']}")

scraper.close()
```

#### 获取问题详情

```python
from zhihu_scraper import ZhihuScraper

scraper = ZhihuScraper()
detail = scraper.get_question_detail("27446676")

print(f"标题: {detail['title']}")
print(f"作者: {detail['author']}")
print(f"回答数: {detail['answer_count']}")
print(f"关注数: {detail['follower_count']}")
print(f"浏览量: {detail['visited_count']}")

scraper.close()
```

#### 获取问题回答

```python
from zhihu_scraper import ZhihuScraper

scraper = ZhihuScraper()

# 获取前20个回答
answers = scraper.get_question_answers("27446676", limit=20)

# 获取所有回答（分页）
all_answers = scraper.get_all_answers("27446676", max_answers=100)

for answer in answers:
    print(f"作者: {answer['author']}")
    print(f"点赞数: {answer['voteup_count']}")
    print(f"内容: {answer['content'][:100]}...")

scraper.close()
```

#### 按话题获取问题

```python
from zhihu_scraper import ZhihuScraper, TOPIC_IDS

scraper = ZhihuScraper()

# 查看可用话题
print("可用话题:", list(TOPIC_IDS.keys()))

# 获取"技术"话题的热门问题
topic_id = TOPIC_IDS['技术']
questions = scraper.get_topic_questions(topic_id, limit=10)

for q in questions:
    print(f"问题: {q['title']}")

scraper.close()
```

### 3. 数据导出

```python
from zhihu_scraper import ZhihuScraper
from data_exporter import DataExporter

scraper = ZhihuScraper()
exporter = DataExporter()

# 获取数据
detail = scraper.get_question_detail("27446676")
answers = scraper.get_all_answers("27446676", max_answers=50)

# 导出问题详情
exporter.export_to_json([detail], "question_detail")
exporter.export_to_csv([detail], "question_detail")

# 导出回答
exporter.export_answers(answers, "27446676")

scraper.close()
```

### 4. 数据分析

```python
from zhihu_scraper import ZhihuScraper
from data_exporter import DataExporter
from analyzer import DataAnalyzer

scraper = ZhihuScraper()
analyzer = DataAnalyzer()
exporter = DataExporter()

# 获取数据
detail = scraper.get_question_detail("27446676")
answers = scraper.get_all_answers("27446676", max_answers=100)

# 生成分析报告
report = analyzer.generate_comparison_report(detail, answers)

# 生成文本报告
text_report = analyzer.generate_text_report(report['answers_analysis'], 'answers')
print(text_report)

# 保存报告
exporter.export_analysis_report(report, "27446676")
analyzer.save_text_report(text_report, "output/report.txt")

scraper.close()
```

## 📁 项目结构

```
zhihu-scraper/
├── config.py           # 配置文件（用户代理、延迟等）
├── zhihu_scraper.py    # 爬虫核心模块
├── data_exporter.py    # 数据导出模块
├── analyzer.py         # 数据分析模块
├── demo.py             # 演示脚本
├── test.py             # 测试脚本
├── README.md           # 项目文档
├── output/             # 输出目录
│   ├── data/          # 数据文件
│   └── question_xxx/   # 按问题ID组织的文件夹
└── requirements.txt     # 依赖列表
```

## 🎯 支持的话题

项目内置了常用话题的 ID 映射：

- 技术
- 编程
- 互联网
- 生活
- 健康
- 美食
- 娱乐
- 电影
- 音乐
- 旅游
- 财经
- 教育

可以通过 `TOPIC_IDS` 字典查看所有可用话题：

```python
from zhihu_scraper import TOPIC_IDS
print(TOPIC_IDS)
```

## 🔧 配置说明

在 `config.py` 中可以调整以下参数：

- `MIN_DELAY` / `MAX_DELAY` - 请求延迟范围（秒）
- `MAX_RETRIES` - 请求重试次数
- `REQUEST_TIMEOUT` - 请求超时时间（秒）
- `USER_AGENTS` - 用户代理列表

## 🧪 运行测试

```bash
python test.py
```

测试脚本会验证所有主要功能：
- 搜索问题
- 获取问题详情
- 获取回答
- 分页功能
- 数据导出
- 数据分析
- 完整工作流

## 🎬 运行演示

```bash
python demo.py
```

演示脚本会展示所有功能的使用方法：
1. 搜索问题
2. 获取话题问题
3. 获取问题详情
4. 获取问题回答
5. 分页获取所有回答
6. 数据导出
7. 数据分析
8. 完整工作流

## 📊 数据分析报告

数据分析模块会生成以下报告：

### 问题分析
- 📈 数据概览（总问题数、总回答数、总关注数、总浏览量）
- 🔥 热门问题排行（按回答数）
- ⭐ 最受关注问题（按关注数）
- 👀 最热门问题（按浏览量）
- 👤 活跃作者排行

### 回答分析
- 📈 数据概览（总回答数、总点赞数、总评论数、平均值）
- 👍 最受欢迎回答（按点赞数）
- 💬 最活跃讨论（按评论数）
- 👤 活跃作者排行

## ⚠️ 注意事项

1. **请求频率**：为避免被封禁，已添加随机延迟（1-3秒），建议不要频繁请求
2. **登录限制**：部分内容可能需要登录才能访问
3. **数据准确性**：知乎可能更改API结构，如遇问题请检查API接口
4. **合法使用**：请遵守知乎的robots.txt和使用条款
5. **数据量限制**：获取大量数据时注意控制频率和数量

## 🛡️ 反爬策略

项目已实现以下反爬策略：

- ✅ 随机 User-Agent 轮换
- ✅ 请求延迟（模拟人类行为）
- ✅ 完整的 HTTP 请求头
- ✅ 请求失败重试机制
- ✅ 错误处理和日志记录

## 📝 输出格式

### JSON 格式

```json
{
  "question_id": "27446676",
  "title": "问题标题",
  "author": "作者名",
  "answer_count": 100,
  "follower_count": 1000,
  "visited_count": 10000,
  "created_time": "2024-01-01 12:00:00",
  "url": "https://www.zhihu.com/question/27446676"
}
```

### CSV 格式

| question_id | title | author | answer_count | follower_count | visited_count | created_time | url |
|------------|-------|--------|-------------|---------------|----------------|--------------|-----|
| 27446676 | 问题标题 | 作者名 | 100 | 1000 | 10000 | 2024-01-01 12:00:00 | https://www.zhihu.com/question/27446676 |

## 🔌 扩展功能

### 使用代理

```python
scraper = ZhihuScraper()
scraper.set_proxy("http://proxy.example.com:8080")
```

### 获取特定排序的回答

```python
# 按点赞排序
answers = scraper.get_question_answers(question_id, sort='voteup')

# 按时间排序
answers = scraper.get_question_answers(question_id, sort='created')
```

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## ⚡ 性能优化建议

1. 对于大量数据获取，建议分批次进行
2. 使用代理IP池提高稳定性
3. 合理设置延迟时间，平衡速度和安全性
4. 定期清理已导出的数据文件

## 📞 联系方式

如有问题或建议，欢迎提 Issue。

---

**注意**：本项目仅供学习交流使用，请勿用于商业用途或违反知乎服务条款的行为。
