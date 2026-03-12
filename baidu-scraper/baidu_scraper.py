#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
百度百科爬虫
支持词条搜索、内容获取、分类筛选、数据导出和分析
"""

import requests
from bs4 import BeautifulSoup
import random
import time
from urllib.parse import quote
import re
from typing import Dict, List, Optional, Set


class BaiduBaikeSpider:
    """百度百科爬虫类"""
    
    def __init__(self):
        """初始化爬虫"""
        self.base_url = "https://baike.baidu.com"
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        ]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.cached_entries: Dict[str, Dict] = {}
        
    def _get_random_delay(self, min_delay: float = 1.0, max_delay: float = 3.0) -> None:
        """随机延时"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def _update_headers(self) -> Dict:
        """更新请求头"""
        headers = self.headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        return headers
        
    def _make_request(self, url: str, retry_count: int = 3) -> Optional[BeautifulSoup]:
        """发送HTTP请求"""
        for attempt in range(retry_count):
            try:
                self._get_random_delay()
                response = self.session.get(
                    url,
                    headers=self._update_headers(),
                    timeout=30
                )
                response.raise_for_status()
                response.encoding = 'utf-8'
                return BeautifulSoup(response.text, 'html.parser')
            except requests.RequestException as e:
                print(f"请求失败 (尝试 {attempt + 1}/{retry_count}): {e}")
                if attempt < retry_count - 1:
                    self._get_random_delay(2, 5)
                continue
        return None
        
    def search_entries(self, keyword: str, limit: int = 10) -> List[Dict]:
        """搜索百科词条"""
        search_url = f"{self.base_url}/item/{quote(keyword)}"
        print(f"正在搜索: {keyword}")
        
        soup = self._make_request(search_url)
        if not soup:
            print(f"搜索失败: {keyword}")
            return []
            
        # 尝试直接获取词条
        entry = self._parse_entry_page(soup, keyword)
        if entry:
            print(f"找到词条: {entry['title']}")
            return [entry]
            
        # 尝试获取搜索结果列表
        results = []
        # 这里简化处理，实际百度百科搜索页面可能需要更复杂的解析
        return results
        
    def get_entry(self, title: str) -> Optional[Dict]:
        """获取词条完整信息"""
        # 检查缓存
        if title in self.cached_entries:
            return self.cached_entries[title]
            
        url = f"{self.base_url}/item/{quote(title)}"
        print(f"正在获取词条: {title}")
        
        soup = self._make_request(url)
        if not soup:
            print(f"获取词条失败: {title}")
            return None
            
        entry = self._parse_entry_page(soup, title)
        if entry:
            self.cached_entries[title] = entry
            return entry
        return None
        
    def _parse_entry_page(self, soup: BeautifulSoup, title: str) -> Optional[Dict]:
        """解析词条页面"""
        entry = {
            'title': title,
            'url': f"{self.base_url}/item/{quote(title)}",
            'summary': '',
            'intro': '',
            'categories': [],
            'content': '',
            'edit_count': 0,
            'views': 0,
            'labels': []
        }
        
        # 提取标题
        title_tag = soup.find('h1', class_='title-text')
        if title_tag:
            entry['title'] = title_tag.get_text(strip=True)
            
        # 提取摘要
        summary_tag = soup.find('div', class_='lemma-summary')
        if summary_tag:
            summary_div = summary_tag.find('div', class_='para')
            if summary_div:
                entry['summary'] = summary_div.get_text(strip=True)
                
        # 提取简介（第一个段落）
        para_tags = soup.find_all('div', class_='para')
        if para_tags:
            entry['intro'] = para_tags[0].get_text(strip=True)
            
        # 提取分类
        cat_tags = soup.find_all('span', class_='tag')
        entry['categories'] = [tag.get_text(strip=True) for tag in cat_tags]
        
        # 提取完整内容
        content_div = soup.find('div', class_='main-content')
        if content_div:
            paragraphs = content_div.find_all('div', class_='para')
            entry['content'] = '\n'.join([p.get_text(strip=True) for p in paragraphs])
            
        # 提取编辑次数
        edit_info = soup.find('div', class_='lemma-statistics')
        if edit_info:
            edit_text = edit_info.get_text()
            edit_match = re.search(r'编辑：(\d+)', edit_text)
            if edit_match:
                entry['edit_count'] = int(edit_match.group(1))
                
            # 提取浏览次数
            view_match = re.search(r'浏览：(\d+)', edit_text)
            if view_match:
                entry['views'] = int(view_match.group(1))
                
        # 提取标签
        label_tags = soup.find_all('a', class_='catalog-link')
        entry['labels'] = [tag.get_text(strip=True) for tag in label_tags]
        
        return entry
        
    def batch_get_entries(self, titles: List[str]) -> List[Dict]:
        """批量获取词条"""
        entries = []
        for title in titles:
            entry = self.get_entry(title)
            if entry:
                entries.append(entry)
            self._get_random_delay(1.5, 3.0)
        return entries
        
    def filter_by_category(self, entries: List[Dict], categories: List[str]) -> List[Dict]:
        """按分类筛选词条"""
        filtered = []
        for entry in entries:
            entry_cats = [cat.lower() for cat in entry['categories']]
            if any(cat.lower() in entry_cats for cat in categories):
                filtered.append(entry)
        return filtered
        
    def get_hot_entries(self, limit: int = 10) -> List[Dict]:
        """获取热门词条"""
        # 这里简化处理，实际需要访问百度百科热门榜单页面
        popular_titles = [
            '人工智能', '量子力学', '相对论', '深度学习',
            '机器学习', '大数据', '云计算', '区块链',
            '元宇宙', 'ChatGPT'
        ]
        return self.batch_get_entries(popular_titles[:limit])
        
    def clear_cache(self):
        """清除缓存"""
        self.cached_entries.clear()
        
    def __del__(self):
        """析构函数"""
        self.session.close()
