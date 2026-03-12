"""
知乎热榜爬虫核心模块
提供实时获取知乎热榜、话题详情、热度对比等功能
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
from typing import List, Dict, Optional
from datetime import datetime
import re


class ZhihuHotScraper:
    """知乎热榜爬虫类"""

    def __init__(self):
        """初始化爬虫"""
        self.base_url = "https://www.zhihu.com"
        self.hot_url = "https://www.zhihu.com/hot"
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        ]
        self.headers = {
            "User-Agent": self._get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _get_random_user_agent(self) -> str:
        """随机获取User-Agent"""
        return random.choice(self.user_agents)

    def _random_delay(self, min_delay: float = 0.5, max_delay: float = 2.0):
        """随机延时"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def _update_headers(self):
        """更新请求头，轮换User-Agent"""
        self.headers["User-Agent"] = self._get_random_user_agent()
        self.session.headers.update(self.headers)

    def _get_page(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """获取网页内容，带重试机制"""
        for attempt in range(max_retries):
            try:
                self._update_headers()
                self._random_delay(0.3, 1.0)
                
                response = self.session.get(url, timeout=10, allow_redirects=True)
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    # 被限流，增加延时
                    print(f"访问频率限制，等待 {2 ** attempt} 秒后重试...")
                    time.sleep(2 ** attempt)
                else:
                    print(f"请求失败，状态码: {response.status_code}")
                    
            except Exception as e:
                print(f"请求异常 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)
        
        return None

    def get_hot_list(self, keyword: Optional[str] = None) -> List[Dict]:
        """
        获取知乎热榜话题列表
        
        Args:
            keyword: 可选关键词过滤
            
        Returns:
            热榜话题列表
        """
        hot_list = []
        
        response = self._get_page(self.hot_url)
        if not response:
            print("获取热榜失败")
            return hot_list
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 尝试多种方式解析热榜数据
        # 方法1: 查找 JavaScript 数据
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string and 'hotList' in script.string:
                try:
                    # 提取 JSON 数据
                    pattern = r'var data\s*=\s*({.*?});'
                    match = re.search(pattern, script.string, re.DOTALL)
                    if match:
                        data = json.loads(match.group(1))
                        hot_list = self._parse_hot_data(data)
                        break
                except Exception as e:
                    print(f"解析JavaScript数据失败: {str(e)}")
        
        # 方法2: 解析HTML结构
        if not hot_list:
            hot_list = self._parse_hot_html(soup)
        
        # 关键词过滤
        if keyword:
            hot_list = [item for item in hot_list if keyword.lower() in item['title'].lower()]
        
        print(f"成功获取 {len(hot_list)} 个热榜话题")
        return hot_list

    def _parse_hot_data(self, data: Dict) -> List[Dict]:
        """解析JavaScript数据"""
        hot_list = []
        
        if 'hotList' in data:
            for index, item in enumerate(data['hotList'], 1):
                hot_item = {
                    'rank': index,
                    'title': item.get('target', {}).get('title', ''),
                    'hot_value': item.get('hotValue', 0),
                    'link': f"https://www.zhihu.com{item.get('target', {}).get('url', '')}",
                    'excerpt': item.get('target', {}).get('excerpt', {}).get('text', ''),
                    'created_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                hot_list.append(hot_item)
        
        return hot_list

    def _parse_hot_html(self, soup: BeautifulSoup) -> List[Dict]:
        """解析HTML结构获取热榜"""
        hot_list = []
        
        # 查找热榜条目
        hot_items = soup.find_all('div', class_='HotItem')
        
        for index, item in enumerate(hot_items, 1):
            try:
                title_elem = item.find('h2', class_='HotItem-title')
                if title_elem:
                    link_elem = title_elem.find('a')
                    if link_elem:
                        title = link_elem.get_text(strip=True)
                        link = link_elem.get('href', '')
                        if link and not link.startswith('http'):
                            link = f"https://www.zhihu.com{link}"
                
                # 热度值
                hot_elem = item.find('div', class_='HotItem-metrics')
                hot_value = 0
                if hot_elem:
                    hot_text = hot_elem.get_text(strip=True)
                    # 提取数字
                    match = re.search(r'([\d.]+)', hot_text)
                    if match:
                        hot_value = float(match.group(1))
                        if '万' in hot_text:
                            hot_value *= 10000
                
                # 摘要
                excerpt_elem = item.find('p', class_='HotItem-excerpt')
                excerpt = excerpt_elem.get_text(strip=True) if excerpt_elem else ''
                
                hot_item = {
                    'rank': index,
                    'title': title,
                    'hot_value': hot_value,
                    'link': link,
                    'excerpt': excerpt,
                    'created_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                
                hot_list.append(hot_item)
                
            except Exception as e:
                print(f"解析热榜项失败: {str(e)}")
                continue
        
        return hot_list

    def get_topic_detail(self, question_url: str) -> Dict:
        """
        获取话题详情
        
        Args:
            question_url: 问题URL
            
        Returns:
            话题详情字典
        """
        detail = {
            'url': question_url,
            'answer_count': 0,
            'follower_count': 0,
            'view_count': 0,
            'tags': [],
        }
        
        response = self._get_page(question_url)
        if not response:
            return detail
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        try:
            # 获取 JSON 数据
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and 'initialState' in script.string:
                    try:
                        pattern = r'window\.__INITIAL_STATE__\s*=\s*({.*?});'
                        match = re.search(pattern, script.string, re.DOTALL)
                        if match:
                            data = json.loads(match.group(1))
                            
                            # 提取问题详情
                            if 'entities' in data and 'questions' in data['entities']:
                                question_id = list(data['entities']['questions'].keys())[0]
                                question_data = data['entities']['questions'][question_id]
                                
                                detail['answer_count'] = question_data.get('answerCount', 0)
                                detail['follower_count'] = question_data.get('followerCount', 0)
                                detail['view_count'] = question_data.get('viewCount', 0)
                                
                                # 提取标签
                                if 'topics' in data['entities']:
                                    for topic_id, topic_data in data['entities']['topics'].items():
                                        detail['tags'].append(topic_data.get('name', ''))
                                
                                break
                    except Exception as e:
                        print(f"解析详情数据失败: {str(e)}")
        except Exception as e:
            print(f"获取话题详情失败: {str(e)}")
        
        return detail

    def compare_hot_values(self, hot_list_1: List[Dict], hot_list_2: List[Dict]) -> List[Dict]:
        """
        对比两次采集的热度变化
        
        Args:
            hot_list_1: 第一次采集的热榜
            hot_list_2: 第二次采集的热榜
            
        Returns:
            热度变化列表
        """
        comparison = []
        
        # 创建URL到热榜项的映射
        dict_1 = {item['link']: item for item in hot_list_1}
        dict_2 = {item['link']: item for item in hot_list_2}
        
        # 对比所有话题
        all_urls = set(dict_1.keys()) | set(dict_2.keys())
        
        for url in all_urls:
            if url in dict_1 and url in dict_2:
                # 两次都存在的话题
                change = dict_2[url]['hot_value'] - dict_1[url]['hot_value']
                comparison.append({
                    'title': dict_2[url]['title'],
                    'hot_value_1': dict_1[url]['hot_value'],
                    'hot_value_2': dict_2[url]['hot_value'],
                    'change': change,
                    'change_percent': (change / dict_1[url]['hot_value'] * 100) if dict_1[url]['hot_value'] > 0 else 0,
                    'link': url,
                })
            elif url in dict_1:
                # 只在第一次存在（已下榜）
                comparison.append({
                    'title': dict_1[url]['title'],
                    'hot_value_1': dict_1[url]['hot_value'],
                    'hot_value_2': 0,
                    'change': -dict_1[url]['hot_value'],
                    'change_percent': -100,
                    'link': url,
                    'status': 'dropped',
                })
            else:
                # 只在第二次存在（新上榜）
                comparison.append({
                    'title': dict_2[url]['title'],
                    'hot_value_1': 0,
                    'hot_value_2': dict_2[url]['hot_value'],
                    'change': dict_2[url]['hot_value'],
                    'change_percent': 100,
                    'link': url,
                    'status': 'new',
                })
        
        # 按变化幅度排序
        comparison.sort(key=lambda x: abs(x['change']), reverse=True)
        
        return comparison
