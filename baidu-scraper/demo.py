#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
百度百科爬虫演示脚本
展示所有主要功能
"""

from baidu_scraper import BaiduBaikeSpider
from exporter import DataExporter
from analyzer import DataAnalyzer
import os


def print_section(title):
    """打印章节标题"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def main():
    """主函数"""
    print("🕷️  百度百科爬虫 - 功能演示")
    print("="*80)
    
    # 创建爬虫实例
    spider = BaiduBaikeSpider()
    
    # 1. 演示搜索功能
    print_section("1. 搜索词条")
    keyword = "人工智能"
    print(f"搜索关键词: {keyword}")
    results = spider.search_entries(keyword)
    if results:
        print(f"找到 {len(results)} 个结果")
    
    # 2. 演示获取单个词条
    print_section("2. 获取单个词条")
    entry_titles = [
        "Python编程语言",
        "机器学习",
        "深度学习"
    ]
    
    entries = []
    for title in entry_titles:
        print(f"\n获取词条: {title}")
        entry = spider.get_entry(title)
        if entry:
            entries.append(entry)
            print(f"✓ 成功获取: {entry['title']}")
            print(f"  分类: {', '.join(entry['categories'])}")
            print(f"  摘要: {entry['summary'][:100]}..." if len(entry['summary']) > 100 else f"  摘要: {entry['summary']}")
            print(f"  编辑次数: {entry['edit_count']}")
            print(f"  浏览量: {entry['views']:,}")
        else:
            print(f"✗ 获取失败: {title}")
    
    # 3. 演示批量获取
    print_section("3. 批量获取词条")
    batch_titles = [
        "神经网络",
        "自然语言处理",
        "计算机视觉",
        "强化学习",
        "大数据"
    ]
    
    print(f"批量获取 {len(batch_titles)} 个词条...")
    batch_entries = spider.batch_get_entries(batch_titles)
    print(f"✓ 成功获取 {len(batch_entries)} 个词条")
    entries.extend(batch_entries)
    
    # 4. 演示分类筛选
    print_section("4. 按分类筛选")
    categories = ["计算机", "科学技术"]
    print(f"筛选分类: {', '.join(categories)}")
    
    filtered = spider.filter_by_category(entries, categories)
    print(f"✓ 筛选出 {len(filtered)} 个相关词条")
    for entry in filtered[:3]:
        print(f"  - {entry['title']}: {', '.join(entry['categories'])}")
    
    # 5. 演示数据导出
    print_section("5. 数据导出")
    
    # 创建输出目录
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 导出CSV
    csv_file = os.path.join(output_dir, "baidu_entries.csv")
    DataExporter.export_to_csv(entries, csv_file)
    
    # 导出JSON
    json_file = os.path.join(output_dir, "baidu_entries.json")
    DataExporter.export_to_json(entries, json_file)
    
    # 6. 演示数据分析
    print_section("6. 数据分析")
    
    if entries:
        analyzer = DataAnalyzer()
        report = analyzer.generate_report(entries)
        analyzer.print_report(report)
        
        # 保存分析报告
        report_file = os.path.join(output_dir, "analysis_report.json")
        analyzer.save_report_to_file(report, report_file)
    
    # 7. 演示热门词条
    print_section("7. 获取热门词条")
    print("正在获取热门词条...")
    hot_entries = spider.get_hot_entries(limit=5)
    print(f"✓ 获取了 {len(hot_entries)} 个热门词条")
    for entry in hot_entries:
        print(f"  - {entry['title']}: {entry['views']:,} 浏览")
    
    # 保存热门词条
    if hot_entries:
        hot_json = os.path.join(output_dir, "hot_entries.json")
        DataExporter.export_to_json(hot_entries, hot_json)
    
    print("\n" + "="*80)
    print("🎉 演示完成!")
    print("="*80)
    print(f"\n所有数据已保存到 {output_dir} 目录:")
    print(f"  - {csv_file}")
    print(f"  - {json_file}")
    print(f"  - {report_file}")
    if hot_entries:
        print(f"  - {hot_json}")
    
    print("\n💡 提示: 运行 python test.py 进行测试")


if __name__ == "__main__":
    main()
