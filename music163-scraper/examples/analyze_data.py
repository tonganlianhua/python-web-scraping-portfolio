"""
示例：数据分析
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from api_client import NetEaseMusicAPI
from analyzer import MusicAnalyzer


def main():
    """数据分析示例"""
    print("数据分析示例")

    # 获取数据
    print("\n1. 获取热歌榜数据...")
    api = NetEaseMusicAPI()
    songs = api.get_top_list_songs("hot", limit=30)

    if not songs:
        print("获取数据失败")
        return

    # 获取评论
    print("\n2. 获取歌曲评论...")
    comments = []
    for song in songs[:10]:
        song_comments = api.get_song_comments(song["id"], limit=10)
        if song_comments:
            comments.extend(song_comments)

    print(f"共获取 {len(songs)} 首歌曲, {len(comments)} 条评论")

    # 创建分析器
    analyzer = MusicAnalyzer()

    # 分析歌手排行
    print("\n3. 分析歌手排行...")
    artist_ranking = analyzer.analyze_artists_ranking(songs, top_n=10)
    print("\n歌手排行 TOP 10:")
    for item in artist_ranking:
        print(f"  {item['rank']:2d}. {item['artist']:<20s} ({item['song_count']}首)")

    # 分析歌曲热度
    print("\n4. 分析歌曲热度...")
    popularity = analyzer.analyze_songs_popularity(songs, top_n=10)
    print("\n歌曲热度排行 TOP 10:")
    for item in popularity:
        print(f"  {item['rank']:2d}. {item['name']:<30s}")
        print(f"      歌手: {item['artist']}")
        print(f"      播放量: {item['play_count']:,}")
        print(f"      评论数: {item['comment_count']:,}")

    # 生成词云
    if comments:
        print("\n5. 生成词云...")
        wordcloud_results = analyzer.generate_wordcloud(comments, max_words=100)

        if wordcloud_results:
            print(f"词云图片: {wordcloud_results.get('wordcloud_image')}")
            print(f"词频统计: {wordcloud_results.get('word_freq_json')}")

    # 生成完整报告
    print("\n6. 生成分析报告...")
    report_path = analyzer.generate_report(
        songs=songs,
        comments=comments,
        include_wordcloud=True,
        filename="example_analysis_report.json"
    )

    print(f"\n分析报告已生成: {report_path}")

    # 显示统计信息
    stats = analyzer._calculate_statistics(songs)
    print("\n数据统计:")
    print(f"  总歌曲数: {stats['total_songs']}")
    print(f"  总歌手数: {stats['total_artists']}")
    print(f"  总播放量: {stats['total_plays']:,}")
    print(f"  总评论数: {stats['total_comments']:,}")
    print(f"  平均播放量: {stats['avg_plays_per_song']:,}")
    print(f"  平均评论数: {stats['avg_comments_per_song']:.2f}")


if __name__ == "__main__":
    main()
