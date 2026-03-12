"""
豆瓣电影爬虫 - 工具模块
提供反爬策略、数据导出等工具函数
"""

import random
import time
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class AntiSpider:
    """反爬策略类"""

    # User-Agent 池
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]

    @staticmethod
    def get_random_user_agent() -> str:
        """随机获取一个 User-Agent"""
        return random.choice(AntiSpider.USER_AGENTS)

    @staticmethod
    def get_headers() -> Dict[str, str]:
        """获取请求头"""
        return {
            'User-Agent': AntiSpider.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.douban.com/',
        }

    @staticmethod
    def random_delay(min_sec: float = 0.5, max_sec: float = 2.0):
        """随机延时"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
        return delay


class DataExporter:
    """数据导出类"""

    @staticmethod
    def to_csv(data: List[Dict[str, Any]], filename: str, encoding: str = 'utf-8') -> str:
        """
        导出为 CSV 格式

        Args:
            data: 数据列表
            filename: 文件名
            encoding: 编码格式

        Returns:
            保存的文件路径
        """
        if not data:
            print("警告：没有数据可导出")
            return ""

        # 提取所有字段名
        fieldnames = set()
        for item in data:
            for key in item.keys():
                # 处理嵌套字典，只保存字符串值
                if isinstance(item[key], (str, int, float)):
                    fieldnames.add(key)

        fieldnames = sorted(fieldnames)

        with open(filename, 'w', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                # 只写入简单类型的数据
                row = {k: v for k, v in item.items() if isinstance(v, (str, int, float))}
                writer.writerow(row)

        print(f"✓ 数据已导出到: {filename}")
        return filename

    @staticmethod
    def to_json(data: List[Dict[str, Any]], filename: str, ensure_ascii: bool = False,
                indent: int = 2) -> str:
        """
        导出为 JSON 格式

        Args:
            data: 数据列表
            filename: 文件名
            ensure_ascii: 是否确保 ASCII 编码
            indent: 缩进空格数

        Returns:
            保存的文件路径
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)

        print(f"✓ 数据已导出到: {filename}")
        return filename


