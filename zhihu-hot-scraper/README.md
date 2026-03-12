# 知乎热榜爬虫 (Zhihu Hot Scraper)

一个功能完整的知乎热榜爬虫项目，支持实时获取热榜话题、关键词过滤、话题详情获取、热度对比、Excel导出和趋势分析。

## ✨ 功能特性

- ✅ **实时获取热榜** - 获取当前知乎热榜前50个话题
- ✅ **关键词过滤** - 根据关键词筛选相关话题
- ✅ **话题详情** - 获取回答数、关注数、浏览量、标签等详细信息
- ✅ **热度对比** - 支持多次采集，对比热度变化
- ✅ **Excel导出** - 将数据导出为格式化的Excel文件
- ✅ **趋势分析** - 生成热度趋势图和变化对比图
- ✅ **反爬策略** - 随机延时、User-Agent轮换、请求失败重试
- ✅ **完整文档** - 包含详细的README和演示脚本
- ✅ **测试覆盖** - 包含完整的单元测试

## 📋 项目结构

```
zhihu-hot-scraper/
├── README.md                 # 项目文档
├── requirements.txt          # 依赖包列表
├── zhihu_scraper.py         # 核心爬虫模块
├── data_exporter.py         # 数据导出和分析模块
├── demo.py                   # 演示脚本
├── test_scraper.py           # 测试脚本
└── output/                   # 输出目录（自动创建）
    ├── zhihu_hot_*.xlsx      # 热榜Excel
    ├── zhihu_comparison_*.xlsx  # 对比数据Excel
    ├── zhihu_details_*.xlsx   # 详情数据Excel
    ├── zhihu_trend_*.png      # 趋势图
    └── zhihu_comparison_chart_*.png  # 对比图
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

依赖包包括：
- requests - HTTP请求库
- beautifulsoup4 - HTML解析库
- lxml - XML/HTML解析器
- pandas - 数据处理库
-` openpyxl - Excel读写库
- matplotlib - 图表绘制库
- numpy - 数值计算库

### 2. 运行演示脚本

```bash
python demo.py
```

演示脚本提供以下选项：
1. 基本获取热榜
2. 关键词过滤
3. 获取话题详情
4. 导出Excel
5. 对比热度变化
6. 多次采集并生成趋势图
7. 完整工作流

### 3. 运行测试

```bash
python test_scraper.py
```

## 📖 使用说明

### 基本使用

```python
from zhihu_scraper import ZhihuHotScraper
from data_exporter import DataExporter

# 创建爬虫实例
scraper = ZhihuHotScraper()

# 获取热榜
hot_list = scraper.get_hot_list()

# 打印热榜
for item in hot_list[:10]:
    print(f"排名: {item['rank']}")
    print(f"标题: {item['title']}")
    print(f"热度: {item['hot_value']}")
    print(f"链接: {item['link']}")
    print(f"摘要: {item['excerpt']}")
    print("-" * 40)
```

### 关键词过滤

```python
# 获取包含"科技"关键词的话题
tech_list = scraper.get_hot_list(keyword="科技")

for item in tech_list:
    print(f"{item['title']} - 热度: {item['hot_value']}")
```

### 获取话题详情

```python
# 获取话题详情
detail = scraper.get_topic_detail("https://www.zhihu.com/question/xxxxx")

print(f"回答数: {detail['answer_count']}")
print(f"关注数: {detail['follower_count']}")
print(f"浏览量: {detail['view_count']}")
print(f"标签: {', '.join(detail['tags'])}")
```

### 导出Excel

```python
# 创建导出器
exporter = DataExporter()

# 导出热榜到Excel
filepath = exporter.export_to_excel(hot_list, filename="my_hot_list")
print(f"已导出到: {filepath}")
```

### 对比热度变化

```python
import time

# 第一次采集
hot_list_1 = scraper.get_hot_list()

# 等待一段时间
time.sleep(300)  # 5分钟

# 第二次采集
hot_list_2 = scraper.get_hot_list()

# 对比热度变化
comparison = scraper.compare_hot_values(hot_list_1, hot_list_2)

# 导出对比结果
exporter.export_comparison_to_excel(comparison)
exporter.generate_comparison_chart(comparison)

# 查看变化最大的话题
for item in comparison[:10]:
    if item['change'] > 0:
        print(f"↑ {item['title']}: +{item['change']:.0f}")
    else:
        print(f"↓ {item['title']}: {item['change']:.0f}")
```

### 多次采集和趋势分析

```python
hot_history = []
collection_times = 5  # 采集5次

for i in range(collection_times):
    hot_list = scraper.get_hot_list()
    hot_history.append(hot_list)
    
    if i < collection_times - 1:
        time.sleep(600)  # 10分钟后再采集

# 生成趋势图
exporter.generate_trend_chart(hot_history, top_n=10)
```

## 🎯 API参考

### ZhihuHotScraper 类

#### `__init__()`
初始化爬虫实例

#### `get_hot_list(keyword=None)`
获取知乎热榜话题列表

**参数:**
- `keyword` (str, optional): 关键词过滤

**返回:**
- `List[Dict]`: 热榜话题列表，每个话题包含：
  - `rank` (int): 排名
  - `title` (str): 标题
  - `hot_value` (float): 热度值
  - `link` (str): 链接
  - `excerpt` (str): 摘要
  - `created_time` (str): 采集时间

