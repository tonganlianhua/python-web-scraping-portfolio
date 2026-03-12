# -*- coding: utf-8 -*-
"""
数据导出模块
"""

import csv
import json
import os
from datetime import datetime
from config import FIELD_MAPPING


class DataExporter:
    """数据导出类"""
    
    def __init__(self, output_dir='data'):
        """
        初始化导出器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def export_to_csv(self, data, filename=None):
        """
        导出数据到CSV文件
        
        Args:
            data: 房源数据列表
            filename: 文件名（不包含扩展名）
            
        Returns:
            文件路径
        """
        if not data:
            print("没有数据可导出")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'lianjia_houses_{timestamp}'
        
        filepath = os.path.join(self.output_dir, f'{filename}.csv')
        
        # 使用中文字段名
        field_order = ['title', 'price', 'unit_price', 'area', 'room_type', 
                      'floor', 'orientation', 'decoration', 'community', 
                      'address', 'city', 'region', 'url']
        
        try:
            with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
                # 写入表头（使用中文名称）
                headers = [FIELD_MAPPING.get(field, field) for field in field_order]
                writer = csv.DictWriter(f, fieldnames=field_order)
                
                # 写入CSV表头
                f.write(','.join(headers) + '\n')
                
                # 写入数据
                for house in data:
                    row = {field: house.get(field, '') for field in field_order}
                    writer.writerow(row)
            
            print(f"成功导出CSV文件: {filepath}")
            print(f"共导出 {len(data)} 条记录")
            return filepath
            
        except Exception as e:
            print(f"导出CSV文件失败: {e}")
            return None
    
    def export_to_json(self, data, filename=None, pretty=True):
        """
        导出数据到JSON文件
        
        Args:
            data: 房源数据列表
            filename: 文件名（不包含扩展名）
            pretty: 是否格式化输出
            
        Returns:
            文件路径
        """
        if not data:
            print("没有数据可导出")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'lianjia_houses_{timestamp}'
        
        filepath = os.path.join(self.output_dir, f'{filename}.json')
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    json.dump(data, f, ensure_ascii=False)
            
            print(f"成功导出JSON文件: {filepath}")
            print(f"共导出 {len(data)} 条记录")
            return filepath
            
        except Exception as e:
            print(f"导出JSON文件失败: {e}")
            return None
    
    def export_all(self, data, filename=None):
        """
        导出数据到CSV和JSON格式
        
        Args:
            data: 房源数据列表
            filename: 文件名（不包含扩展名）
            
        Returns:
            (csv_path, json_path)
        """
        csv_path = self.export_to_csv(data, filename)
        json_path = self.export_to_json(data, filename)
        
        return csv_path, json_path
    
    def get_stats_summary(self, data):
        """
        获取数据统计摘要
        
        Args:
            data: 房源数据列表
            
        Returns:
            统计信息字典
        """
        if not data:
            return {}
        
        stats = {
            'total': len(data),
            'cities': set(),
            'regions': set(),
            'price_range': {'min': float('inf'), 'max': 0},
            'room_types': {},
            'decoration_types': {}
        }
        
        for house in data:
            # 统计城市和区域
            stats['cities'].add(house.get('city', '未知'))
            stats['regions'].add(house.get('region', '未知'))
            
            # 统计价格
            try:
                price = float(house.get('price', 0))
                stats['price_range']['min'] = min(stats['price_range']['min'], price)
                stats['price_range']['max'] = max(stats['price_range']['max'], price)
            except:
                pass
            
            # 统计户型
            room_type = house.get('room_type', '未知')
            stats['room_types'][room_type] = stats['room_types'].get(room_type, 0) + 1
            
            # 统计装修类型
            decoration = house.get('decoration', '未知')
            stats['decoration_types'][decoration] = stats['decoration_types'].get(decoration, 0) + 1
        
        # 转换set为list并排序
        stats['cities'] = sorted(list(stats['cities']))
        stats['regions'] = sorted(list(stats['regions']))
        
        return stats['price_range']['min'] == float('inf'), stats
