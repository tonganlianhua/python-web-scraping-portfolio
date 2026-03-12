#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据导出和分析模块
"""

import csv
import json
import os
from typing import List, Dict
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


class DataExporter:
    """数据导出和分析类"""

    def __init__(self, data_dir: str = None):
        """
        初始化导出器

        Args:
            data_dir: 数据保存目录
        """
        if data_dir is None:
            data_dir = os.path.dirname(__file__)
        self.data_dir = data_dir

        # 设置中文字体
        self._setup_chinese_font()

    def _setup_chinese_font(self):
        """设置中文字体"""
        try:
            # 尝试常见的系统字体
            font_names = ['SimHei', 'Microsoft YaHei', 'SimSun', 'KaiTi']
            for font_name in font_names:
                try:
                    plt.rcParams['font.sans-serif'] = [font_name]
                    plt.rcParams['axes.unicode_minus'] = False
                    break
                except:
                    continue
        except:
            pass

    def export_csv(self, data: List[Dict], filename: str, encoding: str = 'utf-8-sig'):
        """
        导出数据到CSV文件

        Args:
            data: 数据列表
            filename: 文件名
            encoding: 编码格式
        """
        if not data:
            print("没有数据可导出")
            return

        filepath = os.path.join(self.data_dir, filename)

        try:
            # 获取所有可能的字段名
            fieldnames = set()
            for item in data:
                fieldnames.update(item.keys())
            fieldnames = list(fieldnames)

            with open(filepath, 'w', encoding=encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            print(f"成功导出 {len(data)} 条数据到 {filepath}")
            return filepath
        except Exception as e:
            print(f"导出CSV失败: {e}")
            return None

    def export_json(self, data: List[Dict], filename: str):
        """
        导出数据到JSON文件

        Args:
            data: 数据列表
            filename: 文件名
        """
        if not data:
            print("没有数据可导出")
            return

        filepath = os.path.join(self.data_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"成功导出 {len(data)} 条数据到 {filepath}")
            return filepath
        except Exception as e:
            print(f"导出JSON失败: {e}")
            return None

    def generate_text_report(self, merchants: List[Dict], reviews: List[Dict] = None) -> str:
        """
        生成文本分析报告

        Args:
            merchants: 商家数据
            reviews: 评论数据（可选）

        Returns:
            报告文本
        """
        if not merchants:
            return "没有商家数据可分析"

        report = []
        report.append("=" * 70)
        report.append("大众点评数据分析报告".center(70))
        report.append("=" * 70)
        report.append("")

        # 基本信息
        city = merchants[0].get('city', '未指定') if merchants else '未指定'
        keyword = merchants[0].get('keyword', '未指定') if merchants else '未指定'

        report.append(f"📋 基本信息")
        report.append(f"  • 商家总数: {len(merchants)}")
        report.append(f"  • 城市: {city}")
        report.append(f"  • 搜索关键词: {keyword}")
        report.append(f"  • 评论数: {len(reviews) if reviews else 0}")
        report.append("")

        # 评分分析
        self._analyze_ratings(merchants, report)

        # 人均消费分析
        self._analyze_prices(merchants, report)

        # 评论数分析
        self._analyze_reviews(merchants, report)

        # TOP排行
        self._top_rankings(merchants, report)

        # 评论情感分析（如果有评论数据）
        if reviews:
            self._analyze_sentiment(reviews, report)

        report.append("")
        report.append("=" * 70)
        report.append("报告生成完成".center(70))
        report.append("=" * 70)

        return "\n".join(report)

    def _analyze_ratings(self, merchants: List[Dict], report: List[str]):
        """分析评分数据"""
        ratings = [m.get('rating', 0) for m in merchants if m.get('rating', 0) > 0]

        if not ratings:
            return

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
            bar = "█" * int(pct / 5)
            report.append(f"      {score}星: {count:3d}家 ({pct:5.1f}%) {bar}")

        report.append("")

    def _analyze_prices(self, merchants: List[Dict], report: List[str]):
        """分析人均消费数据"""
        prices = [m.get('avg_price', 0) for m in merchants if m.get('avg_price', 0) > 0]

        if not prices:
            return

        avg_price = sum(prices) / len(prices)
        max_price = max(prices)
        min_price = min(prices)

        # 价格分布
        price_ranges = {
            '50元以下': (0, 0),
            '50-100元': (0, 0),
            '100-200元': (0, 0),
            '200-300元': (0, 0),
            '300元以上': (0, 0)
        }

        for p in prices:
            if p < 50:
                price_ranges['50元以下'] = (price_ranges['50元以下'][0] + 1, price_ranges['50元以下'][1] + p)
            elif p < 100:
                price_ranges['50-100元'] = (price_ranges['50-100元'][0] + 1, price_ranges['50-100元'][1] + p)
            elif p < 200:
                price_ranges['100-200元'] = (price_ranges['100-200元'][0] + 1, price_ranges['100-200元'][1] + p)
            elif p < 300:
                price_ranges['200-300元'] = (price_ranges['200-300元'][0] + 1, price_ranges['200-300元'][1] + p)
            else:
                price_ranges['300元以上'] = (price_ranges['300元以上'][0] + 1, price_ranges['300元以上'][1] + p)

        report.append(f"💰 人均消费分析")
        report.append(f"  • 平均人均: {avg_price:.0f}元")
        report.append(f"  • 最高人均: {max_price}元")
        report.append(f"  • 最低人均: {min_price}元")
        report.append(f"  • 价格分布:")

        for range_name, (count, total) in price_ranges.items():
            if count > 0:
                pct = count / len(prices) * 100
                avg_in_range = total / count
                bar = "█" * int(pct / 5)
                report.append(f"      {range_name:10s}: {count:3d}家 ({pct:5.1f}%) 平均{avg_in_range:.0f}元 {bar}")

        report.append("")

    def _analyze_reviews(self, merchants: List[Dict], report: List[str]):
        """分析评论数数据"""
        review_counts = [m.get('review_count', 0) for m in merchants if m.get('review_count', 0) > 0]

        if not review_counts:
            return

        total_reviews = sum(review_counts)
        avg_reviews = total_reviews / len(review_counts)
        max_reviews = max(review_counts)
        min_reviews = min(review_counts)

        # 评论数分布
        review_ranges = {
            '10条以下': 0,
            '10-50条': 0,
            '50-100条': 0,
            '100-500条': 0,
            '500条以上': 0
        }

        for r in review_counts:
            if r < 10:
                review_ranges['10条以下'] += 1
            elif r < 50:
                review_ranges['10-50条'] += 1
            elif r < 100:
                review_ranges['50-100条'] += 1
            elif r < 500:
                review_ranges['100-500条'] += 1
            else:
                review_ranges['500条以上'] += 1

        report.append(f"💬 评论数分析")
        report.append(f"  • 总评论数: {total_reviews}")
        report.append(f"  • 平均评论数: {avg_reviews:.0f}")
        report.append(f"  • 最多评论: {max_reviews}")
        report.append(f"  • 最少评论: {min_reviews}")
        report.append(f"  • 评论分布:")

        for range_name, count in review_ranges.items():
            if count > 0:
                pct = count / len(review_counts) * 100
                bar = "█" * int(pct / 5)
                report.append(f"      {range_name:10s}: {count:3d}家 ({pct:5.1f}%) {bar}")

        report.append("")

    def _top_rankings(self, merchants: List[Dict], report: List[str]):
        """生成TOP排行"""
        # 按评分排行
        top_by_rating = sorted(
            [m for m in merchants if m.get('rating', 0) > 0],
            key=lambda x: x.get('rating', 0),
            reverse=True
        )[:10]

        if top_by_rating:
            report.append(f"🏆 评分TOP10商家")
            for i, m in enumerate(top_by_rating, 1):
                name = m.get('name', '未知')[:20]  # 限制长度
                rating = m.get('rating', 0)
                reviews = m.get('review_count', 0)
                price = m.get('avg_price', 0)
                report.append(f"  {i:2d}. {name:20s} - {rating:4.1f}分 ({reviews:4d}评论, {price:3d}元)")
            report.append("")

        # 按评论数排行
        top_by_reviews = sorted(
            [m for m in merchants if m.get('review_count', 0) > 0],
            key=lambda x: x.get('review_count', 0),
            reverse=True
        )[:10]

        if top_by_reviews:
            report.append(f"🔥 评论数TOP10商家")
            for i, m in enumerate(top_by_reviews, 1):
                name = m.get('name', '未知')[:20]
                rating = m.get('rating', 0)
                reviews = m.get('review_count', 0)
                price = m.get('avg_price', 0)
                report.append(f"  {i:2d}. {name:20s} - {reviews:4d}评论 ({rating:4.1f}分, {price:3d}元)")
            report.append("")

        # 按人均消费排行（从高到低）
        top_by_price = sorted(
            [m for m in merchants if m.get('avg_price', 0) > 0],
            key=lambda x: x.get('avg_price', 0),
            reverse=True
        )[:10]

        if top_by_price:
            report.append(f"💎 人均消费TOP10商家")
            for i, m in enumerate(top_by_price, 1):
                name = m.get('name', '未知')[:20]
                rating = m.get('rating', 0)
                reviews = m.get('review_count', 0)
                price = m.get('avg_price', 0)
                report.append(f"  {i:2d}. {name:20s} - {price:4d}元 ({rating:4.1f}分, {reviews:4d}评论)")
            report.append("")

    def _analyze_sentiment(self, reviews: List[Dict], report: List[str]):
        """分析评论情感（简化版）"""
        if not reviews:
            return

        # 简单的情感分析：基于评分
        positive = [r for r in reviews if r.get('rating', 0) >= 4]
        neutral = [r for r in reviews if 3 <= r.get('rating', 0) < 4]
        negative = [r for r in reviews if r.get('rating', 0) > 0 and r.get('rating', 0) < 3]

        report.append(f"😊 评论情感分析")
        report.append(f"  • 积极评论 (≥4星): {len(positive)}条 ({len(positive)/len(reviews)*100:.1f}%)")
        report.append(f"  • 中性评论 (3.0-3.9星): {len(neutral)}条 ({len(neutral)/len(reviews)*100:.1f}%)")
        report.append(f"  • 消极评论 (<3星): {len(negative)}条 ({len(negative)/len(reviews)*100:.1f}%)")
        report.append("")

    def save_report(self, report: str, filename: str = 'report.txt'):
        """
        保存报告到文件

        Args:
            report: 报告内容
            filename: 文件名

        Returns:
            文件路径
        """
        filepath = os.path.join(self.data_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)

            print(f"报告已保存到 {filepath}")
            return filepath
        except Exception as e:
            print(f"保存报告失败: {e}")
            return None

    def plot_rating_distribution(self, merchants: List[Dict], filename: str = 'rating_dist.png'):
        """
        绘制评分分布图

        Args:
            merchants: 商家数据
            filename: 输出文件名
        """
        ratings = [m.get('rating', 0) for m in merchants if m.get('rating', 0) > 0]

        if not ratings:
            print("没有评分数据可绘制")
            return None

        try:
            # 计算评分分布
            rating_dist = Counter([round(r) for r in ratings])

            # 创建图形
            fig, ax = plt.subplots(figsize=(10, 6))

            scores = sorted(rating_dist.keys())
            counts = [rating_dist[s] for s in scores]

            # 绘制柱状图
            bars = ax.bar(scores, counts, color='skyblue', edgecolor='navy', alpha=0.7)

            # 在柱子上显示数量
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom')

            ax.set_xlabel('评分', fontsize=12)
            ax.set_ylabel('商家数量', fontsize=12)
            ax.set_title('商家评分分布', fontsize=14, fontweight='bold')
            ax.set_xticks(scores)
            ax.grid(axis='y', alpha=0.3)

            plt.tight_layout()

            # 保存图形
            filepath = os.path.join(self.data_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"评分分布图已保存到 {filepath}")
            return filepath
        except Exception as e:
            print(f"绘制评分分布图失败: {e}")
            return None

    def plot_price_distribution(self, merchants: List[Dict], filename: str = 'price_dist.png'):
        """
        绘制人均消费分布图

        Args:
            merchants: 商家数据
            filename: 输出文件名
        """
        prices = [m.get('avg_price', 0) for m in merchants if m.get('avg_price', 0) > 0]

        if not prices:
            print("没有人均消费数据可绘制")
            return None

        try:
            # 创建图形
            fig, ax = plt.subplots(figsize=(12, 6))

            # 绘制直方图
            n, bins, patches = ax.hist(prices, bins=20, color='lightcoral',
                                       edgecolor='darkred', alpha=0.7)

            # 设置X轴标签
            ax.set_xlabel('人均消费 (元)', fontsize=12)
            ax.set_ylabel('商家数量', fontsize=12)
            ax.set_title('商家人均消费分布', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)

            # 在条形图上显示数量
            for i in range(len(n)):
                if n[i] > 0:
                    ax.text((bins[i] + bins[i+1])/2, n[i],
                           f'{int(n[i])}',
                           ha='center', va='bottom')

            plt.tight_layout()

            # 保存图形
            filepath = os.path.join(self.data_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()

            print(f"人均消费分布图已保存到 {filepath}")
            return filepath
        except Exception as e:
            print(f"绘制人均消费分布图失败: {e}")
            return None
