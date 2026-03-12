"""
豆瓣电影爬虫 - 快速开始示例
快速上手示例代码
"""

from scraper import DoubanMovieScraper
from utils import DataExporter, DataAnalyzer
import os


def quick_start():
    """快速开始示例"""
    print("=" * 60)
    print("豆瓣电影爬虫 - 快速开始")
    print("=" * 60)

    # 创建输出目录
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # 创建爬虫实例
    scraper = DoubanMovieScraper()

    try:
        # 1. 爬取 Top250
        print("\n[步骤 1] 爬取豆瓣电影 Top250...")
        movies = scraper.get_top250()
        print(f"✓ 成功爬取 {len(movies)} 部电影")

        # 2. 展示 Top 10
        print("\n[步骤 2] Top 10 电影:")
        print(f"{'排名':<6}{'标题':<30}{'评分':<8}{'年份':<8}")
        print("-" * 52)
        for movie in movies[:10]:
            print(f"{movie['rank']:<6}{movie['title']:<30}{movie['rating']:<8.1f}{movie['year']:<8}")

        # 3. 导出数据
        print("\n[步骤 3] 导出数据...")
        DataExporter.to_csv(movies, f'{output_dir}/top250.csv')
        DataExporter.to_json(movies, f'{output_dir}/top250.json')

        # 4. 生成分析报告
        print("\n[步骤 4] 生成数据分析报告...")
        DataAnalyzer.generate_report(movies, output_dir)

        # 5. 展示数据统计
        print("\n[步骤 5] 数据统计:")
        ratings = [m['rating'] for m in movies]
        years = [m['year'] for m in movies]
        print(f"  - 电影总数: {len(movies)}")
        print(f"  - 平均评分: {sum(ratings) / len(ratings):.2f}")
        print(f"  - 最高评分: {max(ratings)}")
        print(f"  - 最低评分: {min(ratings)}")
        print(f"  - 年份范围: {min(years)} - {max(years)}")

        print("\n" + "=" * 60)
        print("✓ 完成！所有数据已保存到 'output' 目录")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()

    finally:
        scraper.close()


if __name__ == '__main__':
    quick_start()
