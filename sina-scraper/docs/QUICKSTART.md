# 快速开始指南

本指南将帮助你快速上手新浪微博爬虫。

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

## 2. 运行演示脚本

演示脚本展示了所有主要功能：

```bash
python examples/demo.py
```

这将生成以下示例数据：
- 用户数据 (CSV/JSON)
- 微博帖子数据 (CSV/JSON)
- 分析报告
- 可视化图表

所有数据保存在 `data/` 目录。

## 3. 运行单元测试

验证所有功能正常工作：

```bash
python tests/test_scraper.py
```

## 4. 使用命令行工具

项目提供了命令行接口：

```bash
# 显示帮助
python main.py --help

# 运行演示
python main.py demo

# 获取热搜（无需Cookie）
python main.py hot --count 20

# 获取用户信息（需要Cookie）
python main.py user user_id --cookie your_cookie_here

# 搜索微博（需要Cookie）
python main.py search 关键词 --max-results 20 --cookie your_cookie_here
```

## 5. 使用Python API

### 基本示例

```python
from src.api import WeiboAPI
from src.exporter import DataExporter
from src.analyzer import DataAnalyzer

# 初始化API（需要Cookie才能访问大部分功能）
api = WeiboAPI(cookie='your_we_weibo_cookie')

# 获取热搜话题（无需Cookie）
hot_topics = api.get_hot_topics()
print(f"当前热搜: {hot_topics[:10]}")

# 导出数据
exporter = DataExporter('data')
exporter.export_to_json(hot_topics, 'hot_topics')

api.close()
```

### 完整示例

```python
from src.api import WeiboAPI
from src.exporter import DataExporter
from src.analyzer import DataAnalyzer
import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 初始化
api = WeiboAPI(cookie='your_cookie_here')
exporter = DataExporter('data')
analyzer = DataAnalyzer('data')

# 1. 获取用户信息
user = api.get_user_info('user_id_or_name')
print(f"用户: {user.username}, 粉丝: {user.fans_count:,}")

# 2. 搜索微博
posts = api.search_posts('人工智能', max_results=20)
print(f"找到 {len(posts)} 条微博")

# 3. 导出数据
exporter.export_users([user], 'my_user', 'json')
exporter.export_posts(posts, 'ai_posts', 'csv')

# 4. 数据分析
report = analyzer.generate_report([user], posts, 'my_report')
print(f"分析报告: {report}")

# 5. 生成图表
fans_chart = analyzer.plot_user_fans([user])
interaction_chart = analyzer.plot_post_interaction(posts)

# 关闭连接
api.close()
```

## 6. 获取Cookie

大部分微博功能需要登录Cookie。获取步骤：

1. 浏览器登录 https://weibo.com
2. 按F12打开开发者工具
3. 进入 Network 标签
4. 刷新页面
5. 找到任意请求
6. 复制请求头中的 Cookie

## 7. 数据导出格式

### CSV格式
- 使用UTF-8-BOM编码，Excel可直接打开
- 适合Excel分析和共享

### JSON格式
- 结构化数据
- 适合程序处理和复杂数据

## 8. 常见问题

### Q: 为什么无法获取数据？
A: 大部分功能需要登录Cookie。请提供有效的Cookie。

### Q: 如何提高爬取速度？
A: 内置了2-5秒随机延时以防被封。不建议调整。

### Q: 图表显示乱码？
A: 确保系统安装了中文字体（SimHei、Microsoft YaHei）。

### Q: 如何处理大量数据？
A: 使用分页获取，多次调用API，注意控制频率。

## 9. 项目结构

```
sina-scraper/
├── src/                 # 源代码
│   ├── scraper.py      # 爬虫基础类
│   ├── user.py         # 用户信息类
│   ├── weibo.py        # 微博帖子类
│   ├── api.py          # API接口
│   ├── exporter.py     # 数据导出
│   └── analyzer.py     # 数据分析
├── examples/            # 示例脚本
│   └── demo.py         # 功能演示
├── tests/               # 测试脚本
│   └── test_scraper.py # 单元测试
├── data/                # 数据输出（自动创建）
├── main.py             # 命令行入口
└── README.md           # 完整文档
```

## 10. 下一步

- 阅读完整文档: `README.md`
- 查看演示代码: `examples/demo.py`
- 运行单元测试: `tests/test_scraper.py`
- 根据需求修改和扩展功能

## 注意事项

1. **仅用于学习研究**，不得用于商业用途
2. **遵守服务条款**，尊重网站规则
3. **控制访问频率**，避免给服务器造成压力
4. **保护隐私数据**，不要泄露Cookie和个人信息

## 技术支持

如有问题，请：
1. 检查日志输出
2. 查看文档和示例代码
3. 运行单元测试排查问题

---

祝使用愉快！
