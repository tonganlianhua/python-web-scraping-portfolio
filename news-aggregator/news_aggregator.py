#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻聚合器 / News Aggregator
功能：聚合多个新闻源（人民网、新华网、澎湃新闻等），提取标题、时间、摘要
作者：AI助手
日期：2026-03-11
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from typing import List, Dict, Optional
from datetime import datetime
import json
import feedparser
import re

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsAggregator:
    """新闻聚合器类 / News Aggregator Class"""
    
    def __init__(self, delay_range: tuple = (1, 3)):
        """
        初始化聚合器 / Initialize Aggregator
        
        Args:
            delay_range: 请求延时的范围（秒），用于反爬 / Request delay range for anti-scraping
        """
        self.delay_range = delay_range
        self.headers = self._get_headers()
        self.session = requests.Session()
        self.results = []
        
        # 新闻源配置
        self.news_sources = {
            'people': {
                'name': '人民网',
                'url': 'http://www.people.com.cn/rss/politics.xml',
                'type': 'rss'
            },
            'xinhua': {
                'name': '新华网',
                'url': 'http://www.xinhuanet.com/politics/news_politics.xml',
                'type': 'rss'
            },
            'thepaper': {
                'name': '澎湃新闻',
                'url': 'https://www.thepaper.cn/rss/newsList.xml',
                'type': 'rss'
            },
        }
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头 / Get Request Headers"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    
    def _delay(self):
        """随机延时 / Random Delay"""
        delay = random.uniform(self.delay_range[0], self.delay_range[1])
        time.sleep(delay)
    
    def _clean_text(self, text: str) -> str:
        """
        清理文本 / Clean Text
        
        Args:
            text: 原始文本 / Original text
            
        Returns:
            清理后的文本 / Cleaned text
        """
        if not text:
            return ''
        
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def fetch_rss(self, source_key: str, limit: int = 20) -> List[Dict]:
        """
        从RSS源获取新闻 / Fetch News from RSS Source
        
        Args:
            source_key: 新闻源key / News source key
            limit: 获取新闻数量限制 / Number limit
            
        Returns:
            新闻列表 / List of news
        """
        if source_key not in self.news_sources:
            logger.warning(f'未知新闻源 / Unknown news source: {source_key}')
            return []
        
        source = self.news_sources[source_key]
        logger.info(f'开始获取 {source["name"]} 新闻 / Fetching news from {source["name"]}')
        
        try:
            # 解析RSS
            feed = feedparser.parse(source['url'])
            
            news_list = []
            
            for entry in feed.entries[:limit]:
                # 提取新闻信息
                news = {
                    '来源': source['name'],
                    '标题': self._clean_text(entry.get('title', '')),
                    '链接': entry.get('link', ''),
                    '发布时间': self._parse_time(entry.get('published', entry.get('updated', ''))),
                    '摘要': self._clean_text(entry.get('summary', entry.get('description', ''))[:200]),
                }
                
                news_list.append(news)
                logger.info(f'获取新闻: {news["标题"][:50]}...')
            
            self._delay()
            
            logger.info(f'{source["name"]} 获取完成: {len(news_list)} 条')
            return news_list
            
        except Exception as e:
            logger.error(f'获取 {source["name"]} 失败 / Failed to fetch {source["name"]}: {e}')
            return []
    
    def _parse_time(self, time_str: str) -> str:
        """
        解析时间字符串 / Parse Time String
        
        Args:
            time_str: 时间字符串 / Time string
            
        Returns:
            格式化时间 / Formatted time
        """
        try:
            if not time_str:
                return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 尝试解析时间
            parsed = feedparser._parse_date(time_str)
            if parsed:
                return datetime(*parsed[:6]).strftime('%Y-%m-%d %H:%M:%S')
            
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except:
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def fetch_all(self, sources: List[str] = None, limit: int = 20) -> List[Dict]:
        """
        获取所有新闻源 / Fetch All News Sources
        
        Args:
            sources: 新闻源列表 / List of news sources
            limit: 每个源获取新闻数量限制 / Number limit per source
            
        Returns:
            所有新闻列表 / List of all news
        """
        if sources is None:
            sources = list(self.news_sources.keys())
        
        all_news = []
        
        for source_key in sources:
            news_list = self.fetch_rss(source_key, limit)
            all_news.extend(news_list)
        
        # 按时间排序
        all_news.sort(key=lambda x: x['发布时间'], reverse=True)
        
        self.results = all_news
        return all_news
    
    def filter_by_keyword(self, keyword: str) -> List[Dict]:
        """
        根据关键词过滤新闻 / Filter News by Keyword
        
        Args:
            keyword: 搜索关键词 / Search keyword
            
        Returns:
            过滤后的新闻列表 / Filtered news list
        """
        if not keyword:
            return self.results
        
        filtered = [
            item for item in self.results
            if keyword.lower() in item['标题'].lower() or
               keyword.lower() in item['摘要'].lower()
        ]
        
        logger.info(f'关键词 "{keyword}" 过滤后，剩余 {len(filtered)} 条新闻')
        return filtered
    
    def export_to_excel(self, filename: str = 'news_results.xlsx', data: List[Dict] = None):
        """
        导出为Excel文件 / Export to Excel
        
        Args:
            filename: 文件名 / Filename
            data: 要导出的数据 / Data to export
        """
        export_data = data if data is not None else self.results
        
        if not export_data:
            logger.warning('没有数据可导出 / No data to export')
            return
        
        try:
            df = pd.DataFrame(export_data)
            
            # 重新排列列顺序
            columns_order = ['来源', '标题', '发布时间', '摘要', '链接']
            df = df[columns_order]
            
            df.to_excel(filename, index=False, engine='openpyxl')
            logger.info(f'成功导出 {len(export_data)} 条数据到 {filename}')
            
            # 打印预览
            print('\n=== 数据预览 / Data Preview ===')
            print(df.head(10).to_string(index=False))
            
        except Exception as e:
            logger.error(f'导出Excel失败 / Export to Excel failed: {e}')
    
    def export_to_json(self, filename: str = 'news_results.json', data: List[Dict] = None):
        """
        导出为JSON文件 / Export to JSON
        
        Args:
            filename: 文件名 / Filename
            data: 要导出的数据 / Data to export
        """
        export_data = data if data is not None else self.results
        
        if not export_data:
            logger.warning('没有数据可导出 / No data to export')
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            logger.info(f'成功导出 {len(export_data)} 条数据到 {filename}')
        except Exception as e:
            logger.error(f'导出JSON失败 / Export to JSON failed: {e}')
    
    def print_summary(self):
        """打印统计摘要 / Print Summary"""
        if not self.results:
            print('暂无数据 / No data available')
            return
        
        # 统计各来源新闻数量
        source_count = {}
        for news in self.results:
            source = news['来源']
            source_count[source] = source_count.get(source, 0) + 1
        
        print('\n=== 新闻统计 / News Statistics ===')
        print(f'总新闻数 / Total news: {len(self.results)}')
        print(f'来源分布 / Source distribution:')
        for source, count in source_count.items():
            print(f'  - {source}: {count} 条')
        print('=' * 40)


