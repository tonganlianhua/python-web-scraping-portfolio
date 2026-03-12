"""
快速演示脚本
使用模拟数据展示所有功能
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.exporter import DataExporter
from src.analyzer import DataAnalyzer


def create_mock_data():
    """创建模拟数据商品"""
    shops = [
        {'name': '天猫官方旗舰店', 'location': '杭州', 'score': 5.0},
        {'name': '京东自营', 'location': '北京', 'score': 4.9},
        {'name': '苏宁易购', 'location': '南京', 'score': 4.8},
        {'name': '国美在线', 'location': '上海', 'score': 4.7},
        {'name': '1号店', 'location': '广州', 'score': 4.6},
    ]

    products = []

    # 创建 20 个模拟商品
    categories = ['手机', '笔记本', '平板', '耳机', '手表']
    for i in range(20):
        shop = shops[i % len(shops)]
        category = categories[i % len(categories)]

        product = {
            'title': f'{category} 2024新款 高性能版 {i+1}',
            'price': float(1000 + i * 500 + (i % 5) * 100),  # 价格 1000-11000
            'sales': int(1000 * (i % 10 + 1)),  # 销量 1000-10000
            'shop_name': shop['name'],
            'shop_score': shop['score'],
            'shop_location': shop['location'],
            'product_url': f'https://example.com/product/{i+1}',
            'shop_url': f'https://example.com/shop/{i % 5 + 1}',
            'image_url': f'https://example.com/images/product_{i+1}.jpg',
        }
        products.append(product)

    return products


def main():
    """主函数"""
    print("=" * 70)
    print("淘宝商品爬虫 - 快速演示（使用模拟数据）")
    print("=" * 70)

    # 创建模拟数据
    print("\n[1/4] 创建模拟数据...")
    products = create_mock_data()
    print(f"      成功创建 {len(products)} 个商品")

    # 显示前 3 个商品
    print("\n      前 3 个商品预览:")
    for i, product in enumerate(products[:3], 1):
        print(f"      {i}. {product['title']}")
        print(f"         价格: {product['price']:.2f}元 | 销量: {product['sales']} | 店铺: {product['shop_name']}")

    # 导出数据
    print("\n[2/4] 导出数据...")
    exporter = DataExporter()

    # 创建输出目录
    os.makedirs('demo_output', exist_ok=True)

    # 导出所有格式
    results = exporter.export_all(products, 'demo_output/products')
    print(f"      CSV: {'成功' if results['csv'] else '失败'}")
    print(f"      JSON: {'成功' if results['json'] else '失败'}")
    print(f"      Excel: {'成功' if results['excel'] else '失败'}")

    # 数据分析
    print("\n[3/4] 数据分析...")
    analyzer = DataAnalyzer(products)

    stats = analyzer.get_basic_stats()
    print(f"      商品总数: {stats['total_products']}")
    print(f"      店铺数量: {stats['unique_shops']}")
    print(f"      价格范围: {stats['price']['min']:.2f}元 - {stats['price']['max']:.2f}元")
    print(f"      平均价格: {stats['price']['mean']:.2f}元")
    print(f"      总销量: {stats['sales']['total']:,}")

    # TOP 3 商品
    top_products = analyzer.get_top_products_by_sales(3)
    print(f"\n      TOP 3 畅销商品:")
    for i, product in enumerate(top_products, 1):
        print(f"      {i}. {product['title'][:30]}... - 销量: {product['sales']:,}")

    # TOP 3 店铺
    top_shops = analyzer.get_top_shops_by_sales(3)
    print(f"\n      TOP 3 店铺（按销量）:")
    for i, shop in enumerate(top_shops, 1):
        print(f"      {i}. {shop['shop_name']} - 销量: {shop['sales']:,}")

    # 生成报告
    print("\n[4/4] 生成分析报告...")
    os.makedirs('demo_output/reports', exist_ok=True)
    report_file = analyzer.generate_report('demo_output/reports/analysis.html')
    print(f"      报告已生成: {report_file}")

    print("\n" + "=" * 70)
    print("演示完成！")
    print("=" * 70)
    print("\n生成的文件:")
    print("  - demo_output/products.csv")
    print("  - demo_output/products.json")
    print("  - demo_output/products.xlsx")
    print("  - demo_output/reports/analysis.html (请在浏览器中打开查看)")
    print("\n" + "=" * 70)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
