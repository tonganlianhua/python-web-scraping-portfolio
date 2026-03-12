"""
网易云音乐爬虫演示脚本
展示各项功能的使用方法
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from scraper import Music163Scraper


def demo_get_top_list():
    """演示：获取排行榜数据"""
    print("\n" + "="*60)
    print("演示1: 获取热歌榜数据")
    print("="*60)

    scraper = Music163Scraper()

    # 获取热歌榜前20首，获取评论，导出并分析
    result = scraper.scrape_top_list(
        list_type="hot",
        limit=20,
        fetch_comments=True,
        comments_limit=10,
        export=True,
        analyze=True
    )

    # 显示部分结果
    if result.get("songs"):
        print("\n前5首歌曲:")
        for i, song in enumerate(result["songs"][:5], 1):
            print(f"{i}. {song['name']} - {song['artist']}")
            print(f"   播专辑: {song['album']}")
            print(f"   播放量: {song['play_count']:,}")
            print(f"   评论数: {song['comment_count']:,}")

    if result.get("comments"):
        print(f"\n获取到 {len(result['comments'])} 条评论")
        print("前3条评论:")
        for i, comment in enumerate(result["comments"][:3], 1):
            print(f"{i}. {comment['user']}: {comment['content'][:50]}...")
            print(f"   点赞: {comment['liked_count']}")


def demo_search_songs():
    """演示：搜索歌曲"""
    print("\n" + "="*60)
    print("演示2: 搜索歌曲")
    print("="*60)

    scraper = Music163Scraper()

    # 搜索歌曲
    result = scraper.search_and_scrape(
        keyword="周杰伦",
        limit=15,
        fetch_comments=True,
        comments_limit=10,
        export=True
    )

    # 显示搜索结果
    if result.get("songs"):
        print(f"\n搜索到 {len(result['songs'])} 首歌曲:")
        for i, song in enumerate(result["songs"][:10], 1):
            print(f"{i}. {song['name']} - {song['artist']}")


def demo_multiple_top_lists():
    """演示：获取多个排行榜"""
    print("\n" + "="*60)
    print("演示3: 获取多个排行榜")
    print("="*60)

    scraper = Music163Scraper()

    # 获取所有可用榜单
    top_lists = scraper.get_available_top_lists()
    print("\n可用榜单:")
    for list_type, list_name in top_lists.items():
        print(f"  {list_type}: {list_name}")

    # 获取新歌榜和原创榜
    for list_type in ["new", "original"]:
        print(f"\n获取 {top_lists[list_type]}...")
        result = scraper.scrape_top_list(
            list_type=list_type,
            limit=15,
            fetch_comments=False,  # 不获取评论以加快速度
            export=True,
            analyze=True
        )

        if result.get("songs"):
            print(f"成功获取 {len(result['songs'])} 首歌曲")


def demo_export_formats():
    """演示：不同的导出格式"""
    print("\n" + "="*60)
    print("演示4: 数据导出格式")
    print("="*60)

    scraper = Music163Scraper()

    # 获取数据
    result = scraper.scrape_top_list(
        list_type="soar",
        limit=10,
        fetch_comments=False,
        export=False
    )

    if result.get("songs"):
        print("\n数据已获取，将演示单独导出...")

        # 单独导出为JSON
        json_path = scraper.exporter.export_songs_to_json(
            result["songs"],
            "demo_export.json"
        )
        print(f"JSON文件: {json_path}")

        # 单独导出为CSV
        csv_path = scraper.exporter.export_songs_to_csv(
            result["songs"],
            "demo_export.csv"
        )
        print(f"CSV文件: {csv_path}")


def demo_analysis_only():
    """演示：仅进行数据分析"""
    print("\n" + "="*60)
    print("演示5: 数据分析功能")
    print("="*60)

    scraper = Music163Scraper()

    # 先获取数据
    result = scraper.scrape_top_list(
        list_type="hot",
        limit=30,
        fetch_comments=True,
        comments_limit=15,
        export=False
    )

    if result.get("songs"):
        print("\n开始数据分析...")

        # 生成分析报告（不重新爬取）
        report_path = scraper.analyzer.generate_report(
            result["songs"],
            result.get("comments", []),
            include_wordcloud=True,
            filename="demo_analysis_report.json"
        )
        print(f"分析报告: {report_path}")

        # 显示歌手排行
        artists_ranking = scraper.analyzer.analyze_artists_ranking(result["songs"], top_n=10)
        print("\n歌手排行 TOP 10:")
        for item in artists_ranking:
            print(f"  {item['rank']}. {item['artist']} ({item['song_count']}首)")

        # 显示歌曲热度
        popularity = scraper.analyzer.analyze_songs_popularity(result["songs"], top_n=10)
        print("\n歌曲热度排行 TOP 10:")
        for item in popularity:
            print(f"  {item['rank']}. {item['name']} - {item['artist']}")
            print(f"     播放量: {item['play_count']:,}")


def main():
    """主函数 - 运行所有演示"""
    print("\n" + "="*60)
    print("网易云音乐爬虫 - 功能演示")
    print("="*60)

    try:
        # 演示1: 获取排行榜
        demo_get_top_list()

        # 演示2: 搜索歌曲
        demo_search_songs()

        # 演示3: 获取多个排行榜
        demo_multiple_top_lists()

        # 演示4: 导出格式
        demo_export_formats()

        # 演示5: 数据分析
        demo_analysis_only()

        print("\n" + "="*60)
        print("所有演示完成！")
        print("生成的文件位于 data/ 目录")
        print("="*60 + "\n")

    except KeyboardInterrupt:
        print("\n\n演示被用户中断")
    except Exception as e:
        print(f"\n\n演示过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