def main():
    """主函数 / Main Function"""
    print('=' * 60)
    print('新闻聚合器 / News Aggregator')
    print('=' * 60)
    
    # 创建聚合器实例
    aggregator = NewsAggregator()
    
    # 获取新闻
    print('\n开始获取新闻...')
    news_list = aggregator.fetch_all(limit=20)
    
    if news_list:
        print(f'\n✅ 成功获取 {len(news_list)} 条新闻')
        
        # 打印统计
        aggregator.print_summary()
        
        # 关键词搜索（可选）
        keyword = input('\n请输入搜索关键词（留空则搜索全部）/ Enter keyword (empty for all): ').strip()
        
        if keyword:
            filtered_news = aggregator.filter_by_keyword(keyword)
            print(f'\n✅ 关键词过滤后剩余 {len(filtered_news)} 条新闻')
            export_data = filtered_news
        else:
            export_data = news_list
        
        # 导出文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        excel_file = f'news_results_{timestamp}.xlsx'
        json_file = f'news_results_{timestamp}.json'
        
        aggregator.export_to_excel(excel_file, export_data)
        aggregator.export_to_json(json_file, export_data)
        
        print(f'\n✅ Excel文件: {excel_file}')
        print(f'✅ JSON文件: {json_file}')
    else:
        print('\n❌ 未能获取到新闻')
    
    print('=' * 60)


if __name__ == '__main__':
    main()
