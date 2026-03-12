"""
淘宝商品爬虫测试脚本
包含单元测试和集成测试
"""

import unittest
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.scraper import TaobaoScraper
from src.exporter import DataExporter
from src.analyzer import DataAnalyzer


class TestTaobaoScraper(unittest.TestCase):
    """爬虫测试类"""

    def setUp(self):
        """测试前准备"""
        self.scraper = TaobaoScraper(delay_range=(0.5, 1))

    def tearDown(self):
        """测试后清理"""
        self.scraper.close()

    def test_scraper_initialization(self):
        """测试爬虫初始化"""
        self.assertIsNotNone(self.scraper)
        self.assertIsNotNone(self.scraper.anti_spider)

    def test_search_with_keyword(self):
        """测试关键词搜索"""
        products = self.scraper.search(
            keyword="测试商品",
            page_num=1,
            page_size=5
        )
        self.assertIsInstance(products, list)
        print(f"搜索结果: {len(products)} 个商品")

    def test_search_with_empty_keyword(self):
        """测试空关键词"""
        products = self.scraper.search(keyword="", page_num=1)
        self.assertIsInstance(products, list)

    def test_build_search_url(self):
        """测试 URL 构建"""
        url = self.scraper._build_search_url(
            keyword="手机",
            category="digital",
            page_num=1
        )
        self.assertIn("手机", url)
        self.assertIn("taobao.com", url)
        print(f"生成的 URL: {url}")


class TestDataExporter(unittest.TestCase):
    """导出器测试类"""

    def setUp(self):
        """测试前准备"""
        self.exporter = DataExporter()
        self.test_data = [
            {
                'title': '测试商品1',
                'price': 100.0,
                'sales': 1000,
                'shop_name': '测试店铺',
                'shop_score': 5.0,
                'shop_location': '北京',
                'product_url': 'https://example.com/1',
            },
            {
                'title': '测试商品2',
                'price': 200.0,
                'sales': 2000,
                'shop_name': '测试店铺2',
                'shop_score': 4.8,
                'shop_location': '上海',
                'product_url': 'https://example.com/2',
            }
        ]
        self.test_dir = os.path.join(project_root, 'tests', 'test_output')

    def test_export_csv(self):
        """测试 CSV 导出"""
        filename = os.path.join(self.test_dir, 'test.csv')
        result = self.exporter.export_csv(self.test_data, filename)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

    def test_export_json(self):
        """测试 JSON 导出"""
        filename = os.path.join(self.test_dir, 'test.json')
        result = self.exporter.export_json(self.test_data, filename)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

    def test_export_excel(self):
        """测试 Excel 导出"""
        filename = os.path.join(self.test_dir, 'test.xlsx')
        result = self.exporter.export_excel(self.test_data, filename)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

    def test_export_all(self):
        """测试导出所有格式"""
        base_filename = os.path.join(self.test_dir, 'test_all')
        results = self.exporter.export_all(self.test_data, base_filename)
        self.assertTrue(results['csv'])
        self.assertTrue(results['json'])
        self.assertTrue(results['excel'])

    def test_get_summary(self):
        """测试获取摘要"""
        summary = self.exporter.get_summary(self.test_data)
        self.assertIn('total', summary)
        self.assertEqual(summary['total'], 2)
        self.assertIn('price', summary)
        self.assertIn('sales', summary)
        print(f"数据摘要: {summary}")

    def test_filter_fields(self):
        """测试字段过滤"""
        fields = ['title', 'price']
        filtered = self.exporter.filter_fields(self.test_data, fields)
        self.assertEqual(len(filtered), 2)
        self.assertIn('title', filtered[0])
        self.assertIn('price', filtered[0])
        self.assertNotIn('sales', filtered[0])

    def tearDown(self):
        """测试后清理"""
        # 删除测试输出文件
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)


