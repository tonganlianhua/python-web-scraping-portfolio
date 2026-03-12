"""
快速入门脚本
演示最常用的功能
"""

from zhihu_scraper import ZhihuHotScraper
from data_exporter import DataExporter
import time


def simple_example():
    """最简单的使用示例"""
    print("【快速入门】获取知乎热榜TOP10\n")
    
    # 创建爬虫
    scraper = ZhihuHotScraper()
    
    # 获取热榜
    hot_list = scraper.get_hot_list()
    
    # 显示前10个
    for item in hot_list[:10]:
        print(f"#{item['rank']} {item['title']}")
        print(f"热度: {item['hot_value']:,.0f}")
        print(f"链接: {item['link']}")
        print("-" * 60)


def keyword_example():
    """关键词过滤示例"""
    print("\n【关键词过滤】查找科技类话题\n")
    
    scraper = ZhihuHotScraper()
    
    # 查找包含"科技"的话题
    tech_list = scraper.get_hot_list(keyword="科技")
    
    print(f"找到 {len(tech_list)} 个科技相关话题:\n")
    for item in tech_list:
        print(f"#{item['rank']} {item['title']}")


def export_example():
    """导出Excel示例"""
    print("\n【导出Excel】保存热榜数据\n")
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    # 获取热榜
    hot_list = scraper.get_hot_list()
    
    # 导出到Excel
    filepath = exporter.export_to_excel(hot_list, filename="hot_list")
    
    print(f"✓ 已导出到: {filepath}")


def compare_example():
    """对比热度变化示例"""
    print("\n【热度对比】监测热度变化\n")
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    print("第一次采集...")
    hot_list_1 = scraper.get_hot_list()
    
    print("等待5秒后第二次采集...")
    time.sleep(5)
    
    print("第二次采集...")
    hot_list_2 = scraper.get_hot_list()
    
    print("\n对比结果:")
    print("-" * 60)
    
    comparison = scraper.compare_hot_values(hot_list_1, hot_list_2)
    
    # 显示变化最大的5个话题
    for item in comparison[:5]:
        if item['change'] > 0:
            print(f"↑ {item['title']}: +{item['change']:.0f}")
        else:
            print(f"↓ {item['title']}: {item['change']:.0f}")


def main():
    """主函数"""
    print("=" * 80)
    print("知乎热榜爬虫 - 快速入门")
    print("=" * 80)
    
    # 运行所有示例
    simple_example()
    keyword_example()
    export_example()
    compare_example()
    
    print("\n" + "=" * 80)
    print("✓ 快速入门演示完毕！")
    print("=" * 80)
    print("\n提示: 运行 'python demo.py' 查看更多功能")
    print("      运行 'python test_scraper.py' 运行测试")


if __name__ == "__main__":
    main()