class DataAnalyzer:
    """数据分析类"""

    @staticmethod
    def analyze_rating_distribution(movies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析评分分布"""
        ratings = [m.get('rating', 0) for m in movies if m.get('rating')]
        if not ratings:
            return {}

        df = pd.DataFrame({'rating': ratings})

        # 统计评分分布
        rating_stats = {
            'count': len(ratings),
            'mean': float(df['rating'].mean()),
            'median': float(df['rating'].median()),
            'std': float(df['rating'].std()),
            'min': float(df['rating'].min()),
            'max': float(df['rating'].max()),
        }

        # 评分区间统计
        bins = [0, 6, 7, 8, 9, 10]
        labels = ['<6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0', '≥9.0']
        df['rating_range'] = pd.cut(df['rating'], bins=bins, labels=labels, include_lowest=True)
        rating_dist = df['rating_range'].value_counts().sort_index().to_dict()

        return {
            'stats': rating_stats,
            'distribution': {str(k): int(v) for k, v in rating_dist.items()}
        }

    @staticmethod
    def analyze_year_distribution(movies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析年份分布"""
        years = [m.get('year', 0) for m in movies if m.get('year')]
        if not years:
            return {}

        df = pd.DataFrame({'year': years})

        # 年份统计
        year_stats = {
            'count': len(years),
            'earliest': int(df['year'].min()),
            'latest': int(df['year'].max()),
        }

        # 按年代统计
        df['decade'] = (df['year'] // 10) * 10
        decade_dist = df['decade'].value_counts().sort_index().to_dict()

        return {
            'stats': year_stats,
            'by_decade': {str(int(k)): int(v) for k, v in decade_dist.items()}
        }

    @staticmethod
    def analyze_director_ranking(movies: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
        """分析导演排行"""
        directors = []
        for movie in movies:
            director_list = movie.get('directors', [])
            if isinstance(director_list, list):
                for director in director_list:
                    directors.append({'name': director, 'rating': movie.get('rating', 0)})

        if not directors:
            return []

        df = pd.DataFrame(directors)

        # 统计每位导演的作品数和平均评分
        director_stats = df.groupby('name').agg({
            'name': 'count',
            'rating': 'mean'
        }).rename(columns={'name': 'count', 'rating': 'avg_rating'})

        # 按作品数排序
        director_stats = director_stats.sort_values('count', ascending=False).head(top_n)

        result = []
        for director, row in director_stats.iterrows():
            result.append({
                'director': director,
                'count': int(row['count']),
                'avg_rating': round(float(row['avg_rating']), 2)
            })

        return result

    @staticmethod
    def generate_report(movies: List[Dict[str, Any]], output_dir: str = '.') -> Dict[str, str]:
        """
        生成数据分析报告

        Args:
            movies: 电影数据
            output_dir: 输出目录

        Returns:
            生成的报告文件路径
        """
        if not movies:
            print("警告：没有数据可分析")
            return {}

        print("\n=== 生成数据分析报告 ===")

        # 分析评分分布
        rating_analysis = DataAnalyzer.analyze_rating_distribution(movies)
        print(f"✓ 评分分布分析完成: 平均 {rating_analysis.get('stats', {}).get('mean', 0):.2f}")

        # 分析年份分布
        year_analysis = DataAnalyzer.analyze_year_distribution(movies)
        print(f"✓ 年份分布分析完成: {year_analysis.get('stats', {}).get('earliest', 0)} - {year_analysis.get('stats', {}).get('latest', 0)}")

        # 分析导演排行
        director_ranking = DataAnalyzer.analyze_director_ranking(movies, top_n=10)
        print(f"✓ 导演排行分析完成: Top {len(director_ranking)}")

        # 保存分析报告
        report = {
            'summary': {
                'total_movies': len(movies),
                'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            },
            'rating_analysis': rating_analysis,
            'year_analysis': year_analysis,
            'director_ranking': director_ranking
        }

        report_file = f'{output_dir}/analysis_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"✓ 分析报告已保存: {report_file}")

        # 生成可视化图表
        DataAnalyzer._generate_charts(movies, output_dir)

        return {'report': report_file, 'charts': f'{output_dir}/charts'}

    @staticmethod
    def _generate_charts(movies: List[Dict[str, Any]], output_dir: str):
        """生成可视化图表"""
        try:
            # 创建图表目录
            import os
            charts_dir = f'{output_dir}/charts'
            os.makedirs(charts_dir, exist_ok=True)

            # 1. 评分分布直方图
            ratings = [m.get('rating', 0) for m in movies if m.get('rating')]
            if ratings:
                plt.figure(figsize=(10, 6))
                plt.hist(ratings, bins=20, edgecolor='black', alpha=0.7)
                plt.xlabel('评分')
                plt.ylabel('电影数量')
                plt.title('豆瓣电影 Top250 评分分布')
                plt.grid(True, alpha=0.3)
                plt.savefig(f'{charts_dir}/rating_distribution.png', dpi=300, bbox_inches='tight')
                plt.close()
                print(f"✓ 评分分布图已保存")

            # 2. 年份分布柱状图
            years = [m.get('year', 0) for m in movies if m.get('year')]
            if years:
                plt.figure(figsize=(12, 6))
                df = pd.DataFrame({'year': years})
                year_counts = df['year'].value_counts().sort_index()
                plt.bar(year_counts.index, year_counts.values, edgecolor='black', alpha=0.7)
                plt.xlabel('年份')
                plt.ylabel('电影数量')
                plt.title('豆瓣电影 Top250 年份分布')
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3, axis='y')
                plt.tight_layout()
                plt.savefig(f'{charts_dir}/year_distribution.png', dpi=300, bbox_inches='tight')
                plt.close()
                print(f"✓ 年份分布图已保存")

            # 3. Top 10 导演作品数
            director_ranking = DataAnalyzer.analyze_director_ranking(movies, top_n=10)
            if director_ranking:
                directors = [d['director'] for d in director_ranking]
                counts = [d['count'] for d in director_ranking]

                plt.figure(figsize=(12, 6))
                plt.barh(directors, counts, edgecolor='black', alpha=0.7)
                plt.xlabel('作品数')
                plt.ylabel('导演')
                plt.title('Top 10 导演作品数排行')
                plt.grid(True, alpha=0.3, axis='x')
                plt.tight_layout()
                plt.savefig(f'{charts_dir}/director_ranking.png', dpi=300, bbox_inches='tight')
                plt.close()
                print(f"✓ 导演排行图已保存")

        except Exception as e:
            print(f"⚠ 生成图表时出错: {e}")
