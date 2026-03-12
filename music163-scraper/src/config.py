"""
网易云音乐爬虫配置文件
"""

import random
import time

# 基础配置
BASE_URL = "https://music.163.com"
API_BASE_URL = "https://music.163.com/api"

# User-Agent 池（随机轮换以避免被识别为爬虫）
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

# 请求头模板
DEFAULT_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": BASE_URL,
}

# 热门榜单ID
TOP_LISTS = {
    "hot": "37786280",       # 热歌榜
    "new": "3779629",        # 新歌榜
    "original": "2884035",   # 原创榜
    "soar": "1972375675",    # 飙升榜
    "recommend": "3733003",  # 推荐榜
}

# 反爬配置
MIN_DELAY = 1.0     # 最小延时（秒）
MAX_DELAY = 3.0     # 最大延时（秒）
MAX_RETRIES = 3     # 最大重试次数
RETRY_DELAY = 5.0   # 重试延时（秒）

# 数据导出配置
EXPORT_DIR = "../data"
DEFAULT_ENCODING = "utf-8-sig"  # UTF-8 with BOM，确保Excel能正确打开

# 分析报告配置
WORDCLOUD_MAX_WORDS = 100
TOP_N_ARTISTS = 20
TOP_N_SONGS = 50


def get_random_user_agent():
    """随机获取一个User-Agent"""
    return random.choice(USER_AGENTS)


def random_delay():
    """随机延时，避免请求过于频繁"""
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    time.sleep(delay)
    return delay


def get_headers():
    """获取带有随机User-Agent的请求头"""
    headers = DEFAULT_HEADERS.copy()
    headers["User-Agent"] = get_random_user_agent()
    return headers
