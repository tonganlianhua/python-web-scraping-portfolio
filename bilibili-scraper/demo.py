# -*- coding: utf-8 -*-
"""
B站视频爬虫演示脚本
展示爬虫的各种功能
"""

import os
from bilibili_scraper import BiliBiliScraper

# 创建输出目录
os.makedirs('examples', exist_ok=True)


def demo_single_video():
    """演示：获取单个视频信息"""
    print("=" * 60)
    print("演示1：获取单个视频信息")
    print("=" * 60)

    scraper = BiliBiliScraper(min_delay=2, max_delay=3)

    # 使用几个热门视频的BV号号）
    test_videos = [
        'BV1GJ411x7h7',  # 示例视频1
        'BV1xx411c7mD',  # 示例视频2
    ]

    for video in test_videos:
        print(f"\n获取视频信息: {video}")
        info = scraper.get_video_info(video)
        if info:
            print(f"✓ 标题: {info.get('title')}")
            print(f"✓ 作者: {info.get('author')}")
            print(f"✓ 播放量: {info.get('views', 0):,}")
            print(f"✓ 点赞: {info.get('likes', 0):,}")
            print(f"✓ 投币: {info.get('coins', 0):,}")
            print(f"✓ 收藏: {info.get('favorites', 0):,}")
        else:
            print("✗ 获取失败")

    scraper.close()


def demo_batch_videos():
    """演示：批量获取视频信息"""
    print("\n" + "=" * 60)
    print("演示2：批量获取视频信息")
    print("=" * 60)

    scraper = BiliBiliScraper(min_delay=2, max_delay=4)

    # 测试视频列表（使用真实存在的视频BV号）
    video_list = [
        'BV1GJ411x7h7',
        'BV1xx411c7mD',
        'BV1y44y1K7KL',
        'BV1bV4y1k7Vp',
        'BV1uV41197p7',
    ]

    print(f"\n批量获取 {len(video_list)} 个视频信息...")
    results = scraper.batch_get_videos(video_list)

    print(f"\n成功获取 {len(results)} 个视频信息:")
    for i, video in enumerate(results, 1):
        print(f"\n{i}. {video.get('title', 'N/A')}")
        print(f"   作者: {video.get('author', 'N/A')}")
        print(f"   播放量: {video.get('views', 0):,}")

    # 导出到CSV
    if results:
        output_file = 'examples/videos.csv'
        scraper.export_to_csv(results, output_file)
        print(f"\n✓ 数据已导出到: {output_file}")

    scraper.close()
    return results


def demo_search_videos():
    """演示：搜索视频"""
    print("\n" + "=" * 60)
    print("演示3：搜索视频")
    print("=" * 60)

    scraper = BiliBiliScraper(min_delay=2, max_delay=4)

    # 搜索关键词
    keywords = ['Python教程', '编程', '人工智能']

    for keyword in keywords:
        print(f"\n搜索关键词: {keyword}")
        results = scraper.search_videos(keyword, max_results=3)

        if results:
            print(f"✓ 找到 {len(results)} 个视频:")
            for video in results:
                print(f"  - {video.get('title')}")
                print(f"    播放量: {video.get('views', 0):,}")
        else:
            print("✗ 未找到视频")

    scraper.close()


def demo_generate_report():
    """演示：生成分析报告"""
    print("\n" + "=" * 60)
    print("演示4：生成数据分析报告")
    print("=" * 60)

    scraper = BiliBiliScraper(min_delay=2, max_delay=4)

    # 批量获取视频数据
    video_list = [
        'BV1GJ411x7h7',
        'BV1xx411c7mD',
        'BV1y44y1K7KL',
        'BV1bV4y1k7Vp',
        'BV1uV41197p7',
    ]

    print(f"\n获取视频数据用于分析...")
    results = scraper.batch_get_videos(video_list)

    if len(results) >= 2:
        # 生成报告
        report_file = 'examples/report.html'
        scraper.generate_report(results, report_file)
        print(f"\n✓ 分析报告已生成: {report_file}")
        print(f"  请用浏览器打开查看")

        # 导出CSV
        csv_file = 'examples/demo_videos.csv'
        scraper.export_to_csv(results, csv_file)
        print(f"\n✓ CSV文件已导出: {csv_file}")
    else:
        print(f"\n✗ 视频数据不足（需要至少2个视频）")

    scraper.close()


def demo_url_parsing():
    """演示：URL解析"""
    print("\n" + "=" * 60)
    print("演示5：URL和BV号解析")
    print("=" * 60)

    scraper = BiliBiliScraper(min_delay=2, max_delay=3)

    # 测试不同格式的输入
    test_inputs = [
        'BV1GJ411x7h7',
        'https://www.bilibili.com/video/BV1xx411c7mD',
        'https://b23.tv/BV1y44y1K7KL',
    ]

    for input_str in test_inputs:
        print(f"\n输入: {input_str}")
        info = scraper.get_video_info(input_str)
        if info:
            print(f"✓ 成功解析并获取信息")
            print(f"  标题: {info.get('title')}")
            print(f"  BV号: {info.get('bv')}")
        else:
            print(f"✗ 解析或获取失败")

    scraper.close()


def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "      B站视频爬虫 - 功能演示".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")

    try:
        # 运行各个演示
        demo_single_video()
        demo_batch_videos()
        demo_search_videos()
        demo_generate_report()
        demo_url_parsing()

        print("\n" + "=" * 60)
        print("所有演示完成！")
        print("=" * 60)
        print("\n生成的文件:")
        print("  - examples/videos.csv")
        print("  - examples/report.html")
        print("  - examples/demo_videos.csv")
        print("\n请用浏览器打开 report.html 查看分析报告")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n用户中断演示")
    except Exception as e:
        print(f"\n\n演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
