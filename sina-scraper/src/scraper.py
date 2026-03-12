"""
新浪微博爬虫核心模块
提供基础的HTTP请求和反爬策略
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
from typing import Dict, Optional, List, Union
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeiboScraper:
    """新浪微博爬虫基类"""

    def __init__(self, proxy: Optional[Dict[str, str]] = None):
        """
        初始化爬虫

        Args:
            proxy: 代理设置，格式: {'http': 'http://proxy', 'https': 'https://proxy'}
        """
        self.session = requests.Session()
        self.ua = UserAgent()
        self.proxy = proxy
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(self.headers)

        # 请求计数器，用于自适应延迟
        self.request_count = 0
        self.last_request_time = 0
        self.min_delay = 2.0  # 最小延迟2秒
        self.max_delay = 5.0  # 最大延迟5秒

    def _random_delay(self):
        """随机延时，反爬策略"""
        delay = random.uniform(self.min_delay, self.max_delay)
        logger.debug(f"Delaying for {delay:.2f} seconds...")
        time.sleep(delay)

    def _get_user_agent(self) -> str:
        """获取随机User-Agent"""
        try:
            return self.ua.random
        except:
            # 如果fake-useragent失败，使用备用UA列表
            uas = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            ]
            return random.choice(uas)

    def _update_headers(self):
        """更新请求头，轮换User-Agent"""
        self.session.headers['User-Agent'] = self._get_user_agent()

    def request(
        self,
        url: str,
        method: str = 'GET',
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: int = 30,
        retry: int = 3,
        **kwargs
    ) -> Optional[requests.Response]:
        """
        发送HTTP请求（内置反爬策略）

        Args:
            url: 请求URL
            method: 请求方法 (GET/POST)
            params: URL参数
            data: POST数据
            headers: 额外请求头
            timeout: 超时时间（秒）
            retry: 重试次数
            **kwargs: 其他requests参数

        Returns:
            requests.Response对象或None
        """
        self._update_headers()
        if headers:
            self.session.headers.update(headers)

        # 自适应延迟
        if self.last_request_time > 0:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.min_delay:
                self._random_delay()

        for attempt in range(retry):
            try:
                if method.upper() == 'GET':
                    response = self.session.get(
                        url,
                        params=params,
                        proxies=self.proxy,
                        timeout=timeout,
                        **kwargs
                    )
                elif method.upper() == 'POST':
                    response = self.session.post(
                        url,
                        params=params,
                        data=data,
                        proxies=self.proxy,
                        timeout=timeout,
                        **kwargs
                    )
                else:
                    raise ValueError(f"Unsupported method: {method}")

                # 检查响应状态
                response.raise_for_status()

                # 更新请求计数和时间
                self.request_count += 1
                self.last_request_time = time.time()

                logger.info(f"Request {self.request_count}: {url} - Status: {response.status_code}")
                return response

            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1}/{retry} failed: {e}")
                if attempt < retry - 1:
                    delay = (attempt + 1) * 2  # 指数退避
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"All {retry} attempts failed: {e}")
                    return None

        return None

    def get_soup(
        self,
        url: str,
        method: str = 'GET',
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        **kwargs
    ) -> Optional[BeautifulSoup]:
        """
        获取BeautifulSoup对象

        Args:
            url: 请求URL
            method: 请求方法
            params: URL参数
            data: POST数据
            **kwargs: 其他request参数

        Returns:
            BeautifulSoup对象或None
        """
        response = self.request(url, method, params, data, **kwargs)
        if response:
            try:
                soup = BeautifulSoup(response.text, 'lxml')
                return soup
            except Exception as e:
                logger.error(f"Failed to parse HTML: {e}")
                return None
        return None

    def close(self):
        """关闭Session"""
        self.session.close()
        logger.info("Session closed")

    def __enter__(self):
        """支持with语句"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时自动关闭Session"""
        self.close()
