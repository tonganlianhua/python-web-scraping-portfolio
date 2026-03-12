#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据分析模块
生成统计分析报告
"""

from typing import List, Dict
from collections import Counter
import json


class DataAnalyzer:
    """数据分析类"""
    
    @staticmethod
    def generate_report(entries: List[Dict]) -> Dict:
        """生成完整分析报告"""
        if not entries:
            return {"error": "没有数据可分析"}
            
        report = {
            "summary": DataAnalyzer._get_summary(entries),
            "category_distribution": DataAnalyzer._analyze_categories(entries),
            "popular_entries": DataAnalyzer._get_popular_entries(entries),
            "edit_statistics": DataAnalyzer._analyze_edits(entries),
            "content_statistics": DataAnalyzer._analyze_content(entries)
        }
        
        return report
        
    @staticmethod
    def _get_summary(entries: List[Dict]) -> Dict:
        """获取数据摘要"""
        total_entries = len(entries)
        total_views = sum(entry.get('views', 0) for entry in entries)
        total_edits = sum(entry.get('edit_count', 0) for entry in entries)
        avg_views = total_views / total_entries if total_entries > 0 else 0
        avg_edits = total_edits / total_entries if total_entries > 0 else 0
        
        return {
            "total_entries": total_entries,
            "total_views": total_views,
            "total_edits": total_edits,
            "average_views": round(avg_views, 2),
            "average_edits": round(avg_edits, 2)
        }
        
    @staticmethod
    def _analyze_categories(entries: List[Dict]) -> Dict:
        """分析分类分布"""
        all_categories = []
        for entry in entries:
            all_categories.extend(entry.get('categories', []))
            
        category_counter = Counter(all_categories)
        
        return {
            "unique_categories": len(category_counter),
            "category_distribution": dict(category_counter.most_common()),
            "top_10_categories": category_counter.most_common(10)
        }
        
    @staticmethod
    def _get_popular_entries(entries: List[Dict], top_n: int = 10) -> List[Dict]:
        """获取热门词条（按浏览量排行）"""
        sorted_entries = sorted(
            entries,
            key=lambda x: x.get('views', 0),
            reverse=True
        )[:top_n]
        
        return [
            {
                "rank": i + 1,
                "title": entry['title'],
                "views": entry.get('views', 0),
                "categories": entry.get('categories', [])
            }
            for i, entry in enumerate(sorted_entries)
        ]
        
    @staticmethod
    def _analyze_edits(entries: List[Dict]) -> Dict:
        """分析编辑次数统计"""
        edit_counts = [entry.get('edit_count', 0) for entry in entries]
        edit_counts.sort(reverse=True)
        
        return {
            "most_edited": edit_counts[:10] if edit_counts else [],
            "average_edits": round(sum(edit_counts) / len(edit_counts), 2) if edit_counts else 0,
            "total_edits": sum(edit_counts)
        }
        
    @staticmethod
    def _analyze_content(entries: List[Dict]) -> Dict:
        """分析内容统计"""
        content_lengths = [len(entry.get('content', '')) for entry in entries]
        
        return {
            "total_characters": sum(content_lengths),
            "average_length": round(sum(content_lengths) / len(content_lengths), 2) if content_lengths else 0,
            "longest_entry": max(content_lengths) if content_lengths else 0,

            "shortest_entry": min(content_lengths) if content_lengths else 0
        }
        
    @staticmethod
    def print_report(report: Dict):
        """打印分析报告"""
        print("\n" + "="*80)
        print("百度百科词条数据分析报告")
        print("="*80)
        
        # 打印摘要
        summary = report.get('summary', {})
        print("\n📊 数据摘要")
        print("-" * 40)
        print(f"词条总数: {summary.get('total_entries', 0)}")
        print(f"总浏览量: {summary.get('total_views', 0):,}")
        print(f"总编辑次数: {summary.get('total_edits', 0):,}")
        print(f"平均浏览量: {summary.get('average_views', 0):,.2f}")
        print(f"平均编辑次数: {summary.get('average_edits', 0):,.2f}")
        
        # 打印分类分布
        cat_dist = report.get('category_distribution', {})
        print("\n🏷️  分类分布")
        print("-" * 40)
        print(f"分类总数: {cat_dist.get('unique_categories', 0)}")
        print("\nTop 10 分类:")
        for cat, count in cat_dist.get('top_10_categories', []):
            print(f"  {cat}: {count}")
            
        # 打印热门词条
        popular = report.get('popular_entries', [])
        print("\n🔥 热门词条 (按浏览量)")
        print("-" * 40)
        for entry in popular[:5]:
            print(f"{entry['rank']}. {entry['title']}")
            print(f"   浏览量: {entry['views']:,}")
            
        # 打印编辑统计
        edit_stats = report.get('edit_statistics', {})
        print("\n✏️  编辑统计")
        print("-" * 40)
        print(f"平均编辑次数: {edit_stats.get('average_edits', 0):,.2f}")
        print(f"总编辑次数: {edit_stats.get('total_edits', 0):,}")
        
        # 打印内容统计
        content_stats = report.get('content_statistics', {})
        print("\n📝 内容统计")
        print("-" * 40)
        print(f"总字符数: {content_stats.get('total_characters', 0):,}")
        print(f"平均长度: {content_stats.get('average_length', 0):,.2f}")
        print(f"最长词条: {content_stats.get('longest_entry', 0):,} 字符")
        
        print("\n" + "="*80)
        
    @staticmethod
    def save_report_to_file(report: Dict, filename: str):
        """保存报告到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n报告已保存到: {filename}")
        except Exception as e:
            print(f"保存报告失败: {e}")