#### `get_topic_detail(question_url)`
获取话题详情

**参数:**
- `question_url` (str): 问题URL

**返回:**
- `Dict`: 话题详情字典，包含：
  - `url` (str): URL
  - `answer_count` (int): 回答数
  - `follower_count` (int): 关注数
  - `view_count` (int): 浏览量
  - `tags` (List[str]): 标签列表

#### `compare_hot_values(hot_list_1, hot_list_2)`
对比两次采集的热度变化

**参数:**
- `hot_list_1` (List[Dict]): 第一次采集的热榜
- `hot_list_2` (List[Dict]): 第二次采集的热榜

**返回:**
- `List[Dict]`: 热度变化列表，每个条目包含：
  - `title` (str): 标题
  - `hot_value_1` (float): 第一次热度值
  - `hot_value_2` (float): 第二次热度值
  - `change` (float): 热度变化值
  - `change_percent` (float): 变化百分比
  - `link` (str)`: 链接
  - `status` (str, optional): 状态（'new'或'dropped'）

### DataExporter 类

#### `__init__(output_dir="output")`
初始化导出器

**参数:**
- `output_dir` (str): 输出目录

#### `export_to_excel(hot_list, filename=None)`
导出热榜数据到Excel

**参数:**
- `hot_list` (List[Dict]): 热榜数据列表
- `filename` (str, optional): 文件名（不含扩展名）

**返回:**
- `str`: 文件路径

#### `export_comparison_to_excel(comparison, filename=None)`
导出热度对比数据到Excel

**参数:**
- `comparison` (List[Dict]): 对比数据列表
- `filename` (str, optional): 文件名（不含扩展名）

**返回:**
- `str`: 文件路径

#### `export_detail_to_excel(details, filename=None)`
导出话题详情到Excel

**参数:**
- `details` (List[Dict]): 详情数据列表
- `filename` (str, optional): 文件名（不含扩展名）

**返回:**
- `str`: 文件路径

#### `generate_trend_chart(hot_history, filename=None, top_n=10)`
生成热度趋势图

**参数:**
- `hot_history` (List[List[Dict]]): 历史热榜数据列表
- `filename` (str, optional): 文件名（不含扩展名）
- `top_n` (int): 显示前N个话题

**返回:**
- `str`: 图片路径

#### `generate_comparison_chart(comparison, filename=None, top_n=15)`
生成热度变化对比图

**参数:**
- `comparison` (List[Dict]): 对比数据列表
- `filename` (str, optional): 文件名（不含扩展名）
- `top_n` (int): 显示变化最大的N个话题

**返回:**
- `str`: 图片路径

## 🛡️ 反爬策略

本项目实现了多种反爬策略：

1. **User-Agent轮换** - 内置5个常见User-Agent，随机轮换使用
2. **随机延时** - 每次请求前随机延时0.5-2秒
3. **失败重试** - 请求失败时自动重试，最多3次
4. **限流处理** - 检测到429状态码时自动增加等待时间
5. **Session复用** - 使用requests.Session复用连接

## ⚠️ 注意事项

1. **请求频率** - 请合理设置采集间隔，避免对知乎服务器造成压力
2. **数据来源** - 本项目仅供学习研究使用，请遵守知乎的使用条款
3. **网络环境** - 需要稳定的网络连接才能正常使用
4. **数据时效性** - 热榜数据实时变化，采集时间很重要
5. **编码问题** - Excel文件使用UTF-8编码，可正确显示中文

## 🐛 常见问题

### Q: 获取热榜失败怎么办？

A: 可能的原因：
- 网络连接问题
- 知乎服务器暂时不可用
`- 被反爬机制限制

建议：
- 检查网络连接
- 增加延时时间
- 等待一段时间后重试

### Q: 获取的话题详情为空？

A: 可能的原因：
- 话题URL格式不正确
- 话题已被删除或私密
- 解析逻辑需要更新

### Q: 导出的Excel文件打开显示乱码？

A: 使用支持UTF-8的软件打开（如Microsoft Excel 2016+、WPS等）

### Q: 趋势图显示中文乱码？

A: 脚本已自动设置中文字体，如果仍有问题，请检查系统是否安装了中文字体

## 📊 示例输出

### 热榜数据示例

```
排名: 1
标题: 如何看待最近发生的xxx事件？
热度: 3256789
链接: https://www.zhihu.com/question/123456789
摘要: 该事件引发了广泛关注，各方观点不一...
```

### 热度对比示例

```
↑ 如何看待最近发生的xxx事件？: +125000
↓ 某科技公司的财报分析: -89000
[新上榜] 突发新闻：xxx发生
[已下榜] 过时的热门话题
```

## 📝 更新日志

### v1.0.0 (2026-03-12)
- ✨ 初始版本发布
- ✅ 实现核心爬虫功能
- ✅ 支持Excel导出
- ✅ 支持热度对比
- ✅ 生成趋势分析图
- ✅ 添加反爬策略
- ✅ 完整的测试覆盖

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

本项目仅供学习研究使用，请勿用于商业用途。

## 🙏 致谢

- 知乎提供的数据源
- requests、beautifulsoup4等开源库

---

**作者**: OpenClaw AI Assistant
**项目地址**: D:\openclaw\workspace\projects\zhihu-hot-scraper
**创建时间**: 2026-03-12
