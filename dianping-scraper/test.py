#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
大众点评爬虫测试脚本

使用方法:
    python test.py
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from scraper import DianpingScraper
from exporter import DataExporter


class TestDianpingScraper(unittest.TestCase):
    """测试DianpingScraper类"""

    def setUp(self):
        """测试前准备"""
        self.scraper = DianpingScraper()

    def test_init(self):
        """测试初始化"""
        scraper = DianpingScraper(city="北京", keyword="美食", min_rating=4.0)
        self.assertEqual(scraper.city, "北京")
        self.assertEqual(scraper.keyword, "美食")
        self.assertEqual(scraper.min_rating, 4.0)

    def test_user_agents(self):
        """测试User-Agent列表"""
        self.assertGreater(len(DianpingScraper.USER_AGENTS), 0)
        for ua in DianpingScraper.USER_AGENTS:
            self.assertIn('Mozilla', ua)

    def test_random_user_agent(self):
        """测试随机User-Agent获取"""
        ua1 = self.scraper._get_random_user_agent()
        ua2 = self.scraper._get_random_user_agent()
        self.assertIn(ua1, DianpingScraper.USER_AGENTS)
        self.assertIn(ua2, DianpingScraper.USER_AGENTS)

    def test_merchant_list_initialization(self):
        """测试商家列表初始化"""
        self.assertIsInstance(self.scraper.merchants, list)
        self.assertEqual(len(self.scraper.merchants), 0)

    def test_reviews_list_initialization(self):
        """测试评论列表初始化"""
        self.assertIsInstance(self.scraper.reviews, list)
        self.assertEqual(len(self.scraper.reviews), 0)

    def test_generate_empty_report(self):
        """测试空数据报告生成"""
        report = self.scraper.generate_report()
        self.assertIn("没有商家数据可分析", report)

    def test_headers_initialization(self):
        """测试请求头初始化"""
        self.assertIn('User-Agent', self.scraper.headers)
        self.assertIn('Accept', self.scraper.headers)
        self.assertIn('Accept-Language', self.scraper.headers)

    def test_random_delay(self):
        """测试随机延时"""
        import time
        start = time.time()
        self.scraper._random_delay(0.1, 0.2)
        end = time.time()
        self.assertGreater(end - start, 0.1)
        self.assertLess(end - start, 0.3)


