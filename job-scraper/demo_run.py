#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示运行脚本 - 自动执行一次完整的爬取流程
"""

import sys
import io
from job_scraper import LagouJobScraper

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    """主函数"""
    print("="*70)
    print("求职信息爬虫 - 演示运行")
    print("="*70)
    print()
    
    # 创建爬虫实例
    scraper = LagouJobScraper()
    
    # 演示参数
    keyword = "Python开发"
    city = "北京"
    page_count = 3
    
    print(f"搜索关键词：{keyword}")
    print(f"城市：{city}")
    print(f"爬取页数：{page_count}")
    print()
    
    # 爬取职位信息
    jobs = scraper.search_jobs(keyword=keyword, city=city, page_count=page_count)
    
    if jobs:
        # 保存数据
        csv_filename = f"{keyword}_jobs.csv"
        scraper.save_to_csv(jobs, csv_filename)
        
        # 生成报告
        scraper.generate_report(jobs, keyword)
        
        # 生成可视化
        scraper.visualize_salary(jobs, keyword)
        
        print("="*70)
        print("爬取完成！")
        print("="*70)
        print(f"\n生成的文件：")
        print(f"  - 数据文件：{csv_filename}")
        print(f"  - 分析图表：{keyword}_salary_analysis.png")
        print("\n提示：")
        print("  - CSV文件可以用Excel打开查看详细职位信息")
        print("  - PNG图片包含薪资分布分析图表")
        print()
    else:
        print("\n未获取到职位数据")

if __name__ == "__main__":
    main()
