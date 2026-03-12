"""
数据导出模块
支持导出为CSV和JSON格式
"""

import json
import csv
import os
from typing import List, Dict
from datetime import datetime

from config import EXPORT_DIR, DEFAULT_ENCODING


class DataExporter:
    """数据导出器"""

    def __init__(self, export_dir: str = EXPORT_DIR):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def export_songs_to_csv(self, songs: List[Dict], filename: str = None) -> str:
        """
        导出歌曲数据到CSV

        Args:
            songs: 歌曲数据列表
            filename: 自定义文件名（可选）

        Returns:
            导出文件路径
        """
        if not songs:
            print("没有歌曲数据可导出")
            return None

        if filename is None:
            filename = f"songs_{self._get_timestamp()}.csv"

        filepath = os.path.join(self.export_dir, filename)

        with open(filepath, "w", encoding=DEFAULT_ENCODING, newline="") as f:
            fieldnames = ["id", "name", "artist", "album", "play_count",
                         "comment_count", "duration", "url"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for song in songs:
                row = {key: song.get(key, "") for key in fieldnames}
                writer.writerow(row)

        print(f"歌曲数据已导出到: {filepath}")
        return filepath

    def export_songs_to_json(self, songs: List[Dict], filename: str = None) -> str:
        """
        导出歌曲数据到JSON

        Args:
            songs: 歌曲数据列表
            filename: 自定义文件名（可选）

        Returns:
            导出文件路径
        """
        if not songs:
            print("没有歌曲数据可导出")
            return None

        if filename is None:
            filename = f"songs_{self._get_timestamp()}.json"

        filepath = os.path.join(self.export_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(songs, f, ensure_ascii=False, indent=2)

        print(f"歌曲数据已导出到: {filepath}")
        return filepath

    def export_comments_to_csv(self, comments: List[Dict], filename: str = None) -> str:
        """
        导出评论数据到CSV

        Args:
            comments: 评论数据列表
            filename: 自定义文件名（可选）

        Returns:
            导出文件路径
        """
        if not comments:
            print("没有评论数据可导出")
            return None

        if filename is None:
            filename = f"comments_{self._get_timestamp()}.csv"

        filepath = os.path.join(self.export_dir, filename)

        with open(filepath, "w", encoding=DEFAULT_ENCODING, newline="") as f:
            fieldnames = ["id", "song_id", "content", "liked_count",
                         "time", "time_str", "user"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for comment in comments:
                row = {key: comment.get(key, "") for key in fieldnames}
                writer.writerow(row)

        print(f"评论数据已导出到: {filepath}")
        return filepath

    def export_comments_to_json(self, comments: List[Dict], filename: str = None) -> str:
        """
        导出评论数据到JSON

        Args:
            comments: 评论数据列表
            filename: 自定义文件名（可选）

        Returns:
            导出文件路径
        """
        if not comments:
            print("没有评论数据可导出")
            return None

        if filename is None:
            filename = f"comments_{self._get_timestamp()}.json"

        filepath = os.path.join(self.export_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)

        print(f"评论数据已导出到: {filepath}")
        return filepath

    def export_all(self, songs: List[Dict], comments: List[Dict] = None,
                   prefix: str = None) -> Dict[str, str]:
        """
        导出所有数据到CSV和JSON

        Args:
            songs: 歌曲数据列表
            comments: 评论数据列表（可选）
            prefix: 文件名前缀（可选）

        Returns:
            导出文件路径字典
        """
        timestamp = self._get_timestamp()
        if prefix:
            timestamp = f"{prefix}_{timestamp}"

        results = {}

        # 导出歌曲数据
        results["songs_csv"] = self.export_songs_to_csv(songs, f"{timestamp}_songs.csv")
        results["songs_json"] = self.export_songs_to_json(songs, f"{timestamp}_songs.json")

        # 导出评论数据
        if comments:
            results["comments_csv"] = self.export_comments_to_csv(comments, f"{timestamp}_comments.csv")
            results["comments_json"] = self.export_comments_to_json(comments, f"{timestamp}_comments.json")

        return results
