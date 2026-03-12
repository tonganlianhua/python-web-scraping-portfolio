"""
示例：搜索音乐
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from scraper import Music163Scraper


def main():
    """搜索音乐示例"""
    keyword = "周杰伦"
    print(f"搜索关键词: {keyword}")

    # 创建爬虫实例
    scraper = Music163Scraper()

    # 搜索歌曲
    result = scraper.search_and_scrape(
        keyword=keyword,
        limit=30,
        fetch_comments=True,
        comments_limit=15,
        export=True
    )

    # 显示搜索结果
    if result.get("songs"):
        print(f"\n搜索到 {len(result['songs'])} 首歌曲")
        print("\n前15首歌曲:")
        for i, song in enumerate(result['songs'][:15], 1):
            print(f"{i:2d}. {song['name']} - {song['artist']}")
            print(f"    专辑: {song['album']}")
            print(f"    时长: {song['duration'] // 1000 // 60}分{song['duration'] // 1000 % 60}秒")
            print(f"    链接: {song['url']}")

    print("\n数据已导出到 data/ 目录")


if __name__ == "__main__":
    main()
