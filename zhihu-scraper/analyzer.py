# -*- coding: utf-8 -*-
"""
数据分析模块 - 生成各类分析报告
"""

from typing import List, Dict, Any, Optional
from collections import Counter, defaultdict
import json


class DataAnalyzer:
    """数据分析类"""

    def __init__(self):
        pass

    def analyze_questions(self, questions: List[Dict]) -> Dict[str, Any]:
        """
        分析问题数据

        Args:
            questions: 问题列表

        Returns:
            分析报告字典
        """
        if not questions:
            return {'error': '没有数据可供分析'}

        report = {
            'summary': {
                'total_questions': len(questions),
                'total_answers': sum(q.get('answer_count', 0) for q in questions),
                'total_followers': sum(q.get('follower_count', 0) for q in questions),
                'total_views': sum(q.get('visited_count', 0) for q in questions),
            },
            'top_questions_by_answers': self._get_top_by_field(
                questions, 'answer_count', '回答数', 10
            ),
            'top_questions_by_followers': self._get_top_by_field(
                questions, 'follower_count', '关注数', 10
            ),
            'top_questions_by_views': self._get_top_by_field(
                questions, 'visited_count', '浏览量', 10
            ),
            'top_authors': self._get_top_authors(questions, 10),
        }

        return report

    def analyze_answers(self, answers: List[Dict]) -> Dict[str, Any]:
        """
        分析回答数据

        Args:
            answers: 回答列表

        Returns:
            分析报告字典
        """
        if not answers:
            return {'error': '没有数据可供分析'}

        report = {
            'summary': {
                'total_answers': len(answers),
                'total_votes': sum(a.get('voteup_count', 0) for a in answers),
                'total_comments': sum(a.get('comment_count', 0) for a in answers),
                'avg_votes_per_answer': sum(a.get('voteup_count', 0) for a in answers) / len(answers),
                'avg_comments_per_answer': sum(a.get('comment_count', 0) for a in answers) / len(answers),
            },
            'top_answers_by_votes': self._get_top_by_field(
                answers, 'voteup_count', '点赞数', 10
            ),
            'top_answers_by_comments': self._get_top_by_field(
                answers, 'comment_count', '评论数', 10
            ),
            'top_authors': self._get_top_authors(answers, 10),
        }

        return report

    def _get_top_by_field(self, data: List[Dict], field: str,
                         field_name: str, top_n: int = 10) -> List[Dict]:
        """
        获取指定字段的前N名

        Args:
            data: 数据列表
            field: 字段名
            field_name: 字段显示名称
            top_n: 前N名

        Returns:
            排名列表
        """
        sorted_data = sorted(data, key=lambda x: x.get(field, 0), reverse=True)[:top_n]

        result = []
        for idx, item in enumerate(sorted_data, 1):
            result.append({
                'rank': idx,
                'title': item.get('title', item.get('content', '')[:50]),
                'author': item.get('author', '未知'),
                field_name: item.get(field, 0),
                'url': item.get('url', ''),
            })

        return result

    def _get_top_authors(self, data: List[Dict], top_n: int = 10) -> List[Dict]:
        """
        获取活跃作者排行

        Args:
            data: 数据列表
            top_n: 前N名

        Returns:
            作者排名列表
        """
        author_stats = defaultdict(lambda: {'count': 0, 'votes': 0})

        for item in data:
            author = item.get('author', '未知')
            author_stats[author]['count'] += 1
            author_stats[author]['votes'] += item.get('voteup_count', 0)

        # 排序
        sorted_authors = sorted(
            author_stats.items(),
            key=lambda x: (x[1]['votes'], x[1]['count']),
            reverse=True
        )[:top_n]

        result = []
        for idx, (author, stats) in enumerate(sorted_authors, 1):
            result.append({
                'rank': idx,
                'author': author,
                'answer_count': stats['count'],
                'total_votes': stats['votes'],
                'avg_votes': stats['votes'] / stats['count'] if stats['count'] > 0 else 0,
            })

        return result

    def generate_text_report(self, report: Dict[str, Any], report_type: str = 'questions') -> str:
        """
        生成文本格式的分析报告

        Args:
            report: 分析报告数据
            report_type: 报告类型 ('questions' | 'answers')

        Returns:
            文本报告字符串
        """
        lines = []
        lines.append("=" * 60)
        lines.append("知乎数据分析报告")
        lines.append("=" * 60)
        lines.append("")

        # 概览
        if 'summary' in report:
            lines.append("📊 数据概览")
            lines.append("-" * 40)
            for key, value in report['summary'].items():
                key_zh = self._translate_key(key)
                if isinstance(value, float):
                    lines.append(f"{key_zh}: {value:.2f}")
                else:
                    lines.append(f"{key_zh}: {value}")
            lines.append("")

        # 热门排行
        if 'top_questions_by_answers' in report:
            lines.append("🔥 热门问题排行（按回答数）")
            lines.append("-" * 40)
            for item in report['top_questions_by_answers']:
                title = item['title'][:30] + '...' if len(item['title']) > 30 else item['title']
                lines.append(f"{item['rank']}. {title}")
                lines.append(f"   作者: {item['author']} | 回答数: {item['回答数']}")
            lines.append("")

        if 'top_questions_by_followers' in report:
            lines.append("⭐ 最受关注问题（按关注数）")
            lines.append("-" * 40)
            for item in report['top_questions_by_followers']:
                title = item['title'][:30] + '...' if len(item['title']) > 30 else item['title']
                lines.append(f"{item['rank']}. {title}")
                lines.append(f"   作者: {item['author']} | 关注数: {item['关注数']}")
            lines.append("")

        if 'top_questions_by_views' in report:
            lines.append("👀 最热门问题（按浏览量）")
            lines.append("-" * 40)
            for item in report['top_questions_by_views']:
                title = item['title'][:30] + '...' if len(item['title']) > 30 else item['title']
                lines.append(f"{item['rank']}. {title}")
                lines.append(f"   作者: {item['author']} | 浏览量: {item['浏览量']}")
            lines.append("")

        if 'top_answers_by_votes' in report:
            lines.append("👍 最受欢迎回答（按点赞数）")
            lines.append("-" * 40)
            for item in report['top_answers_by_votes'][:5]:
                content = item['title'][:30] + '...' if len(item['title']) > 30 else item['title']
                lines.append(f"{item['rank']}. {content}")
                lines.append(f"   作者: {item['author']} | 点赞数: {item['点赞数']}")
            lines.append("")

        # 作者排行
        if 'top_authors' in report:
            lines.append("👤 活跃作者排行")
            lines.append("-" * 40)
            for item in report['top_authors']:
                lines.append(f"{item['rank']}. {item['author']}")
                lines.append(f"   回答数: {item['answer_count']} | 总点赞: {item['total_votes']} | 平均点赞: {item['avg_votes']:.1f}")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)

    def _translate_key(self, key: str) -> str:
        """翻译英文键为中文"""
        translations = {
            'total_questions': '问题总数',
            'total_answers': '回答总数',
            'total_followers': '总关注数',
            'total_views': '总浏览量',
            'total_votes': '总点赞数',
            'total_comments': '总评论数',
            'avg_votes_per_answer': '平均每回答点赞数',
            'avg_comments_per_answer': '平均每回答评论数',
        }
        return translations.get(key, key)

    def generate_comparison_report(self, question_details: Dict, answers: List[Dict]) -> Dict[str, Any]:
        """
        生成问题及其回答的综合分析报告

        Args:
            question_details: 问题详情
            answers: 回答列表

        Returns:
            综合分析报告
        """
        report = {
            'question': {
                'title': question_details.get('title', ''),
                'author': question_details.get('author', ''),
                'answer_count': question_details.get('answer_count', 0),
                'follower_count': question_details.get('follower_count', 0),
                'visited_count': question_details.get('visited_count', 0),
                'created_time': question_details.get('created_time', ''),
                'url': question_details.get('url', ''),
            },
            'answers_analysis': self.analyze_answers(answers) if answers else None,
            'summary': {
                'fetched_answers': len(answers) if answers else 0,
                'total_votes': sum(a.get('voteup_count', 0) for a in answers) if answers else 0,
            }
        }

        return report

    def save_text_report(self, text_report: str, filepath: str):
        """
        保存文本报告到文件

        Args:
            text_report: 文本报告内容
            filepath: 文件路径
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text_report)

        print(f"✓ 文本报告已保存: {filepath}")
