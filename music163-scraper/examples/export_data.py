"""
示例：数据导出
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from api_client import NetEaseMusicAPI
from export import DataExporter


def main():
    """数据导出示例"""
    print("数据导出示例")

    # 获取数据
    print("\n1. 获取热歌榜数据...")
    api = NetEaseMusicAPI()
    songs = api.get_top_list_songs("hot", limit=10)

    if not songs:
        print("获取数据失败")
        return

    # 获取评论
    print("\n2. 获取歌曲评论...")
    comments = []
    for song in songs[:3]:
        song_comments = api.get_song_comments(song["id"], limit=5)
        if song_comments:
            comments.extend(song_comments)

    # 创建导出器
    exporter = DataExporter()

    # 导出歌曲数据
    print("\n3. 导出歌曲数据...")
    csv_file = exporter.export_songs_to_csv(songs, "export_songs.csv")
    json_file = exporter.export_songs_to_json(songs, "export_songs.json")

    print(f"  CSV文件: {csv_file}")
    print(f"  JSON文件: {json_file}")

    # 导出评论数据
    if comments:
        print("\n4. 导出评论数据...")
        csv_comments = exporter.export_comments_to_csv(comments, "export_comments.csv")
        json_comments = exporter.export_comments_to_json(comments, "export_comments.json")

        print(f"  CSV文件: {csv_comments}")
        print(f"  JSON文件: {json_comments}")

    # 导出所有数据
    print("\n5. 导出所有数据...")
    all_results = exporter.export_all(songs, comments, prefix="batch_export")

    print("\n导出完成！")
    print("\n生成的文件:")
    for name, path in all_results.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
