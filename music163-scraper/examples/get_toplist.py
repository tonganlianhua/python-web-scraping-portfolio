"""
示例：获取排行榜数据
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from scraper import Music163Scraper


def main():
    """获取热歌榜示例"""
    print("获取热歌榜前50首歌曲...")

    # 创建爬虫实例
    scraper = Music163Scraper()

    # 获取热歌榜
    result = scraper.scrape_top_list(
        list_type="hot",
        limit=50,
        fetch_comments=True,
        comments_limit=20,
        export=True,
        analyze=True
    )

    # 显示结果摘要
    if result.get("songs"):
        print(f"\n成功获取 {len(result['songs'])} 首歌曲")
        print(f"成功获取 {len(result.get('comments', []))} 条评论")
        print("\n前10首歌曲:")
        for i, song in enumerate(result['songs'][:10], 1):
            print(f"{i:2d}. {song['name']} - {song['artist']}")
            print(f"    播放量: {song['play_count']:,:,}")
            print(f"    评论数: {song['comment_count']:,}")

    print("\n数据已导出到 data/ 目录")


if __name__ == "__main__":
    main()
