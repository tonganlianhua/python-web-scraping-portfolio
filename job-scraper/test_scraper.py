#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫测试脚本
测试基本功能（不实际爬取，只验证代码结构）
"""

import sys
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_imports():
    """测试依赖包是否正确安装"""
    print("正在检查依赖包...")
    
    try:
        import requests
        print("[OK] requests 已安装")
    except ImportError:
        print("[FAIL] requests 未安装")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("[OK] beautifulsoup4 已安装")
    except ImportError:
        print("[FAIL] beautifulsoup4 未安装")
        return False
    
    try:
        import pandas as pd
        print("[OK] pandas 已安装")
    except ImportError:
        print("[FAIL] pandas 未安装")
        return False
    
    try:
        import matplotlib
        print("[OK] matplotlib 已安装")
    except ImportError:
        print("[FAIL] matplotlib 未安装")
        return False
    
    return True

def test_salary_parsing():
    """测试薪资解析功能"""
    print("\n正在测试薪资解析功能...")
    
    from job_scraper import LagouJobScraper
    
    scraper = LagouJobScraper()
    
    test_cases = [
        ("15k-25k", (15, 25)),
        ("10k-20k", (10, 20)),
        ("30k-50k", (30, 50)),
        ("25k-35k", (25, 35)),
        ("20k-30k", (20, 30)),
    ]
    
    all_passed = True
    for salary_str, expected in test_cases:
        result = scraper.parse_salary(salary_str)
        if result == expected:
            print(f"[OK] {salary_str} -> {result}")
        else:
            print(f"[FAIL] {salary_str} -> {result} (期望: {expected})")
            all_passed = False
    
    return all_passed

def main():
    """主测试函数"""
    print("="*60)
    print("求职信息爬虫 - 代码结构测试")
    print("="*60)
    
    # 测试依赖包
    if not test_imports():
        print("\n错误：依赖包未全部安装，请运行:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # 测试薪资解析
    if not test_salary_parsing():
        print("\n错误：薪资解析功能测试失败")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("所有测试通过！[OK]")
    print("="*60)
    print("\n代码结构验证成功，可以开始使用爬虫了！")
    print("\n使用方法：")
    print("  python job_scraper.py")
    print("\n然后按照提示输入搜索关键词即可")

if __name__ == "__main__":
    main()
