#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
百度百科爬虫测试脚本
测试所有主要功能
"""

import sys
import io
# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from baidu_scraper import BaiduBaikeSpider
from exporter import DataExporter
from analyzer import DataAnalyzer
import os


class TestResult:
    """测试结果类"""
    
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, test_name):
        """添加通过测试"""
        self.total += 1
        self.passed += 1
        print(f"✓ PASS: {test_name}")
    
    def add_fail(self, test_name, reason):
        """添加失败测试"""
        self.total += 1
        self.failed += 1
        print(f"✗ FAIL: {test_name}")
        print(f"  原因: {reason}")
        self.errors.append((test_name, reason))
    
    def summary(self):
        """打印测试摘要"""
        print("\n" + "="*80)
        print("测试摘要")
        print("="*80)
        print(f"总测试数: {self.total}")
        print(f"通过: {self.passed}")
        print(f"失败: {self.failed}")
        print(f"通过率: {(self.passed/self.total*100):.1f}%")
        
        if self.errors:
            print("\n失败详情:")
            for test_name, reason in self.errors:
                print(f"  - {test_name}: {reason}")
        
        return self.failed == 0


def test_spider_initialization():
    """测试爬虫初始化"""
    spider = BaiduBaikeSpider()
    
    result = TestResult()
    
    # 检查基本属性
    if hasattr(spider, 'base_url') and spider.base_url:
        result.add_pass("爬虫初始化 - base_url")
    else:
        result.add_fail("爬虫初始化 - base_url", "未正确设置")
    
    if hasattr(spider, 'user_agents') and len(spider.user_agents) > 0:
        result.add_pass("爬虫初始化 - user_agents")
    else:
        result.add_fail("爬虫初始化 - user_agents", "未正确设置")
    
    if hasattr(spider, 'headers') and spider.headers:
        result.add_pass("爬虫初始化 - headers")
    else:
        result.add_fail("爬虫初始化 - headers", "未正确设置")
    
    return result


def test_search_functionality():
    """测试搜索功能"""
    spider = BaiduBaikeSpider()
    result = TestResult()
    
    # 测试搜索
    keyword = "Python"
    try:
        results = spider.search_entries(keyword)
        if isinstance(results, list):
            result.add_pass(f"搜索功能 - 返回列表")
        else:
            result.add_fail(f"搜索功能 - 返回列表", f"返回类型错误: {type(results)}")
    except Exception as e:
        result.add_fail("搜索功能 - 执行", str(e))
    
    return result


def test_get_entry():
    """测试获取词条"""
    spider = BaiduBaikeSpider()
    result = TestResult()
    
    # 测试获取词条
    title = "机器学习"
    try:
        entry = spider.get_entry(title)
        if entry:
            result.add_pass(f"获取词条 - 成功获取")
            
            # 检查必需字段
            required_fields = ['title', 'url', 'summary', 'categories']
            for field in required_fields:
                if field in entry:
                    result.add_pass(f"获取词条 - 字段 {field}")
                else:
                    result.add_fail(f"获取词条 - 字段 {field}", "字段缺失")
        else:
            result.add_fail("获取词条 - 返回值", "返回None")
    except Exception as e:
        result.add_fail("获取词条 - 执行", str(e))
    
    return result


def test_batch_get_entries():
    """测试批量获取词条"""
    spider = BaiduBaikeSpider()
    result = TestResult()
    
    # 测试批量获取
    titles = ["算法", "数据结构", "计算机网络"]
    try:
        entries = spider.batch_get_entries(titles)
        if isinstance(entries, list):
            result.add_pass("批量获取 - 返回列表")
            
            if len(entries) > 0:
                result.add_pass(f"批量获取 - 获取到 {len(entries)} 个词条")
            else:
                result.add_fail("批量获取 - 数量", "未获取到任何词条")
        else:
            result.add_fail("批量获取 - 返回类型", f"返回类型错误: {type(entries)}")
    except Exception as e:
        result.add_fail("批量获取 - 执行", str(e))
    
    return result


def test_filter_by_category():
    """测试分类筛选"""
    spider = BaiduBaikeSpider()
    result = TestResult()
    
    # 创建测试数据
    test_entries = [
        {
            'title': 'Python',
            'categories': ['计算机', '编程语言'],
            'views': 1000
        },
        {
            'title': '地理',
            'categories': ['地理科学', '自然'],
            'views': 500
        },
        {
            'title': '人工智能',
            'categories': ['计算机', '科学技术'],
            'views': 2000
        }
    ]
    
    try:
        filtered = spider.filter_by_category(test_entries, ['计算机'])
        if len(filtered) == 2:
            result.add_pass("分类筛选 - 正确筛选")
        else:
            result.add_fail("分类筛选 - 数量", f"期望2个，实际{len(filtered)}个")
    except Exception as e:
        result.add_fail("分类筛选 - 执行", str(e))
    
    return result


def test_data_exporter():
    """测试数据导出"""
    result = TestResult()
    
    # 创建测试数据
    test_entries = [
        {
            'title': 'Python',
            'url': 'https://baike.baidu.com/item/Python',
            'summary': 'Python是一种编程语言',
            'intro': 'Python是一种高级编程语言',
            'categories': ['计算机'],
            'content': 'Python的内容...',
            'edit_count': 100,
            'views': 1000,
            'labels': ['编程']
        }
    ]
    
    # 创建输出目录
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 测试CSV导出
    csv_file = os.path.join(output_dir, "test_entries.csv")
    try:
        DataExporter.export_to_csv(test_entries, csv_file)
        if os.path.exists(csv_file):
            result.add_pass("导出CSV - 文件创建")
        else:
            result.add_fail("导出CSV - 文件创建", "文件不存在")
    except Exception as e:
        result.add_fail("导出CSV - 执行", str(e))
    
    # 测试JSON导出
    json_file = os.path.join(output_dir, "test_entries.json")
    try:
        DataExporter.export_to_json(test_entries, json_file)
        if os.path.exists(json_file):
            result.add_pass("导出JSON - 文件创建")
        else:
            result.add_fail("导出JSON - 文件创建", "文件不存在")
    except Exception as e:
        result.add_fail("导出JSON - 执行", str(e))
    
    return result


def test_data_analyzer():
    """测试数据分析"""
    result = TestResult()
    
    # 创建测试数据
    test_entries = [
        {
            'title': 'Python',
            'categories': ['计算机', '编程语言'],
            'views': 1000,
            'edit_count': 100,
            'content': 'Python的内容...'
        },
        {
            'title': '地理',
            'categories': ['地理科学'],
            'views': 500,
            'edit_count': 50,
            'content': '地理的内容...'
        },
        {
            'title': '人工智能',
            'categories': ['计算机', '科学技术'],
            'views': 2000,
            'edit_count': 200,
            'content': '人工智能的内容...'
        }
    ]
    
    try:
        analyzer = DataAnalyzer()
        report = analyzer.generate_report(test_entries)
        
        if 'summary' in report:
            result.add_pass("数据分析 - 生成报告")
        else:
            result.add_fail("数据分析 - 生成报告", "报告格式错误")
        
        if 'category_distribution' in report:
            result.add_pass("数据分析 - 分类分析")
        else:
            result.add_fail("数据分析 - 分类分析", "分类分析失败")
        
        if 'popular_entries' in report:
            result.add_pass("数据分析 - 热门词条")
        else:
            result.add_fail("数据分析 - 热门词条", "热门词条分析失败")
    except Exception as e:
        result.add_fail("数据分析 - 执行", str(e))
    
    return result


def main():
    """主测试函数"""
    print("\n" + "="*80)
    print("🧪 百度百科爬虫测试套件")
    print("="*80)
    
    all_results = []
    
    # 运行所有测试
    print("\n测试爬虫初始化...")
    all_results.append(test_spider_initialization())
    
    print("\n测试搜索功能...")
    all_results.append(test_search_functionality())
    
    print("\n测试获取词条...")
    all_results.append(test_get_entry())
    
    print("\n测试批量获取...")
    all_results.append(test_batch_get_entries())
    
    print("\n测试分类筛选...")
    all_results.append(test_filter_by_category())
    
    print("\n测试数据导出...")
    all_results.append(test_data_exporter())
    
    print("\n测试数据分析...")
    all_results.append(test_data_analyzer())
    
    # 汇总结果
    total_tests = sum(r.total for r in all_results)
    total_passed = sum(r.passed for r in all_results)
    total_failed = sum(r.failed for r in all_results)
    
    print("\n" + "="*80)
    print("📊 最终测试结果")
    print("="*80)
    print(f"总测试数: {total_tests}")
    print(f"通过: {total_passed}")
    print(f"失败: {total_failed}")
    print(f"通过率: {(total_passed/total_tests*100):.1f}%")
    
    if total_failed == 0:
        print("\n🎉 所有测试通过!")
        return 0
    else:
        print(f"\n⚠️  有 {total_failed} 个测试失败")
        return 1


if __name__ == "__main__":
    exit(main())
