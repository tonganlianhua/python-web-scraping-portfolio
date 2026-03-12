"""
数据导出模块
支持导出为CSV、Excel等格式
"""

import pandas as pd
import os
from datetime import datetime
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class DataExporter:
    """数据导出类"""

    def __init__(self, output_dir: str = "output"):
        """
        初始化导出器

        Args:
            output_dir: 输出目录（默认"output"）
        """
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"创建输出目录: {self.output_dir}")

    def export_to_csv(
        self,
        data: List[Dict],
        filename: str = None,
        encoding: str = 'utf-8-sig'
    ) -> str:
        """
        导出为CSV格式

        Args:
            data: 职位数据列表
            filename: 文件名（可选，默认自动生成）
            encoding: 编码（默认utf-8-sig）

        Returns:
            导出文件的完整路径
        """
        if not data:
            logger.warning("没有数据可导出")
            return ""

        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"jobs_{timestamp}.csv"

        # 确保文件扩展名
        if not filename.endswith('.csv'):
            filename += '.csv'

        filepath = os.path.join(self.output_dir, filename)

        try:
            # 转换为DataFrame
            df = pd.DataFrame(data)

            # 导出CSV
            df.to_csv(filepath, index=False, encoding=encoding)

            logger.info(f"成功导出CSV文件: {filepath} ({len(data)} 条记录)")
            return filepath

        except Exception as e:
            logger.error(f"导出CSV失败: {e}")
            return ""

    def export_to_excel(
        self,
        data: List[Dict],
        filename: str = None,
        sheet_name: str = "职位信息"
    ) -> str:
        """
        导出为Excel格式

        Args:
            data: 职位数据列表
            filename: 文件名（可选，默认自动生成）
            sheet_name: 工作表名称

        Returns:
            导出文件的完整路径
        """
        if not data:
            logger.warning("没有数据可导出")
            return ""

        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"jobs_{timestamp}.xlsx"

        # 确保文件扩展名
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'

        filepath = os.path.join(self.output_dir, filename)

        try:
            # 转换为DataFrame
            df = pd.DataFrame(data)

            # 导出Excel
            df.to_excel(filepath, index=False, sheet_name=sheet_name)

            logger.info(f"成功导出Excel文件: {filepath} ({len(data)} 条记录)")
            return filepath

        except Exception as e:
            logger.error(f"导出Excel失败: {e}")
            return ""

    def export_to_json(
        self,
        data: List[Dict],
        filename: str = None,
        indent: int = 2
    ) -> str:
        """
        导出为JSON格式

        Args:
            data: 职位数据列表
            filename: 文件名（可选，默认自动生成）
            indent: 缩进空格数

        Returns:
            导出文件的完整路径
        """
        if not data:
            logger.warning("没有数据可导出")
            return ""

        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"jobs_{timestamp}.json"

        # 确保文件扩展名
        if not filename.endswith('.json'):
            filename += '.json'

        filepath = os.path.join(self.output_dir, filename)

        try:
            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)

            logger.info(f"成功导出JSON文件: {filepath} ({len(data)} 条记录)")
            return filepath

        except Exception as e:
            logger.error(f"导出JSON失败: {e}")
            return ""

    def get_statistics(self, data: List[Dict]) -> Dict:
        """
        获取数据统计信息

        Args:
            data: 职位数据列表

        Returns:
            统计信息字典
        """
        if not data:
            return {}

        try:
            df = pd.DataFrame(data)
            stats = {
                '总职位数': len(df),
            }

            # 薪资分布
            if '薪资' in df.columns:
                stats['薪资分布'] = df['薪资'].value_counts().to_dict()

            # 公司分布
            if '公司' in df.columns:
                stats['公司数量'] = df['公司'].nunique()
                stats['公司排行'] = df['公司'].value_counts().head(10).to_dict()

            # 地区分布
            if '地点' in df.columns:
                stats['地区数量'] = df['地点'].nunique()
                stats['地区分布'] = df['地点'].value_counts().head(10).to_dict()

            # 经验要求分布
            if '经验要求' in df.columns:
                stats['经验要求分布'] = df['经验要求'].value_counts().to_dict()

            # 学历要求分布
            if '学历要求' in df.columns:
                stats['学历要求分布'] = df['学历要求'].value_counts().to_dict()

            return stats

        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return {}


def main():
    """主函数 - 用于测试"""
    # 模拟数据
    test_data = [
        {
            '职位名称': 'Python开发工程师',
            '薪资': '15-25K',
            '公司': '科技有限公司',
            '地点': '北京·朝阳区',
            '经验要求': '3-5年',
            '学历要求': '本科',
            '职位标签': 'Python|Django|MySQL',
            '爬取时间': '2026-03-12 10:00:00'
        },
        {
            '职位名称': 'Java开发工程师',
            '薪资': '20-30K',
            '公司': '互联网公司',
            '地点': '上海·浦东新区',
            '经验要求': '5-10年',
            '学历要求': '本科',
            '职位标签': 'Java|Spring|MySQL',
            '爬取时间': '2026-03-12 10:00:00'
        },
    ]

    exporter = DataExporter()

    # 导出测试
    print("导出CSV...")
    csv_path = exporter.export_to_csv(test_data, filename='test_jobs.csv')
    print(f"CSV文件: {csv_path}")

    print("\n导出Excel...")
    excel_path = exporter.export_to_excel(test_data, filename='test_jobs.xlsx')
    print(f"Excel文件: {excel_path}")

    print("\n导出JSON...")
    json_path = exporter.export_to_json(test_data, filename='test_jobs.json')
    print(f"JSON文件: {json_path}")

    print("\n统计信息:")
    stats = exporter.get_statistics(test_data)
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
