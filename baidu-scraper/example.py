#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用示例
展示如何组合使用各种功能
"""

from baidu_scraper import BaiduBaikeSpider
from exporter import DataExporter
from analyzer import DataAnalyzer
import os


def example_basic_usage():
    """基础使用示例"""
    print("\n" + "="*80)
    print("示例 1: 基础使用")
    print("="*80)
    
    spider = BaiduBaikeSpider()
    
    # 获取单个词条
    entry = spider.get_entry("Python")
    if entry:
        print(f"词条: {entry['title']}")
        print(f"摘要: {entry['summary'][:100]}...")
        print(f"分类: {', '.join(entry['categories'])}")
        print(f"编辑次数: {entry['edit_count']}")
        print(f"浏览量: {entry['views']:,}")


def example_batch_processing():
    """批量处理示例"""
    print("\n" + "="*80)
    print("示例 2: 批量处理")
    print("="*80)
    
    spider = BaiduBaikeSpider()
    
    # 定义要获取的词条
    titles = [
        "机器学习",
        "深度学习",
        "神经网络",
        "自然语言处理",
        "计算机视觉"
    ]
    
    print(f"批量获取 {len(titles)} 个词条...")
    entries = spider.batch_get_entries(titles)
    print(f"成功获取 {len(entries)} 个词条")
    
    # 打印摘要信息
    for entry in entries:
        print(f"  - {entry['title']}: {entry['views']:,} 浏览")


def example_filter_and_export():
    """筛选和导出示例"""
    print("\n" + "="*80)
    print("示例 3: 筛选和导出")
    print("="*80)
    
    spider = BaiduBaikeSpider()
    
    # 获取词条
    titles = ["Python", "Java", "JavaScript", "C++", "Go语言", "Rust"]
    entries = spider.batch_get_entries(titles)
    
    # 按分类筛选
    print("筛选分类: ['计算机', '编程语言']")
    filtered = spider.filter_by_category(entries, ["计算机", "编程语言"])
    print(f"筛选出 {len(filtered)} 个词条")
    
    # 导出数据
    os.makedirs("examples", exist_ok=True)
    
    DataExporter.export_to_csv(filtered, "examples/programming_languages.csv")
    DataExporter.export_to_json(filtered, "examples/programming_languages.json")
    
    print("数据已导出到 examples/ 目录")


def example_data_analysis():
    """数据分析示例"""
    print("\n" + "="*80)
    print("示例 4: 数据分析")
    print("="*80)
    
    spider = BaiduBaikeSpider()
    
    # 获取词条
    titles = [
        "人工智能", "大数据", "云计算", "区块链",
        "量子计算", "物联网", "5G", "元宇宙"
    ]
    
    entries = spider.batch_get_entries(titles)
    
    # 生成分析报告
    analyzer = DataAnalyzer()
    report = analyzer.generate_report(entries)
    
    # 打印报告
    analyzer.print_report(report)
    
    # 保存报告
    os.makedirs("examples", exist_ok=True)
    analyzer.save_report_to_file(report, "examples/tech_trends_report.json")


def example_search_and_collect():
    """搜索和收集示例"""
    print("\n" + "="*80)
    print("示例 5: 搜索和收集")
    print("="*80)
    
    spider = BaiduBaikeSpider()
    
    # 搜索关键词
    keywords = ["算法", "数据结构", "操作系统", "数据库"]
    
    all_entries = []
    for keyword in keywords:
        print(f"搜索: {keyword}")
        results = spider.search_entries(keyword)
        if results:
            all_entries.extend(results)
    
    print(f"共收集到 {len(all_entries)} 个词条")
    
    # 导出结果
    if all_entries:
        os.makedirs("examples", exist_ok=True)
        DataExporter.export_to_csv(all_entries, "examples/search_results.csv")
        print("搜索结果已导出")


def example_complete_workflow():
    """完整工作流示例"""
    print("\n" + "="*80)
    print("示例 6: 完整工作流")
    print("="*80)
    
    spider = BaiduBaikeSpider()
    analyzer = DataAnalyzer()
    
    # 步骤 1: 获取词条
    print("步骤 1: 获取词条")
    titles = [
        "Python", "Java", "JavaScript", "C++",
        "机器学习", "深度学习", "人工智能"
    ]
    entries = spider.batch_get_entries(titles)
    print(f"  获取了 {len(entries)} 个词条")
    
    # 步骤 2: 筛选分类
    print("\n步骤 2: 筛选计算机相关词条")
    filtered = spider.filter_by_category(entries, ["计算机"])
    print(f"  筛选出 {len(filtered)} 个词条")
    
    # 步骤 3: 数据分析
    print("\n步骤 3: 生成分析报告")
    report = analyzer.generate_report(filtered)
    
    # 步骤 4: 导出数据
    print("\n步骤 4: 导出数据")
    os.makedirs("examples", exist_ok=True)
    
    DataExporter.export_to_csv(filtered, "examples/final_results.csv")
    DataExporter.export_to_json(filtered, "examples/final_results.json")
    analyzer.save_report_to_file(report, "examples/final_report.json")
    
    print("  数据已导出到 examples/ 目录")
    
    # 步骤 5: 显示摘要
    print("\n步骤 5: 数据摘要")
    summary = report['summary']
    print(f"  词条总数: {summary['total_entries']}")
    print(f"  总浏览量: {summary['total_views']:,}")
    print(f"  平均浏览量: {summary['average_views']:,.2f}")


def main():
    """主函数"""
    print("\n" + "="*80)
    print("📘 百度百科爬虫 - 使用示例")
    print("="*80)
    print("\n这个脚本展示了如何使用爬虫的各种功能")
    print("每个示例都是独立的，可以根据需要修改和扩展")
    
    try:
        # 运行所有示例
        example_basic_usage()
        example_batch_processing()
        example_filter_and_export()
        example_data_analysis()
        example_search_and_collect()
        example_complete_workflow()
        
        print("\n" + "="*80)
        print("✅ 所有示例运行完成!")
        print("="*80)
        print("\n生成的文件保存在 examples/ 目录中")
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
