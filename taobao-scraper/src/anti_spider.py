"""
反爬策略模块
提供随机延时、User-Agent轮换、Session管理等反爬功能
"""

import random
import time
from typing import List, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class AntiSpiderMiddleware:
    """反爬中间件类"""

    # 常见 User-Agent 列表
    USER_AGENTS = [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        # Firefox
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
        # Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        # Safari
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    ]

    def __init__(
        self,
        delay_range: tuple = (1, 3),
        max_retries: int = 3,
        retry_delay: float = 2.0,
        timeout: int = 30
    ):
        """
        初始化反爬中间件

        Args:
            delay_range: 随机延时范围（秒），默认 (1, 3)
            max_retries: 最大重试次数，默认 3
            retry_delay: 重试延迟（秒），默认 2.0
            timeout: 请求超时时间（秒），默认 30
        """
        self.delay_range = delay_range
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """
        创建带有重试策略的 Session

        Returns:
            requests.Session: 配置好的 Session 对象
        """
        session = requests.Session()

        # 配置重试策略
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=10
        )

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def get_random_user_agent(self) -> str:
        """
        获取随机 User-Agent

        Returns:
            str: 随机 User-Agent 字符串
        """
        return random.choice(self.USER_AGENTS)

    def random_delay(self, min_delay: Optional[float] = None, max_delay: Optional[float] = None) -> None:
        """
        随机延迟

        Args:
            min_delay: 最小延迟时间（秒），如果为 None 则使用初始化时的延迟范围
            max_delay: 最大延迟时间（秒），如果为 None 则使用初始化时的延迟范围
        """
        if min_delay is None or max_delay is None:
            min_delay, max_delay = self.delay_range

        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def add_custom_user_agent(self, user_agent: str) -> None:
        """
        添加自定义 User-Agent

        Args:
            user_agent: User-Agent 字符串
        """
        if user_agent not in self.USER_AGENTS:
            self.USER_AGENTS.append(user_agent)

    def get_headers(self, extra_headers: Optional[dict] = None) -> dict:
        """
        获取请求头

        Args:
            extra_headers: 额外的请求头

        Returns:
            dict: 请求头字典
        """
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }

        if extra_headers:
            headers.update(extra_headers)

        return headers

    def request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> requests.Response:
        """
        发起请求（带重试和延时）

        Args:
            method: 请求方法（GET/POST）
            url: 请求 URL
            **kwargs: 其他请求参数

        Returns:
            requests.Response: 响应对象

        Raises:
            requests.RequestException: 请求失败
        """
        # 添加默认请求头
        if 'headers' not in kwargs:
            kwargs['headers'] = self.get_headers()

        # 添加默认超时
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        # 请求前随机延时
        self.random_delay()

        retries = 0
        last_error = None

        while retries < self.max_retries:
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response

            except requests.RequestException as e:
                last_error = e
                retries += 1

                if retries < self.max_retries:
                    # 重试前延迟
                    time.sleep(self.retry_delay * retries)

        raise last_error if last_error else requests.RequestException("请求失败")

    def get(self, url: str, **kwargs) -> requests.Response:
        """
        发起 GET 请求

        Args:
            url: 请求 URL
            **kwargs: 其他请求参数

        Returns:
            requests.Response: 响应对象
        """
        return self.request('GET', url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """
        发起 POST 请求

        Args:
            url: 请求 URL
            **kwargs: 其他请求参数

        Returns:
            requests.Response: 响应对象
        """
        return self.request('POST', url, **kwargs)

    def close(self) -> None:
        """
        关闭 Session
        """
        self.session.close()

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理器"""
        self.close()
