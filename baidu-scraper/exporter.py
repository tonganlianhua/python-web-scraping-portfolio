#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据导出模块
支持CSV和JSON格式导出
"""

import csv
import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class DataExporter:
    """数据导出类"""
    
    @staticmethod
    def export_to_csv(entries: List[Dict], filename: str, encoding: str = 'utf-8-sig') -> bool:
        """导出为CSV格式"""
        try:
            if not entries:
                print("没有数据可导出")
                return False
                
            # 确保目录存在
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            
            with open(filename, 'w', newline='', encoding=encoding) as f:
                fieldnames = [
                    'title', 'url', 'summary', 'intro',
                    'categories', 'content', 'edit_count',
                    'views', 'labels'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for entry in entries:
                    # 转换列表为字符串
                    row = entry.copy()
                    row['categories'] = '|'.join(entry['categories'])
                    row['labels'] = '|'.join(entry['labels'])
                    # 限制内容长度以避免CSV问题
                    row['content'] = row['content'][:5000]
                    writer.writerow(row)
                    
            print(f"成功导出CSV文件: {filename}")
            return True
            
        except Exception as e:
            print(f"导出CSV失败: {e}")
            return False
            
    @staticmethod
    def export_to_json(entries: List[Dict], filename: str, encoding: str = 'utf-8') -> bool:
        """导出为JSON格式"""
        try:
            if not entries:
                print("没有数据可导出")
                return False
                
            # 确保目录存在
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            
            # 添加导出元数据
            export_data = {
                'export_time': datetime.now().isoformat(),
                'total_entries': len(entries),
                'entries': entries
            }
            
            with open(filename, 'w', encoding=encoding) as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
                
            print(f"成功导出JSON文件: {filename}")
            return True
            
        except Exception as e:
            print(f"导出JSON失败: {e}")
            return False
            
    @staticmethod
    def export_to_csv_and_json(entries: List[Dict], base_filename: str) -> Dict[str, bool]:
        """同时导出CSV和JSON格式"""
        results = {
            'csv': DataExporter.export_to_csv(entries, f"{base_filename}.csv"),
            'json': DataExporter.export_to_json(entries, f"{base_filename}.json")
        }
        return results
        
    @staticmethod
    def load_from_json(filename: str) -> Optional[List[Dict]]:
        """从JSON文件加载数据"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'entries' in data:
                    print(f"从 {filename} 加载了 {len(data['entries'])} 条词条")
                    return data['entries']
                else:
                    print(f"从 {filename} 加载了 {len(data)} 条词条")
                    return data
        except Exception as e:
            print(f"加载JSON失败: {e}")
            return None
