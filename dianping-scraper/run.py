#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
主运行脚本 - 命令行接口
"""

import argparse
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from scraper import DianpingScraper
from exporter import DataExporter


def crawl_search(city, keyword, pages, min_rating, output_dir):
    """搜索爬取模式"""
    print(f"\n开始爬取: {city} - {keyword}")
    print(f"页数: {pages}, 最低评分: {min_rating}")

    # 创建爬虫
    scraper = DianpingScraper(city=city, keyword=keyword, min_rating=min_rating)

    # 爬取数据
    if pages > 1:
        scraper.crawl_multiple_pages(city, keyword, start_page=1, max_pages=pages)
    else:
        scraper.search_merchants(city, keyword, page=1)

    print(f"\n✅ 爬取完成，共获取 {len(scraper.merchants)} 个商家")

    # 导出数据
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    exporter = DataExporter(output_dir=output_dir)

    # 导出CSV
    csv_filename = f"{city}_{keyword}.csv"
    exporter.export_csv(scraper.merchants, csv_filename)

    # 导出JSON
    json_filename = f"{city}_{keyword}.json"
    exporter.export_json(scraper.merchants, json_filename)

    # 生成报告
    report = exporter.generate_text_report(scraper.merchants)
    report_filename = f"{city}_{keyword}_report.txt"
    exporter.save_report(report, report_filename)

    # 绘制图表
    exporter.plot_rating_distribution(scraper.merchants, f"{city}_{keyword}_rating.png")
    exporter.plot_price_distribution(scraper.merchants, f"{city}_{keyword}_price.png")

    print("\n✅ 数据导出和分析完成！")
    print(f"保存位置: {output_dir or '.'}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='大众点评爬虫 - 命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 爬取北京火锅店数据（1页）
  python run.py 北京 火锅

  # 爬取上海日料店数据（3页，最低评分4.0）
  python run.py 上海 日料 -p 3 -r 4.0

  # 爬取广州咖啡馆数据，指定输出目录
  python run.py 广州 咖啡馆 -p 2 -o ./output
        """
    )

    parser.add_argument('city', help='城市名称（如：北京、上海、广州）')
    parser.add_argument('keyword', help='搜索关键词（如：美食、火锅、日料）')
    parser.add_argument('-p', '--pages', type=int, default=1,
                        help='爬取页数（默认：1）')
    parser.add_argument('-r', '--rating', type=float, default=0.0,
                        help='最低评分筛选（默认：0.0）')
    parser.add_argument('-o', '--output', default='output',
                        help='输出目录（默认：output）')

    args = parser.parse_args()

    try:
        crawl_search(
            city=args.city,
            keyword=args.keyword,
            pages=args.pages,
            min_rating=args.rating,
            output_dir=args.output
        )
    except KeyboardInterrupt:
        print("\n\n用户中断爬取")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
