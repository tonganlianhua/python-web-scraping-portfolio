"""
淘宝商品爬虫演示脚本
支持命令行参数配置
"""

import sys
import os
import argparse

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.scraper import TaobaoScraper
from src.exporter import DataExporter
from src.analyzer import DataAnalyzer


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='淘宝商品爬虫演示脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础演示
  python demo.py --keyword "手机" --pages 1

  # 高级演示（带筛选和排序）
  python demo.py --keyword "羽绒服" --category clothing --min-price 100 --max-price 500 --pages 3 --sort-by sales

  # 按价格升序排序
  python demo.py --keyword "笔记本" --pages 2 --sort-by price --sort-order asc
        """
    )

    # 搜索参数
    parser.add_argument('--keyword', type=str, required=True, help='搜索关键词（必需）')
    parser.add_argument('--category', type=str, choices=['all', 'clothing', 'digital', 'home_appliance', 'beauty', 'food', 'sports', 'books'],
                       default=None, help='商品分类')
    parser.add_argument('--min-price', type=float, default=None, help='最低价格')
    parser.add_argument('--max-price', type=float, default=None, help='最高价格')
    parser.add_argument('--sort-by', type=str, choices=['sales', 'price'], default='sales', help='排序方式：sales 或 price')
    parser.add_argument('--sort-order', type=str, choices=['asc', 'desc'], default='desc', help='排序顺序：asc 或 desc')
    parser.add_argument('--pages', type=int, default=1, help='爬取页数')
    parser.add_argument('--page-size', type=int, default=20, help='每页商品数量')

    # 输出参数
    parser.add_argument('--output-dir', type=str, default='data', help='输出目录')
    parser.add_argument('--export-csv', action='store_true', help='导出 CSV')
    parser.add_argument('--export-json', action='store_true', help='导出 JSON')
    parser.add_argument('--export-excel', action='store_true', help='导出 Excel')
    parser.add_argument('--export-all', action='store_true', help='导出所有格式')
    parser.add_argument('--generate-report', action='store_true', help='生成分析报告')

    # 反爬参数
    parser.add_argument('--delay-min', type=float, default=2, help='最小延时（秒）')
    parser.add_argument('--delay-max', type=float, default=4, help='最大延时（秒）')
    parser.add_argument('--max-retries', type=int, default=3, help='最大重试次数')

    args = parser.parse_args()

    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs('reports', exist_ok=True)

    print("=" * 60)
    print("🛒 淘宝商品爬虫演示")
    print("=" * 60)

    # 创建爬虫实例
    print(f"\n📋 配置信息:")
    print(f"  关键词: {args.keyword}")
    print(f"  分类: {args.category or '全部'}")
    if args.min_price and args.max_price:
        print(f"  价格区间: ¥{args.min_price} - ¥{args.max_price}")
    print(f"  排序方式: {args.sort_by} ({args.sort_order})")
    print(f"  爬取页数: {args.pages}")
    print(f"  每页数量: {args.page_size}")
    print(f"  延时范围: {args.delay_min}-{args.delay_max} 秒")

    scraper = TaobaoScraper(
        delay_range=(args.delay_min, args.delay_max),
        max_retries=args.max_retries
    )

    # 构建价格区间
    price_range = None
    if args.min_price is not None and args.max_price is not None:
        price_range = (args.min_price, args.max_price)

    # 爬取数据
    print(f"\n🔍 开始爬取...")
    products = scraper.search_all_pages(
        keyword=args.keyword,
        category=args.category,
        price_range=price_range,
        sort_by=args.sort_by,
        sort_order=args.sort_order,
        page_count=args.pages,
        page_size=args.page_size
    )

    if not products:
        print("\n❌ 没有爬取到任何数据")
        return

    print(f"\n✅ 爬取完成！共获取 {len(products)} 个商品")

    # 显示前 5 个商品
    print(f"\n📦 前 5 个商品:")
    for i, product in enumerate(products[:5], 1):
        print(f"  {i}. {product.get('title', 'N/A')}")
        print(f"     价格: ¥{product.get('price', 0):.2f} | 销量: {product.get('sales', 0)} | 店铺: {product.get('shop_name', 'N/A')}")

    # 导出数据
    exporter = DataExporter()

    base_filename = os.path.join(args.output_dir, f"{args.keyword}")

    if args.export_all or args.export_csv:
        csv_file = f"{base_filename}.csv"
        if exporter.export_csv(products, csv_file):
            print(f"\n📄 CSV 文件已导出: {csv_file}")

    if args.export_all or args.export_json:
        json_file = f"{base_filename}.json"
        if exporter.export_json(products, json_file):
            print(f"📄 JSON 文件已导出: {json_file}")

    if args.export_all or args.export_excel:
        excel_file = f"{base_filename}.xlsx"
        if exporter.export_excel(products, excel_file):
            print(f"📄 Excel 文件已导出: {excel_file}")

    # 生成分析报告
    if args.generate_report:
        print(f"\n📊 正在生成分析报告...")
        analyzer = DataAnalyzer(products)

        # 获取基础统计
        stats = analyzer.get_basic_stats()
        print(f"  商品总数: {stats.get('total_products', 0)}")
        print(f"  店铺数量: {stats.get('unique_shops', 0)}")
        if 'price' in stats:
            print(f"  价格范围: ¥{stats['price']['min']:.2f} - ¥{stats['price']['max']:.2f}")
        if 'sales' in stats:
            print(f"  总销量: {stats['sales']['total']}")

        # 生成报告
        report_file = analyzer.generate_report("reports/demo_report.html")
        print(f"\n📊 分析报告已生成: {report_file}")
        print(f"  请在浏览器中打开该文件查看详细报告")

    # 关闭爬虫
    scraper.close()

    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
