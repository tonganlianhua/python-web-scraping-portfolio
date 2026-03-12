#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单使用示例
演示如何使用大众点评爬虫
"""

from scraper import DianpingScraper
from exporter import DataExporter
import time


def example_1_basic_search():
    """示例1：基本搜索"""
    print("\n" + "="*60)
    print("示例1：基本搜索")
    print("="*60)

    # 创建爬虫实例
    scraper = DianpingScraper(city="北京", keyword="火锅")

    # 搜索商家（第1页）
    merchants = scraper.search_merchants("北京", "火锅", page=1)

    # 显示结果
    print(f"\n找到 {len(merchants)} 个商家：")
    for i, m in enumerate(merchants[:5], 1):
        print(f"{i}. {m.get('name', '未知')} - 评分: {m.get('rating', 0)}, 人均: {m.get('avg_price', 0)}元")


def example_2_export_data():
    """示例2：导出数据"""
    print("\n" + "="*60)
    print("示例2：导出数据")
    print("="*60)

    # 创建爬虫并搜索
    scraper = DianpingScraper(city="上海", keyword="日料")
    scraper.search_merchants("上海", "日料", page=1)

    # 导出到CSV
    scraper.export_to_csv('shanghai_japanese.csv', data_type='merchants')

    # 导出到JSON
    scraper.export_to_json('shanghai_japanese.json', data_type='merchants')

    print("\n✅ 数据导出完成！")


def example_3_generate_report():
    """示例3：生成分析报告"""
    print("\n" + "="*60)
    print("示例3：生成分析报告")
    print("="*60)

    # 创建爬虫并搜索
    scraper = DianpingScraper(city="广州", keyword="咖啡馆")
    scraper.search_merchants("广州", "咖啡馆", page=1)

    # 生成报告
    report = scraper.generate_report()
    print(report)


def example_4_rating_filter():
    """示例4：评分筛选"""
    print("\n" + "="*60)
    print("示例4：只爬取高评分商家")
    print("="*60)

    # 创建爬虫，设置最低评分为4.5
    scraper = DianpingScraper(city="深圳", keyword="美食", min_rating=4.5)

    # 搜索商家
    merchants = scraper.search_merchants("深圳", "美食", page=1)

    print(f"\n评分 >= 4.5 的商家：")
    for i, m in enumerate(merchants, 1):
        print(f"{i}. {m.get('name', '未知')} - 评分: {m.get('rating', 0)}")


def example_5_multi_page():
    """示例5：多页爬取"""
    print("\n" + "="*60)
    print("示例5：多页爬取")
    print("="*60)

    # 创建爬虫
    scraper = DianpingScraper(city="杭州", keyword="酒店")

    # 爬取多页（2页）
    scraper.crawl_multiple_pages(
        city="杭州",
        keyword="酒店",
        start_page=1,
        max_pages=2
    )

    print(f"\n✅ 总共爬取 {len(scraper.merchants)} 个商家")


def example_6_advanced_analysis():
    """示例6：高级分析"""
    print("\n" + "="*60)
    print("示例6：高级数据分析")
    print("="*60)

    # 创建爬虫并搜索
    scraper = DianpingScraper(city="北京", keyword="美食")
    scraper.search_merchants("北京", "美食", page=1)

    # 使用导出器
    exporter = DataExporter()

    # 导出数据
    if scraper.merchants:
        exporter.export_csv(scraper.merchants, 'beijing_food.csv')
        exporter.export_json(scraper.merchants, 'beijing_food.json')

        # 生成详细报告
        report = exporter.generate_text_report(scraper.merchants)
        print(report)

        # 保存报告
        exporter.save_report(report, 'beijing_food_report.txt')

        # 绘制图表
        print("\n正在生成图表...")
        exporter.plot_rating_distribution(scraper.merchants, 'rating_distribution.png')
        exporter.plot_price_distribution(scraper.merchants, 'price_distribution.png')
        print("✅ 图表生成完成！")


def example_7_batch_crawl():
    """示例7：批量爬取多个城市"""
    print("\n" + "="*60)
    print("示例7：批量爬取多个城市")
    print("="*60)

    cities = ['北京', '上海', '广州']
    keyword = '火锅'
    all_merchants = []

    for city in cities:
        print(f"\n正在爬取 {city} 的 {keyword}...")

        scraper = DianpingScraper(city=city, keyword=keyword)
        merchants = scraper.search_merchants(city, keyword, page=1)

        all_merchants.extend(merchants)
        print(f"找到 {len(merchants)} 个商家")

        # 城市间延时
        time.sleep(2)

    # 导出所有数据
    exporter = DataExporter()
    exporter.export_csv(all_merchants, 'all_cities_hotpot.csv')
    exporter.export_json(all_merchants, 'all_cities_hotpot.json')

    # 生成综合报告
    report = exporter.generate_text_report(all_merchants)
    print("\n" + report)

    print(f"\n✅ 总共爬取 {len(all_merchants)} 个商家")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("大众点评爬虫使用示例".center(60))
    print("="*60)

    print("\n可选示例：")
    print("1. 基本搜索")
    print("2. 导出数据")
    print("3. 生成分析报告")
    print("4. 评分筛选")
    print("5. 多页爬取")
    print("6. 高级分析")
    print("7. 批量爬取多个城市")

    choice = input("\n请选择示例 (1-7, 或按Enter运行示例6): ").strip()

    try:
        if not choice or choice == '6':
            example_6_advanced_analysis()
        elif choice == '1':
            example_1_basic_search()
        elif choice == '2':
            example_2_export_data()
        elif choice == '3':
            example_3_generate_report()
        elif choice == '4':
            example_4_rating_filter()
        elif choice == '5':
            example_5_multi_page()
        elif choice == '7':
            example_7_batch_crawl()
        else:
            print("无效选择")

        print("\n✅ 示例执行完成！")

    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
