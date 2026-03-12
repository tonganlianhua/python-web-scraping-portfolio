"""
配置文件
用于设置爬虫参数和路径
"""

import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据输出目录
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 请求配置
DEFAULT_TIMEOUT = 30  # 请求超时（秒）
DEFAULT_RETRY = 3  # 重试次数
MIN_DELAY = 2.0  # 最小延时（秒）
MAX_DELAY = 5.0  # 最大延时（秒）

# 默认导出格式
DEFAULT_EXPORT_FORMAT = 'json'

# 分析配置
TOP_USERS_COUNT = 20  # 用户排行榜显示数量
TOP_POSTS_COUNT = 20  # 热门帖子显示数量
TOP_TOPICS_COUNT = 20  # 热门话题显示数量

# 图表配置
CHART_DPI = 300  # 图表DPI
CHART_FIGSIZE_USERS = (12, 8)  # 用户图表大小
CHART_FIGSIZE_POSTS = (18, 5)  # 帖子图表大小

# 微博配置
WEIBO_BASE_URL = 'https://weibo.com'
WEIBO_API_BASE = 'https://weibo.com/ajax'

# 创建数据目录
os.makedirs(DATA_DIR, exist_ok=True)
