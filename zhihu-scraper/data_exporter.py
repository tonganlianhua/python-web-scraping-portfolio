# -*- coding: utf-8 -*-
"""
数据导出模块 - 支持CSV和JSON格式
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from config import OUTPUT_DIR, DATA_DIR


class DataExporter:
    """数据导出类"""

    def __init__(self, output_dir: str = OUTPUT_DIR):
        self.output_dir = Path(output_dir)
        self.data_dir = Path(DATA_DIR)
        self._ensure_dirs()

    def _ensure_dirs(self):
        """确保输出目录存在"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    def export_to_json(self, data: Any, filename: str = None,
                      subfolder: str = None) -> str:
        """
        导出数据到JSON文件

        Args:
            data: 要导出的数据（列表或字典）
            filename: 文件名（不含扩展名）
            subfolder: 子文件夹名称

        Returns:
            导出文件的完整路径
        """
        if filename is None:
            filename = f"data_{self._get_timestamp()}"

        if subfolder:
            output_path = self.output_dir / subfolder
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = self.output.data_dir

        filepath = output_path / f"{filename}.json"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✓ 数据已导出到: {filepath}")
        return str(filepath)

    def export_to_csv(self, data: List[Dict], filename: str = None,
                     subfolder: str = None) -> str:
        """
        导出数据到CSV文件

        Args:
            data: 要导出的数据（字典列表）
            filename: 文件名（不含扩展名）
            subfolder: 子文件夹名称

        Returns:
            导出文件的完整路径
        """
        if not data:
            print("警告: 没有数据可导出")
            return ""

        if filename is None:
            filename = f"data_{self._get_timestamp()}"

        if subfolder:
            output_path = self.output_dir / subfolder
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = self.data_dir

        filepath = output_path / f"{filename}.csv"

        # 获取所有字段名
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        fieldnames = sorted(fieldnames)

        # 写入CSV
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(data)

        print(f"✓ 数据已导出到: {filepath}")
        return str(filepath)

    def export_questions(self, questions: List[Dict], prefix: str = 'questions') -> Dict[str, str]:
        """
        导出问题数据到多种格式

        Args:
            questions: 问题数据列表
            prefix: 文件名前缀

        Returns:
            包含各格式文件路径的字典
        """
        timestamp = self._get_timestamp()
        base_filename = f"{prefix}_{timestamp}"

        results = {}

        # 导出JSON
        json_path = self.export_to_json(questions, base_filename)
        results['json'] = json_path

        # 导出CSV
        csv_path = self.export_to_csv(questions, base_filename)
        results['csv'] = csv_path

        return results

    def export_answers(self, answers: List[Dict], question_id: str = None) -> Dict[str, str]:
        """
        导出回答数据

        Args:
            answers: 回答数据列表
            question_id: 问题ID（用于文件命名）

        Returns:
            包含各格式文件路径的字典
        """
        timestamp = self._get_timestamp()
        prefix = f"answers_{question_id}_{timestamp}" if question_id else f"answers_{timestamp}"

        # 创建问答子文件夹
        folder_name = f"question_{question_id}" if question_id else "answers"

        results = {}

        # 导出JSON
        json_path = self.export_to_json(answers, prefix, subfolder=folder_name)
        results['json'] = json_path

        # 导出CSV
        csv_path = self.export_to_csv(answers, prefix, subfolder=folder_name)
        results['csv'] = csv_path

        return results

    def export_analysis_report(self, report: Dict, question_id: str = None) -> str:
        """
        导出分析报告

        Args:
            report: 分析报告数据
            question_id: 问题ID

        Returns:
            报告文件路径
        """
        timestamp = self._get_timestamp()
        if question_id:
            filename = f"analysis_{question_id}_{timestamp}"
            subfolder = f"question_{question_id}"
        else:
            filename = f"analysis_{timestamp}"
            subfolder = "analysis"

        return self.export_to_json(report, filename, subfolder=subfolder)

    def load_json(self, filepath: str) -> Any:
        """
        从JSON文件加载数据

        Args:
            filepath: 文件路径

        Returns:
            加载的数据
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_csv(self, filepath: str) -> List[Dict]:
        """
        从CSV文件加载数据

        Args:
            filepath: 文件路径

        Returns:
            加载的数据列表
        """
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            return list(reader)
