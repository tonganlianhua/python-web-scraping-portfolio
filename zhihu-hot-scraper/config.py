"""
配置文件
可根据需要修改这些参数
"""

# 网络配置
REQUEST_TIMEOUT = 10  # 请求超时时间（秒）
MAX_RETRIES = 3  # 最大重试次数
RANDOM_DELAY_MIN = 0.5  # 最小随机延时（秒）
RANDOM_DELAY_MAX = 2.0  # 最大随机延时（秒）

# 爬虫配置
DEFAULT_KEYWORD = None  # 默认过滤关键词
TOP_N_DEFAULT = 10  # 默认显示前N个话题

# 导出配置
OUTPUT_DIR = "output"  # 输出目录
EXPORT_SHEET_NAME = "知乎热榜"  # Excel工作表名称

# 图表配置
CHART_DPI = 300  # 图表分辨率
CHART_FIGSIZE = (14, 8)  # 图表大小（宽，高）
CHART_TOPICS_TO_SHOW = 10  # 趋势图显示的话题数量

# 用户-Agent列表
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

# 请求头配置
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# 字体配置
FONTS = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
