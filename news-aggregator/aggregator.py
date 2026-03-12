#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新闻聚合器爬虫
支持多网站新闻爬取、分类、关键词过滤和导出
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from datetime import datetime
from typing import List, Dict, Optional
import sys


class NewsAggregator:
    """新闻聚合器主类"""
    
    def __init__(self, config_file: str = "config.json"):
        """初始化新闻聚合器
        
        Args:
            config_file: 配置文件路径
        """
        self.config = self._load_config(config_file)
        self.news_data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print("[OK] 新闻聚合器初始化完成")
        print(f"  - 已加载 {len(self.config['sources'])} 个新闻源")
    
    def _load_config(self, config_file: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"错误: 配置文件 {config_file} 不存在")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"错误: 配置文件格式错误 - {e}")
            sys.exit(1)
    
    def fetch_sina_news(self) -> List[Dict]:
        """爬取新浪新闻热点"""
        print("\n正在爬取新浪新闻...")
        news_list = []
        
        try:
            # 新浪新闻中心
            url = "https://news.sina.com.cn/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻标题和链接
            news_items = soup.find_all('a', href=True)
            
            count = 0
            for item in news_items:
                try:
                    title = item.get_text().strip()
                    link = item['href']
                    
                    # 过滤有效的新闻链接
                    if (title and len(title) > 10 and len(title) < 100 and
                        ('/doc/' in link or '/s/' in link) and
                        link.startswith('http')):
                        
                        # 提取时间（如果有）
                        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        news_list.append({
                            'title': title,
                            'url': link,
                            'source': '新浪新闻',
                            'category': '综合',
                            'time': time_str
                        })
                        count += 1
                        
                        if count >= self.config.get('max_news_per_source', 20):
                            break
                except Exception as e:
                    continue
            
            print(f"  [OK] 成功爬取 {len(news_list)} 条新闻")
            
        except Exception as e:
            print(f"  [FAIL] 爬取失败: {e}")
        
        return news_list
    
    def fetch_163_news(self) -> List[Dict]:
        """爬取网易新闻热点"""
        print("\n正在爬取网易新闻...")
        news_list = []
        
        try:
            # 网易新闻中心
            url = "https://news.163.com/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻标题和链接
            news_items = soup.find_all('a', href=True)
            
            count = 0
            for item in news_items:
                try:
                    title = item.get_text().strip()
                    link = item['href']
                    
                    # 过滤有效的新闻链接
                    if (title and len(title) > 10 and len(title) < 100 and
                        '/article/' in link or '/news/' in link):
                        
                        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        news_list.append({
                            'title': title,
                            'url': link,
                            'source': '网易新闻',
                            'category': '综合',
                            'time': time_str
                        })
                        count += 1
                        
                        if count >= self.config.get('max_news_per_source', 20):
                            break
                except Exception as e:
                    continue
            
            print(f"  [OK] 成功爬取 {len(news_list)} 条新闻")
            
        except Exception as e:
            print(f"  [FAIL] 爬取失败: {e}")
        
        return news_list
    
    def fetch_tencent_news(self) -> List[Dict]:
        """爬取腾讯新闻热点"""
        print("\n正在爬取腾讯新闻...")
        news_list = []
        
        try:
            # 腾讯新闻中心
            url = "https://news.qq.com/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻标题和链接
            news_items = soup.find_all('a', href=True)
            
            count = 0
            for item in news_items:
                try:
                    title = item.get_text().strip()
                    link = item['href']
                    
                    # 过滤有效的新闻链接
                    if (title and len(title) > 10 and len(title) < 100 and
                        link.startswith('http')):
                        
                        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        news_list.append({
                            'title': title,
                            'url': link,
                            'source': '腾讯新闻',
                            'category': '综合',
                            'time': time_str
                        })
                        count += 1
                        
                        if count >= self.config.get('max_news_per_source', 20):
                            break
                except Exception as e:
                    continue
            
            print(f"  [OK] 成功爬取 {len(news_list)} 条新闻")
            
        except Exception as e:
            print(f"  [FAIL] 爬取失败: {e}")
        
        return news_list
    
    def fetch_all_news(self) -> List[Dict]:
        """爬取所有配置的新闻源"""
        print("\n" + "="*50)
        print("开始爬取新闻...")
        print("="*50)
        
        all_news = []
        
        # 根据配置调用对应的爬虫
        for source in self.config['sources']:
            time.sleep(1)  # 礼貌延迟
            
            if source == 'sina':
                all_news.extend(self.fetch_sina_news())
            elif source == '163':
                all_news.extend(self.fetch_163_news())
            elif source == 'tencent':
                all_news.extend(self.fetch_tencent_news())
        
        self.news_data = all_news
        return all_news
    
    def filter_by_keywords(self, keywords: List[str]) -> List[Dict]:
        """根据关键词过滤新闻
        
        Args:
            keywords: 关键词列表（支持多个关键词）
        
        Returns:
            过滤后的新闻列表
        """
        if not keywords:
            return self.news_data
        
        filtered = []
        for news in self.news_data:
            title_lower = news['title'].lower()
            # 只要包含任意一个关键词就保留
            if any(keyword.lower() in title_lower for keyword in keywords):
                filtered.append(news)
        
        print(f"\n关键词过滤: {keywords}")
        print(f"  筛选结果: {len(filtered)} 条新闻")
        
        return filtered
    
    def export_to_json(self, data: List[Dict], filename: str = "news.json"):
        """导出为JSON格式"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n[OK] JSON 导出成功: {filename}")
            print(f"  包含 {len(data)} 条新闻")
        except Exception as e:
            print(f"\n[FAIL] JSON 导出失败: {e}")
    
    def export_to_csv(self, data: List[Dict], filename: str = "news.csv"):
        """导出为CSV格式"""
        try:
            with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['title', 'url', 'source', 'category', 'time'])
                writer.writeheader()
                writer.writerows(data)
            print(f"[OK] CSV 导出成功: {filename}")
            print(f"  包含 {len(data)} 条新闻")
        except Exception as e:
            print(f"[FAIL] CSV 导出失败: {e}")
    
    def display_summary(self, data: List[Dict] = None):
        """显示新闻摘要"""
        if data is None:
            data = self.news_data
        
        print("\n" + "="*50)
        print("新闻摘要")
        print("="*50)
        
        if not data:
            print("没有找到新闻数据")
            return
        
        # 按来源分类统计
        source_count = {}
        for news in data:
            source = news['source']
            source_count[source] = source_count.get(source, 0) + 1
        
        print(f"\n总计: {len(data)} 条新闻")
        print("\n按来源分类:")
        for source, count in sorted(source_count.items()):
            print(f"  - {source}: {count} 条")
        
        # 显示前5条新闻
        print(f"\n前 5 条新闻:")
        print("-" * 50)
        for i, news in enumerate(data[:5], 1):
            print(f"\n{i}. [{news['source']}] {news['title']}")
            print(f"   时间: {news['time']}")
            print(f"   链接: {news['url']}")
        
        if len(data) > 5:
            print(f"\n... 还有 {len(data) - 5} 条新闻")
    
    def run(self, keywords: Optional[List[str]] = None):
        """运行完整的爬取流程
        
        Args:
            keywords: 可选的关键词过滤列表
        """
        # 爬取新闻
        self.fetch_all_news()
        
        # 显示摘要
        self.display_summary()
        
        # 关键词过滤
        if keywords:
            filtered_data = self.filter_by_keywords(keywords)
            self.display_summary(filtered_data)
        else:
            filtered_data = self.news_data
        
        # 导出
        if self.config.get('export_json', True):
            json_filename = self.config.get('json_filename', 'news.json')
            self.export_to_json(filtered_data, json_filename)
        
        if self.config.get('export_csv', True):
            csv_filename = self.config.get('csv_filename', 'news.csv')
            self.export_to_csv(filtered_data, csv_filename)
        
        print("\n" + "="*50)
        print("[OK] 新闻聚合完成!")
        print("="*50)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='新闻聚合器爬虫')
    parser.add_argument('-c', '--config', default='config.json',
                        help='配置文件路径 (默认: config.json)')
    parser.add_argument('-k', '--keywords', nargs='*',
                        help='关键词过滤 (多个关键词用空格分隔)')
    
    args = parser.parse_args()
    
    # 创建并运行聚合器
    aggregator = NewsAggregator(args.config)
    aggregator.run(args.keywords)


if __name__ == '__main__':
    main()
