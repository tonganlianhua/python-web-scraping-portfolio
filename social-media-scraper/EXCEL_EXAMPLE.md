# Excel文件说明

## 文件结构

导出的Excel文件包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| 排名 | 热搜排名（1-50） | 1, 2, 3 |
| 标题 | 热搜话题标题 | "某某明星宣布结婚" |
| 热度值 | 讨论热度 | "1234567" 或 "123万" |
| 链接 | 微博搜索链接 | https://s.weibo.com/weibo?q=xxx |

## 数据示例

```
排名    标题                    热度值      链接
1       热门话题示例一          2345678     https://s.weibo.com/weibo?q=%E8%AF%9D%E9%A2%98%E4%B8%80
2       热门话题示例二          1987654     https://s.weibo.com/weibo?q=%E8%AF%9D%E9%A2%98%E4%BA%8C
3       热门话题示例三          1654321     https://s.weibo.com/weibo?q=%E8%AF%9D%E9%A2%98%E4%B8%89
```

## 使用方法

### 方法1：直接用Excel打开

1. 双击Excel文件
2. 查看数据
3. 使用Excel的筛选、排序、图表功能分析数据

### 方法2：用Python读取

```python
import pandas as pd

# 读取Excel
df = pd.read_excel('weibo_hot_search_20260311_225500.xlsx')

# 查看前5条
print(df.head())

# 筛选特定话题
economy_data = df[df['标题'].str.contains('经济')]

# 按热度排序
df_sorted = df.sort_values('热度值', ascending=False)
```

### 方法3：用示例分析脚本

```bash
python example_usage.py
```

该脚本会自动：
- 读取最新的Excel文件
- 显示数据统计信息
- 生成可视化图表（可选）

## 数据分析示例

### 1. 统计热搜数量

```python
import pandas as pd
df = pd.read_excel('weibo_hot_search.xlsx')
print(f"总共 {len(df)} 条热搜")
```

### 2. 查找特定关键词

```python
# 查找包含"游戏"的热搜
game_data = df[df['标题'].str.contains('游戏')]
print(game_data)
```

### 3. 排名对比

```python
# 查看Top 10
top10 = df.head(10)
print(top10)
```

### 4. 导出CSV

```python
# 转换为CSV格式
df.to_csv('hot_search.csv', index=False, encoding='utf-8-sig')
```

## 注意事项

1. **编码问题**: 在Windows上用Excel打开中文CSV时，建议使用utf-8-sig编码
2. **数值格式**: 热度值可能是字符串格式，需要转换为数值进行计算
3. **链接使用**: 点击链接可以跳转到微博搜索页面查看详细内容
4. **数据时效**: 微博热搜实时更新，建议定期获取最新数据

## 高级分析

### 时间趋势分析

如果定期保存Excel文件，可以分析热搜趋势：

```python
import glob
import pandas as pd

# 读取所有历史文件
files = glob.glob('weibo_hot_search_*.xlsx')
all_data = []

for file in sorted(files):
    df = pd.read_excel(file)
    df['日期'] = file.replace('weibo_hot_search_', '').replace('.xlsx', '')
    all_data.append(df)

# 合并所有数据
df_all = pd.concat(all_data)

# 分析特定话题的热度变化
```

### 热度值转换

将"123万"格式转换为数值：

```python
def parse_hot_value(val):
    if '万' in str(val):
        return float(str(val).replace('万', '')) * 10000
    return float(str(val).replace(',', ''))

df['热度值_数值'] = df['热度值'].apply(parse_hot_value)
```

## 可视化建议

可以使用以下库创建图表：

- **matplotlib** - 基础图表
- **seaborn** - 统计图表
- **plotly** - 交互式图表

示例参见 `example_usage.py` 文件。
