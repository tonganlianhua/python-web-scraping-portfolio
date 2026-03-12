# -*- coding: utf-8 -*-
"""
反爬虫策略模块
"""

import random
import time
from fake_useragent import UserAgent


class AntiScraping:
    """反爬虫策略类"""
    
    def __init__(self):
        self.ua = UserAgent()
        
    def get_random_user_agent(self):
        """获取随机User-Agent"""
        try:
            return self.ua.random
        except:
            # 如果fake_useragent失败，使用备用列表
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/605.1.15 Safari/605.1.15'
            ]
            return random.choice(user_agents)
    
    def get_random_delay(self, min_delay=1, max_delay=3):
        """获取随机延迟时间"""
        return random.uniform(min_delay, max_delay)
    
    def random_sleep(self, min_delay=1, max_delay=3):
        """随机休眠"""
        delay = self.get_random_delay(min_delay, max_delay)
        time.sleep(delay)
        return delay
    
    def get_headers(self, referer=None):
        """获取伪装的请求头"""
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        if referer:
            headers['Referer'] = referer
            
        return headers
    
    def get_cookies(self):
        """获取基础cookies（如果需要可以扩展）"""
        return {
            'lianjia_ssid': '',
            'sajssdk_2015_cross_new_user': '1'
        }
