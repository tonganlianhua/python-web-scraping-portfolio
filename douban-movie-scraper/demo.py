"""
豆瓣电影爬虫演示脚本
展示如何使用爬虫的各种功能
"""

from scraper import DoubanMovieScraper
from utils import DataExporter, DataAnalyzer
import os


def demo_top250():
    """演示：爬取 Top250"""
    print("\n" + "=" * 60)
    print("演示 1: 爬取豆瓣电影 Top250")
    print("=" * 60)

    scraper = DoubanMovieScraper()

    try:
        # 爬取 Top250
        movies = scraper.get_top250()

        print(f"\n✓ 成功爬取 {len(movies)} 部电影\n")

        # 打印前 10 部电影
        print("=== Top 10 电影 ===")
        print(f"{'排名':<6}{'标题':<30}{'年份':<8}{'评分':<8}{'评价':<10}")
        print("-" * 62)
        for movie in movies[:10]:
            print(f"{movie['rank']:<6}{movie['title']:<30}{movie['year']:<8}{movie['rating']:<8.1f}{movie['rating_people']:<10}")

        # 导出数据
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)

        DataExporter.to_csv(movies, f'{output_dir}/top250.csv')
        DataExporter.to_json(movies, f'{output_dir}/top250.json')

        # 生成分析报告
        DataAnalyzer.generate_report(movies, output_dir)

        print(f"\n✓ 演示 1 完成！数据已保存到 {output_dir}/ 目录")

        return movies

    except Exception as e:
        print(f"\n✗ 演示 1 失败: {e}")
        return []

    finally:
        scraper.close()


def demo_search():
    """演示：搜索电影"""
    print("\n" + "=" * 60)
    print("演示 2: 搜索电影")
    print("=" * 60)

    scraper = DoubanMovieScraper()

    try:
        # 搜索关键词
        keyword = input("\n请输入搜索关键词（直接回车使用默认 '肖申克的救赎'）: ").strip()
        if not keyword:
            keyword = '肖申克的救赎'

        # 搜索电影
        results = scraper.search_movies(keyword, limit=10)

        print(f"\n✓ 找到 {len(results)} 部电影\n")

        # 打印搜索结果
        print("=== 搜索结果 ===")
        for idx, movie in enumerate(results, 1):
            print(f"{idx}. {movie['title']} ({movie['year']}) - {movie['rating']}")

        print(f"\n✓ 演示 2 完成！")

        return results

    except Exception as e:
        print(f"\n✗ 演示 2 失败: {e}")
        return []

    finally:
        scraper.close()


def demo_movie_detail():
    """演示：获取电影详情"""
    print("\n" + "=" * 60)
    print("演示 3: 获取电影详细信息")
    print("=" * 60)

    scraper = DoubanMovieScraper()

    try:
        # 获取电影 ID
        movie_id = input("\n请输入电影 ID（直接回车使用默认 '1292052' - 肖申克的救赎）: ").strip()
        if not movie_id:
            movie_id = '1292052'

        # 获取详情
        detail = scraper.get_movie_detail(movie_id)

        if detail:
            print(f"\n{'='*40}")
            print(f"电影: {detail['title']}")
            print(f"{'='*40}")
            print(f"年份: {detail['year']}")
            print(f"评分: {detail['rating']}")
            print(f"评价人数: {detail['rating_people']}")
            print(f"导演: {', '.join(detail['directors'])}")
            print(f"主演: {', '.join(detail['actors'])}")
            print(f"类型: {', '.join(detail['genres'])}")
            print(f"\n剧情简介:")
            print(f"{detail['summary'][:200]}...")

            print(f"\n✓ 演示 3 完成！")

        return detail

    except Exception as e:
        print(f"\n✗ 演示 3 失败: {e}")
        return None

    finally:
        scraper.close()


