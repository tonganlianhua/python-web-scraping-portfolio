#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜爬虫 / Weibo Hot Search Scraper
功能：爬取微博热搜榜单，支持关键词搜索，导出Excel
Function: Scrape Weibo hot search ranking, supports keyword search, export to Excel
作者：AI助手
日期：2026-03-11
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from typing import List, Dict, Optional
import logging

# 配置日志 / Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeiboHotSearchScraper:
    """微博热搜爬虫类 / Weibo Hot Search Scraper Class"""
    
    def __init__(self, delay_range: tuple = (1, 3)):
        """
        初始化爬虫 / Initialize Scraper
        
        Args:
           参数说明 / Parameters:
            delay_range: 请求延时的范围（秒），用于反爬 / Request delay range in seconds for anti-scraping
        """
        self.delay_range = delay_range
        self.headers = self._get_random_headers()
        self.session = requests.Session()
        
    def _get_random_headers(self) -> Dict[str, str]:
        """
        获取随机User-Agent头部 / Get Random User-Agent Headers
        
        Returns:
            返回说明 / Returns:
            包含User-Agent等请求头的字典 / Dictionary containing User-Agent and other headers
        """
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://s.weibo.com/top/summary'
        }
    
    def _delay(self):
        """随机延时，用于反爬 / Random Delay for Anti-scraping"""
        delay = random.uniform(self.delay_range[0], self.delay_range[1])
        time.sleep(delay)
    
    def fetch_hot_search(self) -> List[Dict[str, str]]:
        """
        爬取微博热搜榜单 / Scrape Weibo Hot Search Ranking
        
        Returns:
            返回说明 / Returns:
            热搜数据列表，每个元素包含排名、标题、热度值、链接 / List of hot search data, each element contains ranking, title, heat value, link
        """
        url = 'https://s.weibo.com/top/summary'
        
        try:
            logger.info(f'正在获取微博热搜 / Fetching Weibo hot search: {url}')
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找热搜榜单表格 / Find hot search ranking table
            hot_data = []
            
            # 方法1: 查找#pl_top_realtimehot tbody下的所有tr
            # Method 1: Find all tr under #pl_top_realtimehot tbody
            tbody = soup.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
                for row in rows:
                    try:
                        # 获取排名 / Get ranking
                        rank_cell = row.find('td')
                        if rank_cell:
                            rank = rank_cell.get_text(strip=True)
                            
                            # 获取标题和链接 / Get title and link
                            link_cell = row.find('a')
                            if link_cell:
                                title = link_cell.get_text(strip=True)
                                link = 'https://s.weibo.com' + link_cell.get('href', '')
                                
                                # 获取热度值 / Get heat value
                                cells = row.find_all('td')
                                hot_value = ''
                                if len(cells) >= 3:
                                    hot_value = cells[2].get_text(strip=True)
                                
                                # 过滤无效数据 / Filter invalid data
                                if title and rank.isdigit():
                                    hot_data.append({
                                        '排名': rank,
                                        '标题': title,
                                        '热度值': hot_value,
                                        '链接': link
                                    })
                                    logger.info(f'获取到热搜 / Hot search fetched: {rank}. {title} (热度/Heat: {hot_value})')
                    except Exception as e:
                        logger.warning(f'解析单行数据时出错 / Error parsing single row: {e}')
                        continue
            
            self._delay()
            
            if not hot_data:
                logger.warning('未获取到热搜数据，尝试备用解析方法 / No hot search data fetched, trying backup parsing method')
                # 备用方法：查找所有包含热搜信息的div
                # Backup method: Find all divs containing hot search information
                # 这里可以添加备用解析逻辑 / Can add backup parsing logic here
            
            return hot_data
            
        except requests.RequestException as e:
            logger.error(f'请求微博热搜失败 / Request Weibo hot search failed: {e}')
            return []
        except Exception as e:
            logger.error(f'解析微博热搜失败 / Parse Weibo hot search failed: {e}')
            return []
    
    def filter_by_keyword(self, data: List[Dict[str, str]], keyword: str) -> List[Dict[str, str]]:
        """
        根据关键词过滤热搜数据 / Filter Hot Search Data by Keyword
        
        Args:
            参数说明 / Parameters:
            data: 原始热搜数据 / Original hot search data
            keyword: 搜索关键词 / Search keyword
            
        Returns:
            返回说明 / Returns:
            过滤后的热搜数据 / Filtered hot search data
        """
        if not keyword:
            return data
        
        filtered = [item for item in data if keyword.lower() in item['标题'].lower()]
        logger.info(f'关键词 "{keyword}" 过滤后，剩余 {len(filtered)} 条数据 / After filtering by keyword "{keyword}", {len(filtered)} items remaining')
        return filtered
    
    def export_to_excel(self, data: List[Dict[str, str]], filename: str = 'weibo_hot_search.xlsx'):
        """
        将热搜数据导出为Excel文件 / Export Hot Search Data to Excel File
        
        Args:
            参数说明 / Parameters:
            data: 热搜数据 / Hot search data
            filename: 输出文件名 / Output filename
        """
        if not data:
            logger.warning('没有数据可导出 / No data to export')
            return
        
        try:
            # 转换为DataFrame / Convert to DataFrame
            df = pd.DataFrame(data)
            
            # 重新排列列的顺序 / Reorder columns
            columns_order = ['排名', '标题', '热度值', '链接']
            df = df[columns_order]
            
            # 导出Excel / Export to Excel
            df.to_excel(filename, index=False, engine='openpyxl')
            logger.info(f'成功导出 {len(data)} 条数据到 {filename} / Successfully exported {len(data)} items to {filename}')
            
            # 打印前几条数据预览 / Print preview of first few items
            print('\n=== 数据预览 / Data Preview ===')
            print(df.head(10).to_string(index=False))
            
        except Exception as e:
            logger.error(f'导出Excel失败 / Export to Excel failed: {e}')
            raise


