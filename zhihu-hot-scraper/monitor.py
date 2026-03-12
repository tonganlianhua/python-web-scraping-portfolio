"""
知乎热榜监控脚本
支持定时采集、自动导出和对比分析
"""

from zhihu_scraper import ZhihuHotScraper
from data_exporter import DataExporter
import time
from datetime import datetime
import argparse


class HotListMonitor:
    """热榜监控类"""

    def __init__(self, output_dir="output"):
        """初始化监控器"""
        self.scraper = ZhihuHotScraper()
        self.exporter = DataExporter(output_dir=output_dir)
        self.history = []
        self.last_hot_list = None

    def collect_once(self, keyword=None, export=True):
        """
        单次采集
        
        Args:
            keyword: 关键词过滤
            export: 是否导出Excel
            
        Returns:
            热榜数据列表
        """
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始采集...")
        
        hot_list = self.scraper.get_hot_list(keyword=keyword)
        
        if not hot_list:
            print("采集失败")
            return []
        
        print(f"采集成功，获取到 {len(hot_list)} 个话题")
        
        # 显示TOP10
        print("\nTOP10:")
        for item in hot_list[:10]:
            print(f"  #{item['rank']} {item['title']} ({item['hot_value']:,.0f})")
        
        # 记录历史
        self.history.append(hot_list)
        
        # 导出Excel
        if export:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.exporter.export_to_excel(hot_list, filename=f"monitor_{timestamp}")
        
        self.last_hot_list = hot_list
        return hot_list

    def monitor_loop(self, interval_minutes=10, 
                     max_iterations=None, 
                     keyword=None, 
                     auto_compare=True):
        """
        循环监控
        
        Args:
            interval_minutes: 采集间隔（分钟）
            max_iterations: 最大迭代次数（None表示无限）
            keyword: 关键词过滤
            auto_compare: 是否自动对比
        """
        print("=" * 80)
        print("知乎热榜监控启动")
        print("=" * 80)
        print(f"采集间隔: {interval_minutes} 分钟")
        print(f"关键词过滤: {keyword if keyword else '无'}")
        print(f"自动对比: {'是' if auto_compare else '否'}")
        if max_iterations:
            print(f"最大迭代次数: {max_iterations}")
        else:
            print("最大迭代次数: 无限（Ctrl+C停止）")
        print("=" * 80)
        
        iteration = 0
        try:
            while True:
                # 检查最大迭代次数
                if max_iterations and iteration >= max_iterations:
                    print(f"\n已达到最大迭代次数 ({max_iterations})，监控停止")
                    break
                
                iteration += 1
                print(f"\n=== 第 {iteration} 次采集 ===")
                
                # 采集热榜
                hot_list = self.collect_once(keyword=keyword, export=False)
                
                # 对比上一次结果
                if auto_compare and self.last_hot_list and len(self.history) >= 2:
                    print("\n热度变化:")
                    comparison = self.scraper.compare_hot_values(self.history[-2], hot_list)
                    
                    # 显示变化最大的5个
                    for item in comparison[:5]:
                        if item.get('status') == 'new':
                            print(f"  [新] #{item['title'][:30]}... (+{item['hot_value_2']:,.0f})")
                        elif item.get('status') == 'dropped':
                            print(f"  [下] #{item['title'][:30]}... ({item['change']:,.0f})")
                        else:
                            if item['change'] > 0:
                                print(f"  ↑ #{item['title'][:30]}... (+{item['change']:,.0f})")
                            elif item['change'] < 0:
                                print(f"  ↓ #{item['title'][:30]}... ({item['change']:,.0f})")
                
                # 等待下一次采集
                if not (max_iterations and iteration >= max_iterations):
                    print(f"\n等待 {interval_minutes} 分钟后继续...")
                    time.sleep(interval_minutes * 60)
        
        except KeyboardInterrupt:
            print("\n\n监控已停止（用户中断）")
        
        except Exception as e:
            print(f"\n\n监控出错: {str(e)}")
        
        finally:
            # 导出所有采集结果
            if self.history:
                print(f"\n正在导出 {len(self.history)} 次采集结果...")
                for i, hot_list in enumerate(self.history, 1):
                    self.exporter.export_to_excel(hot_list, filename=f"monitor_round_{i}")
                
                # 生成趋势图
                if len(self.history) > 1:
                    print("生成趋势图...")
                    self.exporter.generate_trend_chart(self.history, top_n=10)
                    print(f"✓ 趋势图已生成")
            
            print("\n监控结束")

    def batch_collect(self, times=3, interval_minutes=5, keyword=None):
        """
        批量采集
        
        Args:
            times: 采集次数
            interval_minutes: 间隔（分钟）
            keyword: 关键词过滤
        """
        self.monitor_loop(
            interval_minutes=interval_minutes,
            max_iterations=times,
            keyword=keyword,
            auto_compare=True
        )

    def generate_report(self):
        """生成监控报告"""
        if not self.history:
            print("没有采集数据")
            return
        
        print("\n" + "=" * 80)
        print("监控报告")
        print("=" * 80)
        print(f"采集次数: {len(self.history)}")
        print(f"采集时间: {len(self.history) * 5} 分钟（假设每次间隔5分钟）")
        print(f"数据范围: {self.history[0][0]['created_time']} - {self.history[-1][0]['created_time']}")
        
        # 分析TOP话题
        if self.history:
            print(f"\n首次采集TOP3:")
            for item in self.history[0][:3]:
                print(f"  #{item['rank']} {item['title']}")
            
            if len(self.history) > 1:
                print(f"\n最新采集TOP3:")
                for item in self.history[-1][:3]:
                    print(f"  #{item['rank']} {item['title']}")
        
        # 生成对比报告
        if len(self.history) >= 2:
            print(f"\n总体热度变化:")
            comparison = self.scraper.compare_hot_values(self.history[0], self.history[-1])
            
            # 统计
            new_count = sum(1 for item in comparison if item.get('status') == 'new')
            dropped_count = sum(1 for item in comparison if item.get('status') == 'dropped')
            increase_count = sum(1 for item in comparison if item['change'] > 0 and item.get('status') is None)
            decrease_count = sum(1 for item in comparison if item['change'] < 0 and item.get('status') is None)
            
            print(f"  新上榜: {new_count} 个")
            print(f"  已下榜: {dropped_count} 个")
            print(f"  热度上升: {increase_count} 个")
            print(f"  热度下降: {decrease_count} 个")
        
        # 生成图表
        if len(self.history) > 1:
            print(f"\n生成趋势分析图...")
            self.exporter.generate_trend_chart(self.history, top_n=10)
            
            # 对比第一次和最后一次
            comparison = self.scraper.compare_hot_values(self.history[0], self.history[-1])
            self.exporter.generate_comparison_chart(comparison)
            
            print("✓ 图表已生成")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='知乎热榜监控工具')
    
    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 单次采集命令
    once_parser = subparsers.add_parser('once', help='单次采集')
    once_parser.add_argument('--keyword', '-k', type=str, help='关键词过滤')
    once_parser.add_argument('--no-export', action='store_true', help='不导出Excel')
    
    # 监控命令
    monitor_parser = subparsers.add_parser('monitor', help='循环监控')
    monitor_parser.add_argument('--interval', '-i', type=int, default=10, 
                                 help='采集间隔（分钟），默认10')
    monitor_parser.add_argument('--times', '-t', type=int, help='最大采集次数')
    monitor_parser.add_argument('--keyword', '-k', type=str, help='关键词过滤')
    monitor_parser.add_argument('--no-compare', action='store_true', help='不自动对比')
    
    # 批量采集命令
    batch_parser = subparsers.add_parser('batch', help='批量采集')
    batch_parser.add_argument('--times', '-t', type=int, default=3, 
                              help='采集次数，默认3')
    batch_parser.add_argument('--interval', '-i', type=int, default=5, 
                              help='间隔（分钟），默认5')
    batch_parser.add_argument('--keyword', '-k', type=str, help='关键词过滤')
    
    args = parser.parse_args()
    
    # 创建监控器
    monitor = HotListMonitor()
    
    if args.command == 'once':
'        # 单次采集
        monitor.collect_once(keyword=args.keyword, export=not args.no_export)
    
    elif args.command == 'monitor':
        # 循环监控
        monitor.monitor_loop(
            interval_minutes=args.interval,
            max_iterations=args.times,
            keyword=args.keyword,
            auto_compare=not args.no_compare
        )
    
    elif args.command == 'batch':
        # 批量采集
        monitor.batch_collect(
            times=args.times,
            interval_minutes=args.interval,
            keyword=args.keyword
        )
        
        # 生成报告
        monitor.generate_report()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