def demo_comments():
    """演示：获取电影评论"""
    print("\n" + "=" * 60)
    print("演示 4: 获取电影评论")
    print("=" * 60)

    scraper = DoubanMovieScraper()

    try:
        # 获取电影 ID
        movie_id = input("\n请输入电影 ID（直接回车使用默认 '1292052' - 肖申克的救赎）: ").strip()
        if not movie_id:
            movie_id = '1292052'

        # 获取评论
        limit = input("请输入评论数量（直接回车使用默认 10 条）: ").strip()
        limit = int(limit) if limit.isdigit() else 10

        comments = scraper.get_comments(movie_id, limit=limit)

        print(f"\n✓ 获取到 {len(comments)} 条评论\n")

        # 打印评论
        print("=== 最新评论 ===")
        for idx, comment in enumerate(comments, 1):
            print(f"\n{idx}. {comment['user']} ({comment['time']})")
            if comment['rating_str']:
                print(f"   评分: {comment['rating_str']} ({comment['rating']}/5)")
            print(f"   内容: {comment['content']}")
            print(f"   有用: {comment['votes']} 人")

        print(f"\n✓ 演示 4 完成！")

        return comments

    except Exception as e:
        print(f"\n✗ 演示 4 失败: {e}")
        return []

    finally:
        scraper.close()


def demo_full_workflow():
    """演示：完整工作流"""
    print("\n" + "=" * 60)
    print("演示 5: 完整工作流（爬取 + 导出 + 分析）")
    print("=" * 60)

    scraper = DoubanMovieScraper()

    try:
        # 1. 爬取 Top250
        print("\n[步骤 1] 爬取豆瓣电影 Top250...")
        movies = scraper.get_top250()
        print(f"✓ 成功爬取 {len(movies)} 部电影")

        # 2. 导出出数据
        print("\n[步骤 2] 导出数据...")
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)

        csv_file = DataExporter.to_csv(movies, f'{output_dir}/top250.csv')
        json_file = DataExporter.to_json(movies, f'{output_dir}/top250.json')

        # 3. 生成分析报告
        print("\n[步骤 3] 生成数据分析报告...")
        report_files = DataAnalyzer.generate_report(movies, output_dir)

        # 4. 展示关键数据
        print("\n[步骤 4] 数据概览...")
        print(f"  - 总电影数: {len(movies)}")
        print(f"  - 平均评分: {sum(m['rating'] for m in movies) / len(movies):.2f}")
        print(f"  - 年份范围: {min(m['year'] for m in movies)} - {max(m['year'] for m in movies)}")

        print(f"\n✓ 演示 5 完成！")
        print(f"\n生成的文件:")
        {print(f"  - {csv_file}") if csv_file else None}
        {print(f"  - {json_file}") if json_file else None}
        {print(f"  - {report_files.get('report')}") if report_files.get('report') else None}
        {print(f"  - {report_files.get('charts')} (目录)") if report_files.get('charts') else None}

    except Exception as e:
        print(f"\n✗ 演示 5 失败: {e}")

    finally:
        scraper.close()


def main():
    """主函数"""
    print("=" * 60)
    print("豆瓣电影爬虫 - 演示脚本")
    print("=" * 60)
    print()
    print("请选择演示功能:")
    print("  1. 爬取豆瓣电影 Top250")
    print("  2. 搜索电影")
    print("  3. 获取电影详细信息")
    print("  4. 获取电影评论")
    print("  5. 完整工作流（爬取 + 导出 + 分析）")
    print("  0. 退出")
    (print("=" * 60))

    while True:
        choice = input("\n请输入选项 (0-5): ").strip()

        if choice == '1':
            demo_top250()
        elif choice == '2':
            demo_search()
        elif choice == '3':
            demo_movie_detail()
        elif choice == '4':
            demo_comments()
        elif choice == '5':
            demo_full_workflow()
        elif choice == '0':
            print("\n再见！")
            break
        else:
            print("\n✗ 无效选项，请重新输入！")


if __name__ == '__main__':
    main()
