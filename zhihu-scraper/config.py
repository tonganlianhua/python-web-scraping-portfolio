# -*- coding: utf-8 -*-
"""
知乎爬虫配置文件
"""

import random
import time

# 随机用户代理列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
]

# 请求头
DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# 延迟配置
MIN_DELAY = 1.0  # 最小延迟秒数
MAX_DELAY = 3.0  # 最大延迟秒数

# 知乎API配置
ZHIHU_BASE_URL = 'https://www.zhihu.com'
ZHIHU_API_URL = 'https://www.zhihu.com/api/v4'

# 分页配置
DEFAULT_PAGE_SIZE = 20
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30

# 输出配置
OUTPUT_DIR = 'output'
DATA_DIR = 'data'


def get_random_user_agent():
    """获取随机User-Agent"""
    return random.choice(USER_AGENTS)


def random_delay():
    """随机延迟，模拟人类行为"""
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    time.sleep(delay)
    return delay


def get_headers():
    """获取完整的请求头"""
    headers = DEFAULT_HEADERS.copy()
    headers['User-Agent'] = get_random_user_agent()
    return headers
