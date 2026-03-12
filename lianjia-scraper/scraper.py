# -*- coding: utf-8 -*-
"""
链家房产信息爬虫核心模块
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin
from config import CITIES, ROOM_TYPES, DEFAULT_CONFIG, URL_TEMPLATES, FIELD_MAPPING
from utils.anti_scraping import AntiScraping


class LianjiaScraper:
    """链家房产爬虫类"""
    
    def __init__(self, city='bj', region='', config=None):
        """
        初始化爬虫
        
        Args:
            city: 城市代码（bj/sh/sz等）
            region: 区域代码
            config: 配置字典
        """
        self.city = city
        self.region = region
        self.config = config or DEFAULT_CONFIG.copy()
        self.anti_scraping = AntiScraping()
        self.session = requests.Session()
        self.session.cookies.update(self.anti_scraping.get_cookies())
        
        # 获取城市域名
        self.city_domain = f"{city}.lianjia.com"
        self.base_url = f"https://{self.city_domain}"
        
        print(f"初始化爬虫 - 城市: {CITIES.get(city, city)}, 区域: {region}")
    
    def build_url(self, page=1, params=None):
        """构建请求URL"""
        if page == 1:
            url = URL_TEMPLATES['ershoufang'].format(
                city=self.city,
                region=self.region
            )
        else:
            url = URL_TEMPLATES['ershoufang_with_params'].format(
                city=self.city,
                region=self.region,
                region_part=f"{self.region}/" if self.region else "",
                page=page
            )
        
        # 添加筛选参数
        if params:
            query_parts = []
            if params.get('price_min') and params.get('price_max'):
                query_parts.append(f"rp{params['price_min']}ep{params['price_max']}")
            elif params.get('price_min'):
                query_parts.append(f"rp{params['price_min']}")
            elif params.get('price_max'):
                query_parts.append(f"ep{params['price_max']}")
            
            if params.get('room_type'):
                query_parts.append(f"l{params['room_type']}")
            
            if query_parts:
                url = url.rstrip('/') + '/' + '/'.join(query_parts) + '/'
        
        return url
    
    def make_request(self, url, retry_times=3):
        """
        发送HTTP请求
        
        Args:
            url: 请求URL
            retry_times: 重试次数
            
        Returns:
            BeautifulSoup对象或None
        """
        for attempt in range(retry_times):
            try:
                headers = self.anti_scraping.get_headers(referer=self.base_url)
                
                print(f"正在请求: {url}")
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=self.config.get('timeout', 30)
                )
                
                # 检查响应状态
                if response.status_code == 200:
                    print(f"请求成功 (状态码: {response.status_code})")
                    return BeautifulSoup(response.text, 'html.parser')
                elif response.status_code == 403:
                    print(f"访问被拒绝 (403)，可能触发了反爬机制")
                    time.sleep(self.anti_scraping.random_sleep(5, 10))
                else:
                    print(f"请求失败 (状态码: {response.status_code})")
                    
            except requests.exceptions.Timeout:
                print(f"请求超时 (尝试 {attempt + 1}/{retry_times})")
            except requests.exceptions.RequestException as e:
                print(f"请求异常: {e}")
            
            # 随机延迟后重试
            if attempt < retry_times - 1:
                delay = self.anti_scraping.random_sleep(2, 5)
                print(f"等待 {delay:.2f} 秒后重试...")
        
        return None
    
    def parse_house_info(self, house_div):
        """
        解析单个房源信息
        
        Args:
            house_div: BeautifulSoup元素
            
        Returns:
            房源信息字典
        """
        house_info = {}
        
        try:
            # 提取标题和链接
            title_tag = house_div.find('a', class_='title')
            if title_tag:
                house_info['title'] = title_tag.text.strip()
                house_info['url'] = urljoin(self.base_url, title_tag.get('href', ''))
            else:
                house_info['title'] = '未知'
                house_info['url'] = ''
            
            # 提取价格
            price_tag = house_div.find('div', class_='totalPrice')
            if price_tag:
                house_info['price'] = price_tag.text.strip().replace('万', '').replace(',', '')
            else:
                house_info['price'] = '0'
            
            # 提取单价
            unit_price_tag = house_div.find('div', class_='unitPrice')
            if unit_price_tag:
                unit_price_text = unit_price_tag.find('span')
                if unit_price_text:
                    house_info['unit_price'] = unit_price_text.text.strip().replace(',', '')
                else:
                    house_info['unit_price'] = '0'
            else:
                house_info['unit_price'] = '0'
            
            # 提取详细信息（户型、面积、楼层等）
            info_divs = house_div.find('div', class_='houseInfo')
            if info_divs:
                info_text = info_divs.text.strip()
                info_parts = info_text.split('|')
                
                # 解析户型、面积等信息
                for part in info_parts:
                    part = part.strip()
                    if '室' in part or '居' in part:
                        house_info['room_type'] = part
                    elif '平' in part or '㎡' in part:
                        house_info['area'] = part.replace('平米', '').replace('平', '').replace('㎡', '').replace('m²', '')
                    elif '楼' in part:
                        house_info['floor'] = part
            
            # 解析朝向和装修
            position_div = house_div.find('div', class_='positionInfo')
            if position_div:
                position_text = position_div.text.strip()
                position_parts = position_text.split('|')
                
                for part in position_parts:
                    part = part.strip()
                    if any(x in part for x in ['东', '南', '西', '北']):
                        house_info['orientation'] = part
                    elif any(x in part for x in ['精装', '简装', '毛坯', '其他']):
                        house_info['decoration'] = part
            
            # 提取小区名称
            community_div = house_div.find('div', class_='positionInfo')
            if community_div:
                community_text = community_div.text.strip()
                if '|' in community_text:
                    house_info['community'] = community_text.split('|')[0].strip()
                else:
                    house_info['community'] = community_text
            
            # 填充缺失字段
            default_fields = {
                'room_type': '未知',
                'area': '0',
                'floor': '未知',
                'orientation': '未知',
                'decoration': '未知',
                'community': '未知',
                'address': '未知'
            }
            
            for field, default_value in default_fields.items():
                if field not in house_info:
                    house_info[field] = default_value
            
            # 添加城市和区域信息
            house_info['city'] = CITIES.get(self.city, self.city)
            house_info['region'] = self.region if self.region else '全部'
            
        except Exception as e:
            print(f"解析房源信息时出错: {e}")
            return None
        
        return house_info
    
    def scrape_page(self, page=1):
        """
        爬取单页房源信息
        
        Args:
            page: 页码
            
        Returns:
            房源信息列表
        """
        # 构建URL参数
        params = {
            'price_min': self.config.get('price_min'),
            'price_max': self.config.get('price_max'),
            'room_type': self.config.get('room_type')
        }
        
        url = self.build_url(page, params)
        soup = self.make_request(url)
        
        if not soup:
            print(f"页面 {page} 请求失败")
            return []
        
        # 查找房源列表
        house_list = []
        house_divs = soup.find_all('div', class_='clear')
        
        if not house_divs:
            # 尝试其他可能的选择器
            house_divs = soup.find_all('li', class_='clear')
        
        if not house_divs:
            print("未找到房源列表，可能页面结构已变化或无数据")
            return []
        
        print(f"页面 {page} 找到 {len(house_divs)} 个房源")
        
        for house_div in house_divs:
            house_info = self.parse_house_info(house_div)
            if house_info:
                house_list.append(house_info)
        
        # 随机延迟
        if page < self.config.get('max_pages', 5):
            delay = self.anti_scraping.random_sleep(
                self.config.get('delay_min', 1),
                self.config.get('delay_max', 3)
            )
            print(f"等待 {delay:.2f} 秒后继续...")
        
        return house_list
    
    def scrape_multiple_pages(self, max_pages=None):
        """
        爬取多页房源信息
        
        Args:
            max_pages: 最大页数
            
        Returns:
            所有房源信息列表
        """
        max_pages = max_pages or self.config.get('max_pages', 5)
        all_houses = []
        
        print(f"\n开始爬取，最大页数: {max_pages}")
        print(f"城市: {CITIES.get(self.city, self.city)}, 区域: {self.region or '全部'}")
        print(f"价格区间: {self.config.get('price_min', 0)}-{self.config.get('price_max', '无限制')}万")
        print(f"户型筛选: {ROOM_TYPES.get(self.config.get('room_type'), '全部')}")
        print("-" * 60)
        
        for page in range(1, max_pages + 1):
            print(f"\n=== 正在爬取第 {page} 页 ===")
            houses = self.scrape_page(page)
            
            if not houses:
                print(f"第 {page} 页没有数据，停止爬取")
                break
            
            all_houses.extend(houses)
            print(f"第 {page} 页获取到 {len(houses)} 个房源，累计: {len(all_houses)} 个")
        
        print(f"\n爬取完成！共获取 {len(all_houses)} 个房源")
        return all_houses
    
    def close(self):
        """关闭会话"""
        self.session.close()
