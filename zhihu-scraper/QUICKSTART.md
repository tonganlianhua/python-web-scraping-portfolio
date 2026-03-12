# 快速入门指南

## 第一步：安装依赖

```bash
cd D:\openclaw\workspace\projects\zhihu-scraper
pip install -r requirements.txt
```

## 第二步：运行测试

```bash
python test.py
```

## 第三步：运行演示

```bash
python demo.py
```

## 使用示例

### 1. 搜索问题

```bash
python main.py search "Python编程" --limit 5 --export
```

### 2. 获取问题详情

```bash
python main.py detail 27446676 --export
```

### 3. 获取回答

```bash
# 获取前20个回答
python main.py answers 27446676 --limit 20 --export

# 获取所有回答（最多100个）
python main.py answers 27446676 --all --limit 100 --export --analyze
```

### 4. 按话题获取问题

```bash
# 列出所有可用话题
python main.py list-topics

# 获取技术话题的热门问题
python main.py topic 技术 --limit 10 --export
```

## Python代码示例

### 简单示例

```python
from zhihu_scraper import ZhihuScraper

scraper = ZhihuScraper()

# 搜索问题
questions = scraper.search_questions("人工智能", limit=5)
for q in questions:
    print(q['title'])

scraper.close()
```

### 完整示例

```python
from zhihu_scraper import ZhihuScraper
from data_exporter import DataExporter
from analyzer import DataAnalyzer

scraper = ZhihuScraper()
analyzer = DataAnalyzer()
exporter = DataExporter()

# 1. 搜索问题
questions = scraper.search_questions("Python", limit=3)

if questions:
    # 2. 获取问题详情
    question_id = questions[0]['question_id']
    detail = scraper.get_question_detail(question_id)
    print(f"问题: {detail['title']}")

    # 3. 获取回答
    answers = scraper.get_all_answers(question_id, max_answers=50)

    # 4. 分析数据
    report = analyzer.generate_comparison_report(detail, answers)

    # 5. 导出数据
    exporter.export_questions([detail])
    exporter.export_answers(answers, question_id)

scraper.close()
```

## 常见问题

### Q: 如何获取问题ID？
A: 通过搜索功能获取，或者从知乎URL中提取（如 https://www.zhihu.com/question/27446676）

### Q: 可以抓取所有回答吗？
A: 可以，但建议限制数量（如 `max_answers=100`）以避免请求过多

### Q: 数据保存在哪里？
A: 默认保存在 `output/` 目录下

### Q: 如何使用代理？
A: 在代码中调用 `scraper.set_proxy("http://proxy:port")`

### Q: 遇到403错误怎么办？
A: 可能被反爬，建议增加延迟时间或更换代理