class TestDataExporter(unittest.TestCase):
    """测试DataExporter类"""

    def setUp(self):
        """测试前准备"""
        self.exporter = DataExporter()
        self.test_data = [
            {
                'name': '测试餐厅1',
                'rating': 4.5,
                'avg_price': 100,
                'review_count': 500,
                'city': '北京',
                'keyword': '美食'
            },
            {
                'name': '测试餐厅2',
                'rating': 3.8,
                'avg_price': 200,
                'review_count': 300,
                'city': '北京',
                'keyword': '美食'
            },
            {
                'name': '测试餐厅3',
                'rating': 4.8,
                'avg_price': 150,
                'review_count': 800,
                'city': '北京',
                'keyword': '美食'
            }
        ]

    def tearDown(self):
        """测试后清理"""
        # 删除测试生成的文件
        test_files = [
            'test_export.csv',
            'test_export.json',
            'test_report.txt',
            'test_rating_dist.png',
            'test_price_dist.png'
        ]
        for filename in test_files:
            filepath = os.path.join(self.exporter.data_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)

    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.exporter.data_dir)
        self.assertTrue(os.path.exists(self.exporter.data_dir))

    def test_export_csv(self):
        """测试CSV导出"""
        result = self.exporter.export_csv(self.test_data, 'test_export.csv')
        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(result))

        # 验证文件内容
        with open(result, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            self.assertIn('name', content)
            self.assertIn('rating', content)
            self.assertIn('测试餐厅1', content)

    def test_export_json(self):
        """测试JSON导出"""
        result = self.exporter.export_json(self.test_data, 'test_export.json')
        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(result))

        # 验证文件内容
        import json
        with open(result, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data), 3)
            self.assertEqual(data[0]['name'], '测试餐厅1')

    def test_generate_text_report(self):
        """测试文本报告生成"""
        report = self.exporter.generate_text_report(self.test_data)

        self.assertIn('数据分析报告', report)
        self.assertIn('商家总数', report)
        self.assertIn('评分分析', report)
        self.assertIn('人均消费分析', report)
        self.assertIn('北京', report)
        self.assertIn('TOP', report)

    def test_save_report(self):
        """测试报告保存"""
        test_report = "这是测试报告内容"
        result = self.exporter.save_report(test_report, 'test_report.txt')
        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(result))

        # 验证文件内容
        with open(result, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, test_report)

    def test_export_empty_data(self):
        """测试空数据导出"""
        result = self.exporter.export_csv([], 'empty.csv')
        self.assertIsNone(result)

        result = self.exporter.export_json([], 'empty.json')
        self.assertIsNone(result)

    def test_plot_rating_distribution(self):
        """测试评分分布图绘制"""
        result = self.exporter.plot_rating_distribution(self.test_data, 'test_rating_dist.png')
        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(result))

    def test_plot_price_distribution(self):
        """测试人均消费分布图绘制"""
        result = self.exporter.plot_price_distribution(self.test_data, 'test_price_dist.png')
        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(result))

    def test_plot_empty_data(self):
        """测试空数据绘图"""
        result = self.exporter.plot_rating_distribution([], 'empty.png')
        self.assertIsNone(result)

        result = self.exporter.plot_price_distribution([], 'empty.png')
        self.assertIsNone(result)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_full_workflow(self):
        """测试完整工作流程"""
        # 创建爬虫
        scraper = DianpingScraper(city="测试城市", keyword="测试关键词")

        # 添加模拟数据
        scraper.merchants = [
            {
                'name': '测试商家1',
                'rating': 4.5,
                'avg_price': 100,
                'review_count': 500,
                'city': '测试城市',
                'keyword': '测试关键词',
                'address': '测试地址1',
                'business_hours': '10:00-22:00'
            },
            {
                'name': '测试商家2',
                'rating': 3.5,
                'avg_price': 150,
                'review_count': 200,
                'city': '测试城市',
                'keyword': '测试关键词',
                'address': '测试地址2',
                'business_hours': '09:00-21:00'
            }
        ]

        # 生成报告
        report = scraper.generate_report()
        self.assertIn('测试城市', report)
        self.assertIn('测试商家1', report)
        self.assertIn('测试商家2', report)

        # 导出数据
        scraper.export_to_csv('integration_test.csv', data_type='merchants')
        scraper.export_to_json('integration_test.json', data_type='merchants')

        # 使用导出器
        exporter = DataExporter()

        # 生成高级报告
        advanced_report = exporter.generate_text_report(scraper.merchants)
        self.assertIn('测试城市', advanced_report)
        self.assertIn('评分分析', advanced_report)

        # 清理测试文件
        test_files = ['integration_test.csv', 'integration_test.json']
        for filename in test_files:
            filepath = os.path.join(exporter.data_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)


def run_tests():
    """运行所有测试"""
    print("\n" + "="*70)
    print("大众点评爬虫测试套件".center(70))
    print("="*70)

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestDianpingScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestDataExporter))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 输出总结
    print("\n" + "="*70)
    print("测试总结".center(70))
    print("="*70)
    print(f"总计: {result.testsRun} 个测试")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)} 个")
    print(f"失败: {len(result.failures)} 个")
    print(f"错误: {len(result.errors)} 个")

    if result.wasSuccessful():
        print("\n所有测试通过！")
        return 0
    else:
        print("\n存在失败的测试")
        return 1


if __name__ == '__main__':
    sys.exit(run_tests())
