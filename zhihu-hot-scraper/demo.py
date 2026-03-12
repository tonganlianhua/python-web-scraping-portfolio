"""
知乎热榜爬虫演示脚本
展示所有功能的使用方法
"""

from zhihu_scraper import ZhihuHotScraper
from data_exporter import DataExporter
import json
from datetime import datetime





def print_separator():
    """打印分隔线"""
    print("\n" + "=" * 80 + "\n")


def demo_basic():
    """演示：基本获取热榜"""
    print("【演示1】获取知乎热榜")
    print_separator()
    
    scraper = ZhihuHotScraper()
    hot_list = scraper.get_hot_list()
    
    print(f"获取到 {len(hot_list)} 个热榜话题\n")
    
    for item in hot_list[:10]:  # 显示前10个
        print(f"排名: {item['rank']}")
        print(f"标题: {item['title']}")
        print(f"热度: {item['hot_value']}")
        print(f"链接: {item['link']}")
        print(f"摘要: {item['excerpt'][:100] if item['excerpt'] else '无'}...")
        print("-" * 40)
    
    return hot_list


def demo_keyword_filter():
    """演示：关键词过滤"""
    print("【演示2】关键词过滤热榜")
    print_separator()
    
    scraper = ZhihuHotScraper()
    keyword = "科技"  # 可修改为其他关键词
    print(f"过滤关键词: {keyword}\n")
    
    hot_list = scraper.get_hot_list(keyword=keyword)
    
    print(f"找到 {len(hot_list)} 个相关话题\n")
    
    for item in hot_list:
        print(f"排名: {item['rank']} | 热度: {item['hot_value']} | {item['title']}")
    
    return hot_list


def demo_topic_detail():
    """演示：获取话题详情"""
    print("【演示3】获取话题详情")
    print_separator()
    
    scraper = ZhihuHotScraper()
    
    # 先获取热榜
    hot_list = scraper.get_hot_list()
    
    if hot_list:
        # 获取第一个话题的详情
        topic_url = hot_list[0]['link']
        print(f"获取话题详情: {hot_list[0]['title']}")
        print(f"URL: {topic_url}\n")
        
        detail = scraper.get_topic_detail(topic_url)
        
        print(f"回答数: {detail['answer_count']}")
        print(f"关注数: {detail['follower_count']}")
        print(f"浏览量: {detail['view_count']}")
        print(f"标签: {', '.join(detail['tags'])}")
    
    return hot_list


def demo_export_excel():
    """演示：导出Excel"""
    print("【演示4】导出Excel")
    print_separator()
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    print("正在获取热榜数据...")
    hot_list = scraper.get_hot_list()
    
    print("正在导出Excel...")
    filepath = exporter.export_to_excel(hot_list)
    
    print(f"\n✓ Excel文件已生成: {filepath}")
    
    return hot_list


def demo_compare_hot_values():
    """演示：对比热度变化"""
    print("【演示5】对比热度变化")
    print_separator()
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    print("第一次采集热榜...")
    hot_list_1 = scraper.get_hot_list()
    print(f"获取到 {len(hot_list_1)} 个话题\n")
    
    print("等待5秒后进行第二次采集...")
    import time
    time.sleep(5)
    
    print("第二次采集热榜...")
    hot_list_2 = scraper.get_hot_list()
    print(f"获取到 {len(hot_list_2)} 个话题\n")
    
    print("正在对比热度变化...")
    comparison = scraper.compare_hot_values(hot_list_1, hot_list_2)
    
    print("\n热度变化TOP10:")
    print("-" * 60)
    for item in comparison[:10]:
        status = item.get('status', '')
        if status == 'new':
            print(f"[新上榜] {item['title']}")
            print(f"  热度: {item['hot_value_2']}")
        elif status == 'dropped':
            print(f"[已下榜] {item['title']}")
            print(f"  热度变化: {item['change']:.0f}")
        else:
            change_symbol = "↑" if item['change'] > 0 else "↓"
            print(f"{item['title']}")
            print(f"  热度: {item['hot_value_1']:.0f} → {item['hot_value_2']:.0f} ({change_symbol} {abs(item['change']):.0f}, {item['change_percent']:.1f}%)")
        print("-" * 60)
    
    # 导出对比结果
    print("\n正在导出对比结果...")
    exporter.export_comparison_to_excel(comparison)
    exporter.generate_comparison_chart(comparison)
    
    return comparison