class TestDataAnalyzer(unittest.TestCase):
    """分析器测试类"""

    def setUp(self):
        """测试前准备"""
        self.test_data = [
            {
                'title': '商品1',
                'price': 100.0,
                'sales': 1000,
                'shop_name': '店铺A',
                'shop_score': 5.0,
                'shop_location': '北京',
                'product_url': 'https://example.com/1',
            },
            {
                'title': '商品2',
                'price': 200.0,
                'sales': 2000,
                'shop_name': '店铺A',
                'shop_score': 5.0,
                'shop_location': '北京',
                'product_url': 'https://example.com/2',
            },
            {
                'title': '商品3',
                'price': 300.0,
                'sales': 500,
                'shop_name': '店铺B',
                'shop_score': 4.8,
                'shop_location': '上海',
                'product_url': 'https://example.com/3',
            }
        ]
        self.analyzer = DataAnalyzer(self.test_data)

    def test_basic_stats(self):
        """测试基础统计"""
        stats = self.analyzer.get_basic_stats()
        self.assertIn('total_products', stats)
        self.assertEqual(stats['total_products'], 3)
        self.assertIn('unique_shops', stats)
        self.assertEqual(stats['unique_shops'], 2)
        print(f"基础统计: {stats}")

    def test_price_distribution(self):
        """测试价格分布"""
        dist = self.analyzer.get_price_distribution(bins=2)
        self.assertIn('min', dist)
        self.assertIn('max', dist)
        self.assertIn('distribution', dist)
        print(f"价格分布: {dist}")

    def test_top_products_by_sales(self):
        """测试 TOP 商品排行"""
        top_products = self.analyzer.get_top_products_by_sales(top_n=2)
        self.assertEqual(len(top_products), 2)
        self.assertEqual(top_products[0]['sales'], 2000)  # 销量最高
        print(f"TOP 2 商品: {top_products}")

    def test_top_shops_by_sales(self):
        """测试 TOP 店铺排行"""
        top_shops = self.analyzer.get_top_shops_by_sales(top_n=2)
        self.assertEqual(len(top_shops), 2)
        self.assertEqual(top_shops[0]['shop_name'], '店铺A')  # 销量最高
        print(f"TOP 2 店铺: {top_shops}")

    def test_shops_by_score(self):
        """测试店铺评分排行"""
        shops_by_score = self.analyzer.get_shops_by_score(top_n=2)
        self.assertEqual(len(shops_by_score), 2)
        self.assertEqual(shops_by_score[0]['shop_name'], '店铺A')  # 评分最高
        print(f"TOP 2 店铺（按评分）: {shops_by_score}")

    def test_price_distribution_chart(self):
        """测试价格分布图"""
        test_dir = os.path.join(project_root, 'tests', 'test_output')
        os.makedirs(test_dir, exist_ok=True)
        filename = os.path.join(test_dir, 'test_price_distribution.png')
        result = self.analyzer.save_price_distribution_chart(filename)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

    def test_sales_chart(self):
        """测试销量排行图"""
        test_dir = os.path.join(project_root, 'tests', 'test_output')
        os.makedirs(test_dir, exist_ok=True)
        filename = os.path.join(test_dir, 'test_sales_ranking.png')
        result = self.analyzer.save_sales_chart(filename)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

    def test_generate_report(self):
        """测试生成报告"""
        test_dir = os.path.join(project_root, 'tests', 'test_output')
        os.makedirs(test_dir, exist_ok=True)
        filename = os.path.join(test_dir, 'test_report.html')
        result = self.analyzer.generate_report(filename)
        self.assertTrue(os.path.exists(result))
        print(f"报告已生成: {result}")

    def tearDown(self):
        """测试后清理"""
        # 删除测试输出文件
        import shutil
        test_dir = os.path.join(project_root, 'tests', 'test_output')
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_full_workflow(self):
        """测试完整工作流"""
        print("\n" + "=" * 60)
        print("集成测试：完整工作流")
        print("=" * 60)

        # 1. 创建测试数据
        test_data = [
            {
                'title': f'测试商品{i}',
                'price': float(i * 100),
                'sales': i * 1000,
                'shop_name': f'店铺{i % 2 + 1}',
                'shop_score': 5.0 - i * 0.1,
                'shop_location': '北京',
                'product_url': f'https://example.com/{i}',
            }
            for i in range(1, 6)
        ]

        print(f"[OK] 1. 创建测试数据: {len(test_data)} 个商品")

        # 2. 导出数据
        exporter = DataExporter()
        test_dir = os.path.join(project_root, 'tests', 'test_output')
        os.makedirs(test_dir, exist_ok=True)

        csv_file = os.path.join(test_dir, 'integration_test.csv')
        json_file = os.path.join(test_dir, 'integration_test.json')

        self.assertTrue(exporter.export_csv(test_data, csv_file))
        self.assertTrue(exporter.export_json(test_data, json_file))
        print(f"[OK] 2. 导出数据: CSV 和 JSON")

        # 3. 数据分析
        analyzer = DataAnalyzer(test_data)
        stats = analyzer.get_basic_stats()
        print(f"[OK] 3. 数据分析: {stats['total_products']} 个商品, {stats['unique_shops']} 个店铺")

        # 4. 生成报告
        report_file = os.path.join(test_dir, 'integration_report.html')
        result = analyzer.generate_report(report_file)
        print(f"[OK] 4. 生成报告: {result}")

        print("=" * 60)
        print("[OK] 集成测试完成！")
        print("=" * 60)

    def tearDown(self):
        """测试后清理"""
        # 删除测试输出文件
        import shutil
        test_dir = os.path.join(project_root, 'tests', 'test_output')
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


def run_tests():
    """运行测试"""
    print("\n" + "=" * 60)
    print("淘宝商品爬虫测试套件")
    print("=" * 60 + "\n")

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestTaobaoScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestDataExporter))
    suite.addTests(loader.loadTestsFromTestCase(TestDataAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 打印总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 60)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
