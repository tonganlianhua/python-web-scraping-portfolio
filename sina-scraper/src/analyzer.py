"""
数据分析模块
生成微博数据统计报告
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

sns.set_style("whitegrid")


class DataAnalyzer:
    """数据分析器"""

    def __init__(self, output_dir: str = 'data'):
        """
        初始化分析器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def analyze_users(self, users: List) -> Dict:
        """
        分析用户数据

        Args:
            users: 用户列表

        Returns:
            分析结果字典
        """
        if not users:
            logger.warning("No user data to analyze")
            return {}

        # 转换为DataFrame
        data = []
        for user in users:
            if hasattr(user, 'to_dict'):
                data.append(user.to_dict())
            elif isinstance(user, dict):
                data.append(user)

        df = pd.DataFrame(data)

        analysis = {
            'total_users': len(users),
            'verified_users': df['verified'].sum() if 'verified' in df.columns else 0,
            'verified_rate': (df['verified'].sum() / len(users) * 100) if 'verified' in df.columns else 0,
        }

        # 统计字段
        numeric_fields = ['fans_count', 'follow_count', 'weibo_count']
        for field in numeric_fields:
            if field in df.columns:
                analysis[f'{field}_total'] = df[field].sum()
                analysis[f'{field}_avg'] = df[field].mean()
                analysis[f'{field}_max'] = df[field].max()
                analysis[f'{field}_min'] = df[field].min()

        # Top用户排行
        if 'fans_count' in df.columns and 'username' in df.columns:
            top_fans = df.nlargest(10, 'fans_count')[['username', 'fans_count']]
            analysis['top_fans_users'] = top_fans.to_dict('records')

        if 'weibo_count' in df.columns and 'username' in df.columns:
            top_weibo = df.nlargest(10, 'weibo_count')[['username', 'weibo_count']]
            analysis['top_weibo_users'] = top_weibo.to_dict('records')

        return analysis

    def analyze_posts(self, posts: List) -> Dict:
        """
        分析微博帖子数据

        Args:
            posts: 帖子列表

        Returns:
            分析结果字典
        """
        if not posts:
            logger.warning("No post data to analyze")
            return {}

        # 转换为DataFrame
        data = []
        for post in posts:
            if hasattr(post, 'to_dict'):
                data.append(post.to_dict())
            elif isinstance(post, dict):
                data.append(post)

        df = pd.DataFrame(data)

        analysis = {
            'total_posts': len(posts),
        }

        # 统计互动数据
        interaction_fields = ['likes', 'comments', 'reposts']
        for field in interaction_fields:
            if field in df.columns:
                analysis[f'{field}_total'] = df[field].sum()
                analysis[f'{field}_avg'] = df[field].mean()
                analysis[f'{field}_max'] = df[field].max()

        # 转发统计
        if 'is_repost' in df.columns:
            analysis['original_posts'] = (~df['is_repost']).sum()
            analysis['repost_posts'] = df['is_repost'].sum()
            analysis['repost_rate'] = (df['is_repost'].sum() / len(posts) * 100)

        # 话题统计
        if 'topics' in df.columns:
            all_topics = []
            for topics in df['topics'].dropna():
                if isinstance(topics, list):
                    all_topics.extend(topics)
                elif isinstance(topics, str):
                    all_topics.append(topics)

            from collections import Counter
            topic_counter = Counter(all_topics)
            analysis['total_topics'] = len(topic_counter)
            analysis['top_topics'] = topic_counter.most_common(20)

        # 热门微博排行
        if 'likes' in df.columns and 'username' in df.columns and 'content' in df.columns:
            df['content_preview'] = df['content'].str.slice(0, 50)
            hot_posts = df.nlargest(10, 'likes')[['username', 'content_preview', 'likes', 'comments', 'reposts']]
            analysis['hot_posts'] = hot_posts.to_dict('records')

        return analysis

    def generate_report(
        self,
        users: List = None,
        posts: List = None,
        filename: str = None
    ) -> str:
        """
        生成完整分析报告

        Args:
            users: 用户列表
            posts: 帖子列表
            filename: 报告文件名

        Returns:
            报告文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'weibo_analysis_report_{timestamp}'

        if not filename.endswith('.txt'):
            filename = filename + '.txt'

        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("新浪微博数据分析报告\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            if users:
                f.write("一、用户数据分析\n")
                f.write("-" * 80 + "\n")
                user_analysis = self.analyze_users(users)
                self._write_user_analysis(f, user_analysis)
                f.write("\n")

            if posts:
                f.write("二、微博帖子分析\n")
                f.write("-" * 80 + "\n")
                post_analysis = self.analyze_posts(posts)
                self._write_post_analysis(f, post_analysis)
                f.write("\n")

        logger.info(f"Report generated: {filepath}")
        return filepath

    def _write_user_analysis(self, f, analysis: Dict):
        """写入用户分析"""
        f.write(f"总用户数: {analysis.get('total_users', 0)}\n")
        f.write(f"认证用户数: {analysis.get('verified_users', 0)}\n")
        f.write(f"认证率: {analysis.get('verified_rate', 0):.2f}%\n\n")

        f.write("粉丝统计:\n")
        f.write(f"  总粉丝数: {analysis.get('fans_count_total', 0):,}\n")
        f.write(f"  平均粉丝数: {analysis.get('fans_count_avg', 0):.2f}\n")
        f.write(f"  最高粉丝数: {analysis.get('fans_count_max', 0):,}\n\n")

        f.write("Top 10 粉丝用户:\n")
        if 'top_fans_users' in analysis:
            for i, user in enumerate(analysis['top_fans_users'], 1):
                f.write(f"  {i}. {user['username']}: {user['fans_count']:,} 粉丝\n")
        f.write("\n")

    def _write_post_analysis(self, f, analysis: Dict):
        """写入帖子分析"""
        f.write(f"总微博数: {analysis.get('total_posts', 0)}\n")
        f.write(f"原创微博: {analysis.get('original_posts', 0)}\n")
        f.write(f"转发微博: {analysis.get('repost_posts', 0)}\n")
        f.write(f"转发率: {analysis.get('repost_rate', 0):.2f}%\n\n")

        f.write("互动统计:\n")
        f.write(f"  总点赞数: {analysis.get('likes_total', 0):,}\n")
        f.write(f"  总评论数: {analysis.get('comments_total', 0):,}\n")
        f.write(f"  总转发数: {analysis.get('reposts_total', 0):,}\n")
        f.write(f"  平均点赞数: {analysis.get('likes_avg', 0):.2f}\n\n")

        f.write("热门话题 Top 10:\n")
        if 'top_topics' in analysis:
            for i, (topic, count) in enumerate(analysis['top_topics'][:10], 1):
                f.write(f"  {i}. #{topic}: {count} 次\n")
        f.write("\n")

    def plot_user_fans(self, users: List, save_path: str = None) -> str:
        """
        绘制用户粉丝分布图

        Args:
            users: 用户列表
            save_path: 保存路径

        Returns:
            图片文件路径
        """
        if not users:
            logger.warning("No user data to plot")
            return None

        # 转换为DataFrame
        data = []
        for user in users:
            if hasattr(user, 'to_dict'):
                item = user.to_dict()
            elif isinstance(user, dict):
                item = user
            else:
                continue
            if 'fans_count' in item and 'username' in item:
                data.append({'username': item['username'], 'fans_count': item['fans_count']})

        if not data:
            logger.warning("No valid fan count data")
            return None

        df = pd.DataFrame(data).nlargest(20, 'fans_count')

        plt.figure(figsize=(12, 8))
        plt.barh(df['username'], df['fans_count'])
        plt.xlabel('粉丝数', fontsize=12)
        plt.ylabel('用户名', fontsize=12)
        plt.title('Top 20 用户粉丝数排行', fontsize=16)
        plt.tight_layout()

        if save_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.output_dir, f'user_fans_{timestamp}.png')

        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Plot saved: {save_path}")
        return save_path

    def plot_post_interaction(self, posts: List, save_path: str = None) -> str:
        """
        绘制微博互动分布图

        Args:
            posts: 帖子列表
            save_path: 保存路径

        Returns:
            图片文件路径
        """
        if not posts:
            logger.warning("No post data to plot")
            return None

        # 转换为DataFrame
        data = []
        for post in posts:
            if hasattr(post, 'to_dict'):
                item = post.to_dict()
            elif isinstance(post, dict):
                item = post
            else:
                continue
            data.append({
                'likes': item.get('likes', 0),
                'comments': item.get('comments', 0),
                'reposts': item.get('reposts', 0)
            })

        if not data:
            return None

        df = pd.DataFrame(data)

        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        # 点赞分布
        axes[0].hist(df['likes'], bins=50, color='skyblue', edgecolor='black')
        axes[0].set_xlabel('点赞数')
        axes[0].set_ylabel('频数')
        axes[0].set_title('点赞数分布')

        # 评论分布
        axes[1].hist(df['comments'], bins=50, color='lightgreen', edgecolor='black')
        axes[1].set_xlabel('评论数')
        axes[1].set_ylabel('频数')
        axes[1].set_title('评论数分布')

        # 转发分布
        axes[2].hist(df['reposts'], bins=50, color='lightcoral', edgecolor='black')
        axes[2].set_xlabel('转发数')
        axes[2].set_ylabel('频数')
        axes[2].set_title('转发数分布')

        plt.tight_layout()

        if save_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.output_dir, f'post_interaction_{timestamp}.png')

        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Plot saved: {save_path}")
        return save_path
