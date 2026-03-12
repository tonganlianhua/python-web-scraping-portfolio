#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
大众点评爬虫核心模块
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
import csv
import re
from typing import List, Dict, Optional
from collections import Counter
import os


class DianpingScraper:
    """大众点评爬虫类"""

    # User-Agent 列表
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edge/118.0.2088',
    ]

    def __init__(self, city: str = None, keyword: str = None, min_rating: float = 0.0):
        """
        初始化爬虫

        Args:
            city: 城市名称
            keyword: 搜索关键词
            min_rating: 最低评分筛选
        """
        self.city = city
        self.keyword = keyword
        self.min_rating = min_rating
        self.session = requests.Session()
        self.merchants = []
        self.reviews = []

        # 请求头
        self.headers = {
            'User-Agent': self._get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.dianping.com/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def _get_random_user_agent(self) -> str:
        """随机获取 User-Agent"""
        return random.choice(self.USER_AGENTS)

    def _random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """随机延时"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def _update_headers(self):
        """更新请求头"""
        self.headers['User-Agent'] = self._get_random_user_agent()

    def search_merchants(self, city: str, keyword: str, page: int = 1) -> List[Dict]:
        """
        搜索商家

        Args:
            city: 城市名称
            keyword: 搜索关键词
            page: 页码

        Returns:
            商家列表
        """
        self.city = city
        self.keyword = keyword

        # 构建搜索URL
        url = f"https://www.dianping.com/search/keyword/{page}/?s={keyword}"
        if city:
            url = f"https://www.dianping.com/{city}/search/{page}/?keyword={keyword}"

        print(f"正在搜索: {city} - {keyword} (第{page}页)")
        print(f"URL: {url}")

        try:
            self._update_headers()
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            merchants = self._parse_merchants(soup)

            print(f"找到 {len(merchants)} 个商家")

            # 筛选评分
            filtered = [m for m in merchants if m.get('rating', 0) >= self.min_rating]
            if self.min_rating > 0:
                print(f"评分 >= {self.min_rating} 的商家: {len(filtered)} 个")

            self.merchants.extend(filtered)
            return filtered

        except Exception as e:
            print(f"搜索失败: {e}")
            return []

    def _parse_merchants(self, soup: BeautifulSoup) -> List[Dict]:
        """
        解析商家列表

        Args:
            soup: BeautifulSoup对象

        Returns:
            商家信息列表
        """
        merchants = []

        # 查找商家列表项 - 大众点评的页面结构
        # 注意：实际HTML结构可能需要根据页面调整
        shop_items = soup.find_all('div', class_=re.compile(r'shop|item|content'))

        for item in shop_items:
            merchant = {}

            try:
                # 店名
                title_tag = item.find(['h1', 'h2', 'h3', 'h4', 'a'], class_=re.compile(r'title|name'))
                if title_tag:
                    merchant['name'] = title_tag.get_text(strip=True)
                elif item.find('a'):
                    merchant['name'] = item.find('a').get_text(strip=True)

                # 评分
                rating_tag = item.find(['span', 'div'], class_=re.compile(r'rating|score|star'))
                if rating_tag:
                    rating_text = rating_tag.get_text(strip=True)
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        merchant['rating'] = float(rating_match.group(1))
                    else:
                        merchant['rating'] = 0.0
                else:
                    merchant['rating'] = 0.0

                # 地址
                addr_tag = item.find(['span', 'div', 'p'], class_=re.compile(r'addr|address|location'))
                if addr_tag:
                    merchant['address'] = addr_tag.get_text(strip=True)
                else:
                    merchant['address'] = ''

                # 人均消费
                price_tag = item.find(['span', 'div'], class_=re.compile(r'price|cost|avg'))
                if price_tag:
                    price_text = price_tag.get_text(strip=True)
                    price_match = re.search(r'(\d+)', price_text)
                    if (price_match):
                        merchant['avg_price'] = int(price_match.group(1))
                    else:
                        merchant['avg_price'] = 0
                else:
                    merchant['avg_price'] = 0

                # 营业时间
                time_tag = item.find(['span', 'div'], class_=re.compile(r'time|hour|open'))
                if time_tag:
                    merchant['business_hours'] = time_tag.get_text(strip=True)
                else:
                    merchant['business_hours'] = ''

                # 评论数
                review_tag = item.find(['span', 'div'], class_=re.compile(r'review|comment'))
                if review_tag:
                    review_text = review_tag.get_text(strip=True)
                    review_match = re.search(r'(\d+)', review_text)
                    if review_match:
                        merchant['review_count'] = int(review_match.group(1))
                    else:
                        merchant['review_count'] = 0
                else:
                    merchant['review_count'] = 0

                # 商家链接
                link_tag = item.find('a')
                if link_tag and link_tag.get('href'):
                    merchant['url'] = link_tag['href']
                else:
                    merchant['url'] = ''

                # 添加城市和关键词
                merchant['city'] = self.city
                merchant['keyword'] = self.keyword

                # 只有当有店名时才添加
                if merchant.get('name'):
                    merchants.append(merchant)

            except Exception as e:
                print(f"解析商家信息失败: {e}")
                continue

        return merchants

    def get_merchant_reviews(self, merchant_url: str, limit: int = 10) -> List[Dict]:
        """
        获取商家评论

        Args:
            merchant_url: 商家页面URL
            limit: 评论数量限制

        Returns:
            评论列表
        """
        print(f"正在获取评论: {merchant_url}")

        if not merchant_url.startswith('http'):
            merchant_url = 'https://www.dianping.com' + merchant_url

        try:
            self._random_delay()
            self._update_headers()
            response = self.session.get(merchant_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            reviews = self._parse_reviews(soup)

            self.reviews.extend(reviews[:limit])
            return reviews[:limit]

        except Exception as e:
            print(f"获取评论失败: {e}")
            return []

    def _parse_reviews(self, soup: BeautifulSoup) -> List[Dict]:
        """
        解析评论列表

        Args:
            soup: BeautifulSoup对象对象

        Returns:
            评论信息列表
        """
        reviews = []

        # 查找评论项
        review_items = soup.find_all(['div', 'article'], class_=re.compile(r'review|comment|item'))

        for item in review_items:
            review = {}

            try:
                # 用户名
                user_tag = item.find(['span', 'a'], class_=re.compile(r'user|name'))
                if user_tag:
                    review['user'] = user_tag.get_text(strip=True)
                else:
                    review['user'] = '匿名用户'

                # 评分
                rating_tag = item.find(['span', 'div'], class_=re.compile(r'rating|score|star'))
                if rating_tag:
                    rating_text = rating_tag.get_text(strip=True)
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        review['rating'] = float(rating_match.group(1))
                    else:
                        review['rating'] = 0.0
                else:
                    review['rating'] = 0.0

                # 评论内容
                content_tag = item.find(['p', 'div', 'span'], class_=re.compile(r'content|text|desc'))
                if content_tag:
                    review['content'] = content_tag.get_text(strip=True)
                else:
                    review['content'] = ''

                # 日期
                date_tag = item.find(['span', 'time'], class_=re.compile(r'date|time'))
                if date_tag:
                    review['date'] = date_tag.get_text(strip=True)
                else:
                    review['date'] = ''

                # 点赞数
                like_tag = item.find(['span', 'div'], class_=re.compile(r'like|up|thumb'))
                if like_tag:
                    like_text = like_tag.get_text(strip=True)
                    like_match = re.search(r'(\d+)', like_text)
                    if like_match:
                        review['likes'] = int(like_match.group(1))
                    else:
                        review['likes'] = 0
                else:
                    review['likes'] = 0

                # 只有当有评论内容时才添加
                if review.get('content'):
                    reviews.append(review)

            except Exception as e:
                print(f"解析评论失败: {e}")
                continue

        return reviews

    def export_to_csv(self, filename: str = 'merchants.csv', data_type: str = 'merchants'):
        """
        导出数据到CSV文件

        Args:
            filename: 文件名
            data_type: 数据类型 (merchants 或 reviews)
        """
        data = self.merchants if data_type == 'merchants' else self.reviews

        if not data:
            print(f"没有{data_type}数据可导出")
            return

        filepath = os.path.join(os.path.dirname(__file__), filename)

        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        print(f"成功导出 {len(data)} 条数据到 {filepath}")

    def export_to_json(self, filename: str = 'merchants.json', data_type: str = 'merchants'):
        """
        导出数据到JSON文件

        Args:
            filename: 文件名
            data_type: 数据类型 (merchants 或 reviews)
        """
        data = self.merchants if data_type == 'merchants' else self.reviews

        if not data:
            print(f"没有{data_type}数据可导出")
            return

        filepath = os.path.join(os.path.dirname(__file__), filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"成功导出 {len(data)} 条数据到 {filepath}")

    def generate_report(self) -> str:
        """
        生成数据分析报告

        Returns:
            报告文本
        """
        if not self.merchants:
            return "没有商家数据可分析"

        report = []
        report.append("=" * 60)
        report.append("大众点评数据分析报告")
        report.append("=" * 60)
        report.append("")

        # 基本统计
        report.append(f"📊 基本统计")
        report.append(f"  • 商家总数: {len(self.merchants)}")
        report.append(f"  • 城市: {self.city or '未指定'}")
        report.append(f"  • 搜索关键词: {self.keyword or '未指定'}")
        report.append("")

        # 评分统计
        ratings = [m.get('rating', 0) for m in self.merchants if m.get('rating', 0) > 0]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            max_rating = max(ratings)
            min_rating = min(ratings)

            # 评分分布
            rating_dist = Counter([round(r) for r in ratings])

            report.append(f"⭐ 评分分析")
            report.append(f"  • 平均评分: {avg_rating:.2f}")
            report.append(f"  • 最高评分: {max_rating}")
            report.append(f"  • 最低评分: {min_rating}")
            report.append(f"  • 评分分布:")
            for score in sorted(rating_dist.keys(), reverse=True):
                count = rating_dist[score]
                pct = count / len(ratings) * 100
                report.append(f"      {score}星: {count}家 ({pct:.1f}%)")
            report.append("")

        # 人均消费统计
        prices = [m.get('avg_price', 0) for m in self.merchants if m.get('avg_price', 0) > 0]
        if prices:
            avg_price = sum(prices) / len(prices)
            max_price = max(prices)
            min_price = min(prices)

            # 价格分布
            price_ranges = {
                '50元以下': 0,
                '50-100元': 0,
                '100-200元': 0,
                '200-300元': 0,
                '300元以上': 0
            }

            for p in prices:
                if p < 50:
                    price_ranges['50元以下'] += 1
                elif p < 100:
                    price_ranges['50-100元'] += 1
                elif p < 200:
                    price_ranges['100-200元'] += 1
                elif p < 300:
                    price_ranges['200-300元'] += 1
                else:
                    price_ranges['300元以上'] += 1

            report.append(f"💰 人均消费分析")
            report.append(f"  • 平均人均: {avg_price:.0f}元")
            report.append(f"  • 最高人均: {max_price}元")
            report.append(f"  • 最低人均: {min_price}元")
            report.append(f"  • 价格分布:")
            for range_name, count in price_ranges.items():
                if count > 0:
                    pct = count / len(prices) * 100
                    report.append(f"      {range_name}: {count}家 ({pct:.1f}%)")
            report.append("")

        # 评论数统计
        review_counts = [m.get('review_count', 0) for m in self.merchants if m.get('review_count', 0) > 0]
        if review_counts:
            total_reviews = sum(review_counts)
            avg_reviews = total_reviews / len(review_counts)
            max_reviews = max(review_counts)

            report.append(f"💬 评论分析")
            report.append(f"  • 总评论数: {total_reviews}")
            report.append(f"  • 平均评论数: {avg_reviews:.0f}")
            report.append(f"  • 最多评论: {max_reviews}")
            report.append("")

        # 热门商家排行（按评分）
        top_by_rating = sorted(
            [m for m in self.merchants if m.get('rating', 0) > 0],
            key=lambda x: x.get('rating', 0),
            reverse=True
        )[:10]

        if top_by_rating:
            report.append(f"🏆 评分TOP10商家")
            for i, m in enumerate(top_by_rating, 1):
                name = m.get('name', '未知')
                rating = m.get('rating', 0)
                reviews = m.get('review_count', 0)
                price = m.get('avg_price', 0)
                report.append(f"  {i}. {name} - {rating}分 ({reviews}评论, {price}元)")
            report.append("")

        # 热门商家排行（按评论数）
        top_by_reviews = sorted(
            [m for m in self.merchants if m.get('review_count', 0) > 0],
            key=lambda x: x.get('review_count', 0),
            reverse=True
        )[:10]

        if top_by_reviews:
            report.append(f"🔥 评论数TOP10商家")
            for i, m in enumerate(top_by_reviews, 1):
                name = m.get('name', '未知')
                rating = m.get('rating', 0)
                reviews = m.get('review_count', 0)
                price = m.get('avg_price', 0)
                report.append(f"  {i}. {name} - {reviews}评论 ({rating}分, {price}元)")
            report.append("")

        report.append("=" * 60)
        report.append(f"报告生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)

        return "\n".join(report)

    def crawl_multiple_pages(self, city: str, keyword: str, start_page: int = 1, max_pages: int = 3):
        """
        爬取多页数据

        Args:
            city: 城市名称
            keyword: 搜索关键词
            start_page: 起始页码
            max_pages: 最大页数
        """
        self.city = city
        self.keyword = keyword

        for page in range(start_page, start_page + max_pages):
            print(f"\n--- 爬取第 {page} 页 ---")
            merchants = self.search_merchants(city, keyword, page)

            if not merchants:
                print("没有更多数据，停止爬取")
                break

            # 页面间延时
            if page < start_page + max_pages:
                self._random_delay(2, 4)

        print(f"\n总共爬取 {len(self.merchants)} 个商家")

    def get_merchant_detail(self, merchant_url: str) -> Dict:
        """
        获取商家详细信息

        Args:
            merchant_url: 商家页面URL

        Returns:
            商家详细信息
        """
        print(f"正在获取商家详情: {merchant_url}")

        if not merchant_url.startswith('http'):
            merchant_url = 'https://www.dianping.com' + merchant_url

        try:
            self._random_delay()
            self._update_headers()
            response = self.session.get(merchant_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            detail = {}

            # 解析各种详细信息
            # 这里可以根据实际页面结构扩展
            # ...
            return detail

        except Exception as e:
            print(f"获取商家详情失败: {e}")
            return {}

    def __del__(self):
        """析构函数，清理资源"""
        if hasattr(self, 'session'):
            self.session.close()
