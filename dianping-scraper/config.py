#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置文件
存放爬虫的配置参数
"""

# 请求配置
REQUEST_CONFIG = {
    'timeout': 10,          # 请求超时时间（秒）
    'max_retries': 3,       # 最大重试次数
    'retry_delay': 2,       # 重试延时（秒）
}

# 延时配置
DELAY_CONFIG = {
    'min_delay': 1.0,       # 最小延时（秒）
    'max_delay': 3.0,       # 最大延时（秒）
    'page_delay_min': 2.0,  # 页面间最小延时
    'page_delay_max': 4.0,  # 页面间最大延时
}

# User-Agent 列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edge/118.0.2088',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edge/117.0.2045',
]

# 代理配置（如需使用代理，取消注释并配置）
PROXY_CONFIG = {
    'enabled': False,      # 是否启用代理
    'http': '',            # HTTP代理地址
    'https': '',           # HTTPS代理地址
}

# 导出配置
EXPORT_CONFIG = {
    'default_csv_encoding': 'utf-8-sig',  # CSV默认编码
    'default_json_indent': 2,             # JSON缩进空格数
    'output_dir': './output',             # 输出目录
}

# 图表配置
PLOT_CONFIG = {
    'dpi': 300,              # 图片DPI
    'figsize': (12, 6),      # 图片尺寸
    'font_names': ['SimHei', 'Microsoft YaHei', 'SimSun', 'KaiTi'],  # 中文字体列表
    'color_rating': 'skyblue',      # 评分图颜色
    'color_price': 'lightcoral',   # 价格图颜色
}

# 日志配置
LOG_CONFIG = {
    'enabled': True,        # 是否启用日志
    'level': 'INFO',       # 日志级别
    'file': 'scraper.log',  # 日志文件
}

# 常用城市列表
COMMON_CITIES = [
    '北京', '上海', '广州', '深圳',
    '杭州', '成都', '重庆', '武汉',
    '西安', '南京', '苏州', '天津'
]

# 常用搜索关键词
COMMON_KEYWORDS = [
    '美食', '火锅', '日料', '川菜',
    '酒店', '咖啡馆', 'KTV', '电影院',
    '健身房', '美容院', '理发店'
]
