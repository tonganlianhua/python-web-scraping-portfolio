"""
数据导出模块
支持导出为 CSV 和 JSON 格式
"""

import csv
import json
import os
from typing import List, Dict, Optional
import pandas as pd


class DataExporter:
    """数据导出类"""

    def __init__(self, encoding: str = 'utf-8-sig'):
        """
        初始化数据导出器

        Args:
            encoding: 文件编码，默认 utf-8-sig（支持中文）
        """
        self.encoding = encoding

    def export_csv(
        self,
        products: List[Dict],
        filename: str,
        fields: Optional[List[str]] = None
    ) -> bool:
        """
        导出为 CSV 格式

        Args:
            products: 商品数据列表
            filename: 输出文件名
            fields: 指定导出的字段，如果为 None 则导出所有字段

        Returns:
            bool: 是否导出成功
        """
        if not products:
            print("没有数据可导出")
            return False

        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            # 如果没有指定字段，使用所有字段
            if fields is None:
                fields = list(products[0].keys())

            # 使用 pandas 导出（更简单）
            df = pd.DataFrame(products)

            # 只导出指定字段
            if fields:
                df = df[fields]

            # 保存为 CSV
            df.to_csv(filename, index=False, encoding=self.encoding)

            print(f"CSV 文件已导出: {filename}")
            return True

        except Exception as e:
            print(f"导出 CSV 失败: {e}")
            return False

    def export_json(
        self,
        products: List[Dict],
        filename: str,
        indent: int = 2,
        ensure_ascii: bool = False
    ) -> bool:
        """
        导出为 JSON 格式

        Args:
            products: 商品数据列表
            filename: 输出文件名
            indent: JSON 缩进空格数
            ensure_ascii: 是否确保 ASCII 编码（False 支持中文）

        Returns:
            bool: 是否导出成功
        """
        if not products:
            print("没有数据可导出")
            return False

        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            # 保存为 JSON
            with open(filename, 'w', encoding=self.encoding) as f:
                json.dump(products, f, indent=indent, ensure_ascii=ensure_ascii)

            print(f"JSON 文件已导出: {filename}")
            return True

        except Exception as e:
            print(f"导出 JSON 失败: {e}")
            return False

    def export_excel(
        self,
        products: List[Dict],
        filename: str,
        fields: Optional[List[str]] = None,
        sheet_name: str = '商品数据'
    ) -> bool:
        """
        导出为 Excel 格式

        Args:
            products: 商品数据列表
            filename: 输出文件名
            fields: 指定导出的字段
            sheet_name: 工作表名称

        Returns:
            bool: 是否导出成功
        """
        if not products:
            print("没有数据可导出")
            return False

        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            # 转换为 DataFrame
            df = pd.DataFrame(products)

            # 只导出指定字段
            if fields:
                df = df[fields]

            # 保存为 Excel
            df.to_excel(filename, index=False, sheet_name=sheet_name, engine='openpyxl')

            print(f"Excel 文件已导出: {filename}")
            return True

        except Exception as e:
            print(f"导出 Excel 失败: {e}")
            return False

    def export_all(
        self,
        products: List[Dict],
        base_filename: str,
        fields: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """
        导出为所有格式（CSV、JSON、Excel）

        Args:
            products: 商品数据列表
            base_filename: 基础文件名（不带扩展名）
            fields: 指定导出的字段

        Returns:
            Dict[str, bool]: 各格式导出结果
        """
        results = {}

        # 导出 CSV
        results['csv'] = self.export_csv(products, f"{base_filename}.csv", fields)

        # 导出 JSON
        results['json'] = self.export_json(products, f"{base_filename}.json")

        # 导出 Excel
        results['excel'] = self.export_excel(products, f"{base_filename}.xlsx", fields)

        return results

    def filter_fields(
        self,
        products: List[Dict],
        fields: List[str]
    ) -> List[Dict]:
        """
        过滤字段

        Args:
            products: 商品数据列表
            fields: 要保留的字段列表

        Returns:
            List[Dict]: 过滤后的商品数据
        """
        return [{k: v for k, v in product.items() if k in fields} for product in products]

    def get_summary(self, products: List[Dict]) -> Dict:
        """
        获取数据摘要

        Args:
            products: 商品数据列表

        Returns:
            Dict: 数据摘要
        """
        if not products:
            return {
                'total': 0,
                'fields': []
            }

        summary = {
            'total': len(products),
            'fields': list(products[0].keys()),
        }

        # 添加价格统计
        prices = [p.get('price', 0) for p in products if p.get('price')]
        if prices:
            summary['price'] = {
                'min': min(prices),
                'max': max(prices),
                'avg': sum(prices) / len(prices)
            }

        # 添加销量统计
        sales = [p.get('sales', 0) for p in products if p.get('sales')]
        if sales:
            summary['sales'] = {
                'total': sum(sales),
                'avg': sum(sales) / len(sales)
            }

        # 添加店铺数量
        shops = set(p.get('shop_name', '') for p in products)
        summary['unique_shops'] = len(shops)

        return summary
