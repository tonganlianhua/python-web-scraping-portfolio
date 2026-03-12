"""
数据导出和分析模块
提供Excel导出、趋势分析等功能
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from typing import List, Dict
import os
from datetime import datetime


class DataExporter:
    """数据导出和分析类"""

    def __init__(self, output_dir: str = "output"):
        """
        初始化导出器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # 设置中文字体
        self._setup_chinese_font()

    def _setup_chinese_font(self):
        """设置中文字体支持"""
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False

    def export_to_excel(self, hot_list: List[Dict], filename: str = None) -> str:
        """
        导出热榜数据到Excel
        
        Args:
            hot_list: 热榜数据列表
            filename: 输出文件名（不含扩展名）
            
        Returns:
            文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"zhihu_hot_{timestamp}"
        
        filepath = os.path.join(self.output_dir, f"{filename}.xlsx")
        
        # 创建DataFrame
        df = pd.DataFrame(hot_list)
        
        # 调整列顺序
        columns_order = ['rank', 'title', 'hot_value', 'link', 'excerpt', 'created_time']
        df = df[columns_order]
        
        # 导出到Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='知乎热榜', index=False)
            
            # 获取sheet对象
            sheet = writer.sheets['知乎热榜']
            
            # 设置列宽
            sheet.column_dimensions['A'].width = 8   # 排名
            sheet.column_dimensions['B'].width = 50  # 标题
            sheet.column_dimensions['C'].width = 15  # 热度
            sheet.column_dimensions['D'].width = 60  # 链接
            sheet.column_dimensions['E'].width = 80  # 摘要
            sheet.column_dimensions['F'].width = 25  # 时间
        
        print(f"数据已导出到: {filepath}")
        return filepath

    def export_comparison_to_excel(self, comparison: List[Dict], filename: str = None) -> str:
        """
        导出热度对比数据到Excel
        
        Args:
            comparison: 对比数据列表
            filename: 输出文件名（不含扩展名）
            
        Returns:
            文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"zhihu_comparison_{timestamp}"
        
        filepath = os.path.join(self.output_dir, f"{filename}.xlsx")
        
        # 创建DataFrame
        df = pd.DataFrame(comparison)
        
        # 调整列顺序
        columns_order = ['title', 'hot_value_1', 'hot_value_2', 'change', 'change_percent', 'link']
        if 'status' in df.columns:
            columns_order.append('status')
        
        df = df[columns_order]
        
        # 导出到Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='热度对比', index=False)
            
            # 获取sheet对象
            sheet = writer.sheets['热度对比']
            
            # 设置列宽
            sheet.column_dimensions['A'].width = 50  # 标题
            sheet.column_dimensions['B'].width = 15  # 热度1
            sheet.column_dimensions['C'].width = 15  # 热度2
            sheet.column_dimensions['D'].width = 15  # 变化
            sheet.column_dimensions['E'].width = 15  # 变化百分比
            sheet.column_dimensions['F'].width = 60  # 链接
        
        print(f"对比数据已导出到: {filepath}")
        return filepath

    def export_detail_to_excel(self, details: List[Dict], filename: str = None) -> str:
        """
        导出话题详情到Excel
        
        Args:
            details: 详情数据列表
            filename: 输出文件名（不含扩展名）
            
        Returns:
            文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"zhihu_details_{timestamp}"
        
        filepath = os.path.join(self.output_dir, f"{filename}.xlsx")
        
        # 创建DataFrame
        df = pd.DataFrame(details)
        
        # 将标签列表转换为字符串
        if 'tags' in df.columns:
            df['tags'] = df['tags'].apply(lambda x: ', '.join(x) if x else '')
        
        # 导出到Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='话题详情', index=False)
            
            # 获取sheet对象
            sheet = writer.sheets['话题详情']
            
            # 设置列宽
            sheet.column_dimensions['A'].width = 60  # URL
            sheet.column_dimensions['B'].width = 15  # 回答数
            sheet.column_dimensions['C'].width = 15  # 关注数
            sheet.column_dimensions['D'].width = 15  # 浏览量
            sheet.column_dimensions['E'].width = 40  # 标签
        
        print(f"详情数据已导出到: {filepath}")
        return filepath

    def generate_trend_chart(self, hot_history: List[List[Dict]], filename: str = None, top_n: int = 10) -> str:
        """
        生成热度趋势图
        
        Args:
            hot_history: 历史热榜数据列表
            filename: 输出文件名（不含扩展名）
            top_n: 显示前N个话题
            
        Returns:
            图片路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"zhihu_trend_{timestamp}"
        
        filepath = os.path.join(self.output_dir, f"{filename}.png")
        
        # 收集所有话题的热度数据
        topic_data = {}
        time_points = []
        
        for idx, hot_list in enumerate(hot_history):
            time_points.append(idx + 1)
            for item in hot_list[:top_n]:
                title = item['title']
                if title not in topic_data:
                    topic_data[title] = []
                topic_data[title].append(item['hot_value'])
        
        # 填充缺失数据
        for title in topic_data:
            while len(topic_data[title]) < len(time_points):
                topic_data[title].append(0)
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # 绘制趋势线
        for title, values in topic_data.items():
            if any(v > 0 for v in values):  # 只绘制有数据的话题
                ax.plot(time_points, values, marker='o', linewidth=2, markersize=6, label=title)
        
        ax.set_xlabel('采集次数', fontsize=12)
        ax.set_ylabel('热度值', fontsize=12)
        ax.set_title('知乎热榜TOP话题热度趋势', fontsize=14, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # 图例放在右侧
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        
        # 调整布局
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"趋势图已保存到: {filepath}")
        return filepath

    def generate_comparison_chart(self, comparison: List[Dict], filename: str = None, top_n: int = 15) -> str:
        """
        生成热度变化对比图
        
        Args:
            comparison: 对比数据列表
            filename: 输出文件名（不含扩展名）
            top_n: 显示变化最大的N个话题
            
        Returns:
            图片路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"zhihu_comparison_chart_{timestamp}"
        
        filepath = os.path.join(self.output_dir, f"{filename}.png")
        
        # 按变化幅度排序
        sorted_comparison = sorted(comparison, key=lambda x: abs(x['change']), reverse=True)[:top_n]
        
        # 提取数据
        titles = [item['title'][:20] + '...' if len(item['title']) > 20 else item['title'] 
                  for item in sorted_comparison]
        changes = [item['change'] for item in sorted_comparison]
        colors = ['green' if c > 0 else 'red' for c in changes]
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # 绘制条形图
        bars = ax.barh(titles, changes, color=colors)
        
        ax.set_xlabel('热度变化', fontsize=12)
        ax.set_title(f'知乎热榜热度变化TOP{top_n}', fontsize=14, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.5, axis='x')
        
        # 在条形上显示数值
        for i, (bar, change) in enumerate(zip(bars, changes)):
            width = bar.get_width()
            offset = 5 if width > 0 else -5
            ax.text(width + offset, bar.get_y() + bar.get_height()/2, 
                   f'{change:+.0f}', 
                   va='center', ha='left' if width > 0 else 'right',
                   fontsize=9)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"对比图已保存到: {filepath}")
        return filepath
