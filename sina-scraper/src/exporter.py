"""
数据导出模块
支持导出为CSV和JSON格式
"""

import json
import csv
import os
from typing import List, Dict, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataExporter:
    """数据导出器"""

    def __init__(self, output_dir: str = 'data'):
        """
        初始化导出器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export_to_json(
        self,
        data: List[Union[Dict, object]],
        filename: str = None,
        pretty: bool = True
    ) -> str:
        """
        导出为JSON格式

        Args:
            data: 数据列表（字典或对象）
            filename: 文件名（不含扩展名）
            pretty: 是否格式化输出

        Returns:
            输出文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'weibo_data_{timestamp}'

        filepath = os.path.join(self.output_dir, f'{filename}.json')

        # 转换对象为字典
        processed_data = []
        for item in data:
            if hasattr(item, 'to_dict'):
                processed_data.append(item.to_dict())
            elif isinstance(item, dict):
                processed_data.append(item)
            else:
                logger.warning(f"Unexpected data type: {type(item)}")

        with open(filepath, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)
            else:
                json.dump(processed_data, f, ensure_ascii=False)

        logger.info(f"Exported {len(processed_data)} items to {filepath}")
        return filepath

    def export_to_csv(
        self,
        data: List[Union[Dict, object]],
        filename: str = None,
        encoding: str = 'utf-8-sig'
    ) -> str:
        """
        导出为CSV格式

        Args:
            data: 数据列表（字典或对象）
            filename: 文件名（不含扩展名）
            encoding: 编码格式

        Returns:
            输出文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'weibo_data_{timestamp}'

        filepath = os.path.join(self.output_dir, f'{filename}.csv')

        if not data:
            logger.warning("No data to export")
            return filepath

        # 转换对象为字典
        processed_data = []
        for item in data:
            if hasattr(item, 'to_dict'):
                processed_data.append(item.to_dict())
            elif isinstance(item, dict):
                processed_data.append(item)
            else:
                logger.warning(f"Unexpected data type: {type(item)}")

        # 获取所有字段名
        fieldnames = set()
        for item in processed_data:
            fieldnames.update(item.keys())
        fieldnames = sorted(fieldnames)

        # 写入CSV
        with open(filepath, 'w', encoding=encoding, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for item in processed_data:
                # 处理复杂类型（列表转为字符串）
                row = {}
                for key, value in item.items():
                    if isinstance(value, (list, dict)):
                        row[key] = json.dumps(value, ensure_ascii=False)
                    else:
                        row[key] = value
                writer.writerow(row)

        logger.info(f"Exported {len(processed_data)} items to {filepath}")
        return filepath

    def export_users(
        self,
        users: List,
        filename: str = None,
        format: str = 'json'
    ) -> str:
        """
        导出用户数据

        Args:
            users: 用户列表
            filename: 文件名
            format: 格式 (json/csv)

        Returns:
            输出文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'weibo_users_{timestamp}'

        if format.lower() == 'json':
            return self.export_to_json(users, filename)
        elif format.lower() == 'csv':
            return self.export_to_csv(users, filename)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def export_posts(
        self,
        posts: List,
        filename: str = None,
        format: str = 'json'
    ) -> str:
        """
        导出微博数据

        Args:
            posts: 微博列表
            filename: 文件名
            format: 格式 (json/csv)

        Returns:
            输出文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'weibo_posts_{timestamp}'

        if format.lower() == 'json':
            return self.export_to_json(posts, filename)
        elif format.lower() == 'csv':
            return self.export_to_csv(posts, filename)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def export_summary(
        self,
        summary: Dict,
        filename: str = None
    ) -> str:
        """
        导出摘要统计

        Args:
            summary: 摘要字典
            filename: 文件名

        Returns:
            输出文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'weibo_summary_{timestamp}'

        filepath = os.path.join(self.output_dir, f'{filename}.json')

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        logger.info(f"Exported summary to {filepath}")
        return filepath
