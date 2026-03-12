"""
使用示例集合
展示各种项目场景的使用方法
"""

from zhihu_scraper import ZhihuHotScraper
from data_exporter import DataExporter
import time


def example_1_daily_hot():
    """场景1: 每日热榜快照"""
    print("=" * 80)
    print("场景1: 每日热榜快照")
    print("=" * 80)
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    # 获取热榜
    hot_list = scraper.get_hot_list()
    
    # 导出为Excel
    filepath = exporter.export_to_excel(hot_list, filename="daily_snapshot")
    
    print(f"✓ 每日快照已保存: {filepath}")


def example_2_track_keywords():
    """场景2: 追踪特定关键词"""
    print("\n" + "=" * 80)
    print("场景2: 追踪特定关键词")
    print("=" * 80)
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    keywords = ["科技", "AI", "创业"]  # 可修改为感兴趣的关键词
    
    all_results = {}
    
    for keyword in keywords:
        print(f"\n搜索: {keyword}")
        results = scraper.get_hot_list(keyword=keyword)
        all_results[keyword] = results
        print(f"  找到 {len(results)} 个话题")
    
    # 保存结果
    for keyword, results in all_results.items():
        if results:
            exporter.export_to_excel(results, filename=f"keyword_{keyword}")


def example_3_monitor_trending():
    """场景3: 监控热门趋势"""
    print("\n" + "=" * 80)
    print("场景3: 监控热门趋势")
    print("=" * 80)
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    hot_history = []
    rounds = 3  # 采集3次
    
    for i in range(rounds):
        print(f"\n第 {i + 1}/{rounds} 次采集...")
        hot_list = scraper.get_hot_list()
        hot_history.append(hot_list)
        
        if i < rounds - 1:
            print("  等待10秒后继续...")
            time.sleep(10)
    
    # 生成趋势图
    print("\n生成趋势分析...")
    exporter.generate_trend_chart(hot_history, top_n=10)
    
    # 导出所有采集结果
    for i, hot_list in enumerate(hot_history, 1):
        exporter.export_to_excel(hot_list, filename=f"trend_round_{i}")


def example_4_topic_analysis():
    """场景4: 深度话题分析"""
    print("\n" + "=" * 80)
    print("场景4: 深度话题话题分析")
    print("=" * 80)
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    # 获取热榜
    hot_list = scraper.get_hot_list()
    
    # 分析TOP3话题
    print("\n分析TOP3话题:")
    details = []
    
    for i, item in enumerate(hot_list[:3], 1):
        print(f"\n{i}. {item['title']}")
        detail = scraper.get_topic_detail(item['link'])
        details.append(detail)
        
        print(f"   回答数: {detail['answer_count']}")
        print(f"   关注数: {detail['follower_count']}")
        print(f"   浏览量: {detail['view_count']}")
        print(f"   标签: {', '.join(detail['tags'][:5])}")
    
    # 导出详情
    exporter.export_detail_to_excel(details, filename="topic_analysis")


def example_5_hot_change():
    """场景5: 检测热度异常变化"""
    print("\n" + "=" * 80)
    print("场景5: 检测热度异常变化")
    print("=" * 80)
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    # 第一次采集
    print("第一次采集...")
    hot_list_1 = scraper.get_hot_list()
    
    # 等待
    print("等待10秒...")
    time.sleep(10)
    
    # 第二次采集
    print("第二次采集...")
    hot_list_2 = scraper.get_hot_list()
    
    # 对比
    print("\n检测热度变化...")
    comparison = scraper.compare_hot_values(hot_list_1, hot_list_2)
    
    # 找出变化最大的话题
    print("\n热度变化TOP5:")
    for item in comparison[:5]:
        change_percent = item.get('change_percent', 0)
        
        if change_percent > 20:
            print(f"⚠️ 大幅上升: {item['title'][:40]}... (+{change_percent:.1f}%)")
        elif change_percent < -20:
            print(f"⚠️ 大幅下降: {item['title'][:40]}... ({change_percent:.1f}%)")
        else:
            symbol = "↑" if item['change'] > 0 else "↓"
            print(f"  {symbol} {item['title'][:40]}... ({change_percent:+.1f}%)")
    
    # 导出对比结果
    exporter.export_comparison_to_excel(comparison)
    exporter.generate_comparison_chart(comparison)


def example_6_custom_report():
    """场景6: 自定义报告"""
    print("\n" + "=" * 80)
    print("场景6: 自定义报告")
    print("=" * 80)
    
    scraper = ZhihuHotScraper()
    exporter = DataExporter()
    
    # 获取热榜
    hot_list = scraper.get_hot_list()
    
    # 生成自定义报告
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("知乎热榜报告")
    report_lines.append("=" * 80)
    report_lines.append(f"生成时间: {hot_list[0]['created'] if hot_list else 'N/A'}")
    report_lines.append(f"话题总数: {len(hot_list)}")
    report_lines.append("")
    
    # TOP10
    report_lines.append("TOP10热门话题:")
    report_lines.append("-" * 80)
    for item in hot_list[:10]:
        report_lines.append(f"#{item['rank']:<3} {item['title']}")
        report_lines.append(f"     热度: {item['hot_value']:,.0f} | 链接: {item['link']}")
        report_lines.append("")
    
    # 热度分布
    report_lines.append("热度分布:")
    report_lines.append("-" * 80)
    if hot_list:
        max_hot = max(item['hot_value'] for item in hot_list)
        min_hot = min(item['hot_value'] for item in hot_list)
        avg_hot = sum(item['hot_value'] for item in hot_list) / len(hot_list)
        
        report_lines.append(f"最高热度: {max_hot:,.0f}")
        report_lines.append(f"最低热度: {min_hot:,.0f}")
        report_lines.append(f"平均热度: {avg_hot:,.0f}")
    
    # 保存报告
    report_text = "\n".join(report_lines)
    with open("output/custom_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
    
    print(report_text)
    print("\n✓ 自定义报告已保存到 output/custom_report.txt")


def main():
    """主函数"""
    print("\n知乎热榜爬虫 - 使用示例集")
    print("运行所有示例场景\n")
    
    try:
        # 运行所有示例
        example_1_daily_hot()
        example_2_track_keywords()
        example_3_monitor_trending()
        example_4_topic_analysis()
        example_5_hot_change()
        example_6_custom_report()
        
        print("\n" + "=" * 80)
        print("✓ 所有示例执行完毕集")
        print("=" * 80)
        print("\n提示: 查看output目录获取所有生成的文件")
    
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