def main():
    """主函数 / Main Function"""
    print('=' * 60)
    print('微博热搜爬虫 / Weibo Hot Search Scraper')
    print('=' * 60)
    
    # 创建爬虫实例 / Create scraper instance
    scraper = WeiboHotSearchScraper(delay_range=(1, 2))
    
    # 获取热搜数据 / Fetch hot search data
    print('\n[1/3] 正在获取微博热搜数据 / [1/3] Fetching Weibo hot search data...')
    hot_data = scraper.fetch_hot_search()
    
    if not hot_data:
        print('\n❌ 未能获取到热搜数据，请检查网络连接或稍后重试 / ❌ Failed to fetch hot search data, please check network or try again later')
        return
    
    print(f'\n✅ 成功获取 {len(hot_data)} 条热话题 / ✅ Successfully fetched {len(hot_data)} hot topics')
    
    # 关键词搜索（可选）/ Keyword search (optional)
    keyword = input('\n[2/3] 输入搜索关键词（留空则搜索全部） / [2/3] Enter search keyword (leave empty for all): ').strip()
    filtered_data = scraper.filter_by_keyword(hot_data, keyword)
    
    if keyword:
        print(f'\n✅ 关键词过滤后剩余 {len(filtered_data)} 条数据 / ✅ After keyword filtering, {len(filtered_data)} items remaining')
    else:
        print(f'\n✅ 使用全部 {len(filtered_data)} 条数据 / ✅ Using all {len(filtered_data)} items')
    
    # 导出Excel / Export to Excel
    print('\n[3/3] 导出Excel文件 / [3/3] Exporting to Excel...')
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filename = f'weibo_hot_search_{timestamp}.xlsx'
    scraper.export_to_excel(filtered_data, filename)
    
    print(f'\n✅ 完成！文件已保存为: {filename} / ✅ Completed! File saved as: {filename}')
    print('=' * 60)


if __name__ == '__main__':
    main()