def demo_multiple_collection():
    """演示：多次采集并生成趋势图"""
    print("【演示6】多次采集并生成趋势图")
    print_separator()
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    collection_times = 3  # 采集次数
    interval = 10  # 采集间隔（秒）
    
    hot_history = []
    
    print(f"计划采集 {collection_times} 次，每次间隔 {interval} 秒\n")
    
    for i in range(collection_times):
        print(f"第 {i + 1} 次采集...")
        hot_list = scraper.get_hot_list()
        hot_history.append(hot_list)
        print(f"  获取到 {len(hot_list)} 个话题")
        
        if i < collection_times - 1:
            print(f"  等待 {interval} 秒后继续...\n")
            import time
            time.sleep(interval)
    
    print("\n生成趋势图...")
    exporter.generate_trend_chart(hot_history, top_n=5)
    
    print("\n各话题热度变化:")
    print("-" * 60)
    
    # 显示前5个话题的趋势
    top_topics = hot_history[0][:5]
    for topic in top_topics:
        title = topic['title']
        values = []
        for hot_list in hot_history:
            # 查找该话题在每次采集中的热度
            found = False
            for item in hot_list:
                if item['title'] == title:
                    values.append(item['hot_value'])
                    found = True
                    break
            if not found:
                values.append(0)
        
        values_str = " → ".join([f"{v:.0f}" for v in values])
        print(f"{title}")
        print(f"  热度趋势: {values_str}")
        print("-" * 60)


def demo_full_workflow():
    """演示：完整工作流"""
    print("【演示7】完整工作流")
    print_separator()
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    print("步骤1: 获取热榜")
    hot_list = scraper.get_hot_list()
    print(f"  ✓ 获取到 {len(hot_list)} 个话题\n")
    
    print("步骤2: 关键词过滤")
    tech_list = scraper.get_hot_list(keyword="科技")
    print(f"  ✓ 找到 {len(tech_list)} 个科技相关话题\n")
    
    print("步骤3: 获取话题详情")
    details = []
    for item in hot_list[:3]:  # 只获取前3个的详情
        detail = scraper.get_topic_detail(item['link'])
        details.append(detail)
        print(f"  ✓ {item['title']}: {detail['answer_count']} 回答")
    print()
    
    print("步骤4: 导出数据")
    exporter.export_to_excel(hot_list)
    exporter.export_detail_to_excel(details)
    print("  ✓ Excel文件已生成\n")
    
    print("步骤5: 等待5秒后第二次采集")
    import time
    time.sleep(5)
    
    print("步骤6: 第二次采集")
    hot_list_2 = scraper.get_hot_list()
    print(f"  ✓ 获取到 {len(hot_list_2)} 个话题\n")
    
    print("步骤7: 对比热度变化")
    comparison = scraper.compare_hot_values(hot_list, hot_list_2)
    exporter.export_comparison_to_excel(comparison)
    exporter.generate_comparison_chart(comparison)
    print("  ✓ 对比完成\n")
    
    print("✓ 完整工作流执行完毕！")


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("知乎热榜爬虫 - 功能演示")
    print("=" * 80)
    print("\n请选择演示内容:")
    print("1. 基本获取热榜")
    print("2. 关键词过滤")
    print("3. 获取话题详情")
    print("4. 导出Excel")
    print("5. 对比热度变化")
    print("6. 多次采集并生成趋势图")
    print("7. 完整工作流")
    print("0. 退出")
    print("=" * 80)
    
    choice = input("\n请输入选项 (0-7): ").strip()
    
    print_separator()
    
    if choice == "1":
        demo_basic()
    elif choice == "2":
        demo_keyword_filter()
    elif choice == "3":
        demo_topic_detail()
    elif choice == "4":
        demo_export_excel()
    elif choice == "5":
        demo_compare_hot_values()
    elif choice == "6":
        demo_multiple_collection()
    elif choice == "7":
        demo_full_workflow()
    elif choice == "0":
        print("退出演示")
        return
    else:
        print("无效选项")
        return
    
    print_separator()
    print("✓ 演示完成！")


if __name__ == "__main__":
    main()
