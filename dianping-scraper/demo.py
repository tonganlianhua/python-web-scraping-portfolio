#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
大众点评爬虫演示脚本
展示所有功能的使用方法

使用方法:
    python demo.py
"""

from scraper import DianpingScraper
from exporter import DataExporter
import time


def demo_basic_search():
    """演示基本搜索功能"""
    print("\n" + "="*70)
    print("📝 演示 1: 基本搜索")
    print("="*70)

    # 创建爬虫实例
    scraper = DianpingScraper(city="北京", keyword="美食")

    # 搜索商家
    merchants = scraper.search_merchants("北京", "美食", page=1)

    print(f"\n找到 {len(merchants)} 个商家:")
    for i, m in enumerate(merchants[:5], 1):
        print(f"  {i}. {m.get('name', '未知')} - 评分: {m.get('rating', 0)}, 人均: {m.get('avg_price', 0)}元")

    return scraper


def demo_multi_page():
    """演示多页爬取"""
    print("\n" + "="*70)
    print("📝 演示 2: 多页爬取")
    print("="*70)

    scraper = DianpingScraper(city="上海", keyword="酒店")

    # 爬取多页数据
    scraper.crawl_multiple_pages(city="上海", keyword="酒店", start_page=1, max_pages=2)

    print(f"\n总共爬取 {len(scraper.merchants)} 个商家")
    return scraper


def demo_rating_filter():
    """演示评分筛选"""
    print("\n" + "="*70)
    print("📝 演示 3: 评分筛选")
    print("="*70)

    # 只搜索评分 >= 4.5 的商家
    scraper = DianpingScraper(city="广州", keyword="餐厅", min_rating=4.5)

    merchants = scraper.search_merchants("广州", "餐厅", page=1)

    print(f"\n评分 >= 4.5 的商家:")
    for i, m in enumerate(merchants, 1):
        print(f"  {i}. {m.get('name', '未知')} - 评分: {m.get('rating', 0)}")

    return scraper


def demo_export():
    """演示数据导出功能"""
    print("\n" + "="*70)
    print("📝 演示 4: 数据导出 (CSV + JSON)")
    print("="*70)

    # 先爬取一些数据
    scraper = DianpingScraper(city="深圳", keyword="娱乐")
    scraper.search_merchants("深圳", "娱乐", page=1)

    # 导出到CSV
    scraper.export_to_csv('demo_merchants.csv', data_type='merchants')

    # 导出到JSON
    scraper.export_to_json('demo_merchants.json', data_type='merchants')

    return scraper


def demo_report():
    """演示报告生成功能"""
    print("\n" + "="*70)
    print("📝 演示 5: 数据分析报告")
    print("="*70)

    # 先爬取一些数据
    scraper = DianpingScraper(city="杭州", keyword="美食")
    scraper.crawl_multiple_pages(city="杭州", keyword="美食", start_page=1, max_pages=2)

    # 生成报告
    report = scraper.generate_report()
    print("\n" + report)

    # 保存报告
    report_file = 'demo_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存到 {report_file}")

    return scraper


def demo_advanced_exporter():
    """演示高级导出和分析功能"""
    print("\n" + "="*70)
    print("📝 演示 6: 高级导出和分析")
    print("="*70)

    # 创建爬虫并获取数据
    scraper = DianpingScraper(city="北京", keyword="火锅")
    scraper.search_merchants("北京", "火锅", page=1)

    # 使用导出器
    exporter = DataExporter()

    # 导出数据
    if scraper.merchants:
        csv_file = exporter.export_csv(scraper.merchants, 'advanced_merchants.csv')
        json_file = exporter.export_json(scraper.merchants, 'advanced_merchants.json')

        # 生成分析报告
        report = exporter.generate_text_report(scraper.merchants)
        print("\n" + report)

        # 保存报告
        exporter.save_report(report, 'advanced_report.txt')

        # 绘制图表
        exporter.plot_rating_distribution(scraper.merchants, 'rating_distribution.png')
        exporter.plot_price_distribution(scraper.merchants, 'price_distribution.png')

    return scraper


def demo_full_workflow():
    """演示完整工作流程"""
    print("\n" + "="*70)
    print("📝 演示 7: 完整工作流程")
    print("="*70)

    print("\n步骤 1: 初始化爬虫")
    scraper = DianpingScraper(city="北京", keyword="日料", min_rating=4.0)

    print("\n步骤 2: 爬取商家数据")
    scraper.crawl_multiple_pages(city="北京", keyword="日料", start_page=1, max_pages=2)

    print(f"✅ 爬取完成，共获取 {len(scraper.merchants)} 个商家")

    print("\n步骤 3: 导出数据")
    exporter = DataExporter()

    if scraper.merchants:
        csv_file = exporter.export_csv(scraper.merchants, 'full_workflow_merchants.csv')
        json_file = exporter.export_json(scraper.merchants, 'full_workflow_merchants.json')

    print("\n步骤 4: 生成分析报告")
    report = exporter.generate_text_report(scraper.merchants) if scraper.merchants else "无数据"

    print("\n步骤 5: 保存报告")
    exporter.save_report(report, 'full_workflow_report.txt')

    print("\n步骤 6: 生成可视化图表")
    exporter.plot_rating_distribution(scraper.merchants, 'full_workflow_rating.png')
    exporter.plot_price_distribution(scraper.merchants, 'full_workflow_price.png')

    print("\n✅ 完整工作流程执行完成！")

    return scraper


def main():
    """主函数"""
    print("\n" + "="*70)
    print("大众点评爬虫演示程序".center(70))
    print("="*70)
    print("\n本演示将展示以下功能:")
    print("  1. 基本搜索")
    print("  2. 多页爬取")
    print("  3. 评分筛选")
    print("  4. 数据导出 (CSV + JSON)")
    print("  5. 数据分析报告")
    print("  6. 高级导出和分析")
    print("  7. 完整工作流程")
    print("\n注意: 实际爬取数据时，请遵守网站robots.txt规定")

    choice = input("\n请选择演示 (1-7, 或按Enter跳过): ").strip()

    if not choice:
        print("\n跳过演示，程序结束")
        return

    try:
        if choice == '1':
            demo_basic_search()
        elif choice == '2':
            demo_multi_page()
        elif choice == '3':
            demo_rating_filter()
        elif choice == '4':
            demo_export()
        elif choice == '5':
            demo_report()
        elif choice == '6':
            demo_advanced_exporter()
        elif choice == '7':
            demo_full_workflow()
        else:
            print("无效选择")

        print("\n演示完成！")

    except KeyboardInterrupt:
        print("\n\n用户中断演示")
    except Exception as e:
        print(f"\n演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
