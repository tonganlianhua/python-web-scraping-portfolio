# 安装指南

## 系统要求

- Python 3.7 或更高版本
- pip 包管理器
- 互联网连接

## 安装步骤

### 1. 克隆或下载项目

```bash
cd D:\openclaw\workspace\projects\zhihu-hot-scraper
```

### 2. 创建虚拟环境（推荐）

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 验证安装

```bash
python -c "import requests, bs4, pandas, matplotlib; print('所有依赖安装成功！')"
```

## 快速测试

运行快速入门脚本验证安装：

```bash
python quick_start.py
```

## 常见问题

### Q: pip 安装速度慢？

A: 使用国内镜像源加速：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: matplotlib 中文显示乱码？

A: 确保系统已安装中文字体（如 SimHei、微软雅黑等）

### Q: requests 安装失败？

A: 尝试升级 pip：

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 依赖包说明

| 包名 | 版本 | 用途 |
|------|------|------|
| requests | 2.31.0 | HTTP 请求 |
| beautifulsoup4 | 4.12.2 | HTML 解析 |
| lxml | 4.9.3 | XML/HTML 解析器 |
| pandas | 2.0.3 | 数据处理 |
| openpyxl | 3.1.2 | Excel 读写 |
| matplotlib | 3.7.2 | 图表绘制 |
| numpy | 1.24.3 | 数值计算 |

## 开发环境设置

如需进行开发，建议安装额外的开发工具：

```bash
pip install black pytest pylint mypy
```

## 更新依赖

更新到最新版本：

```bash
pip install --upgrade -r requirements.txt
```

## 卸载

如需卸载项目依赖：

```bash
pip uninstall -r requirements.txt -y
```

---

安装完成后，请查看 README.md 了解使用方法。
