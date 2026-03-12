# -*- coding: utf-8 -*-
"""
B站视频爬虫测试脚本
测试各种功能和边界情况
"""

import unittest
import os
import json
import pandas as pd
from bilibili_scraper import BiliBiliScraper


class TestBiliBiliScraper(unittest.TestCase):
    """B站爬虫测试类"""

    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        print("\n" + "=" * 60)
        print("开始运行测试套件")
        print("=" * 60 + "\n")

    def setUp(self):
        """每个测试用例前的初始化"""
        self.scraper = BiliBiliScraper(min_delay=1, max_delay=2)

    def tearDown(self):
        """每个测试用例后的清理"""
        self.scraper.close()

    def test_extract_bv_code(self):
        """测试BV号提取功能"""
        print("\n测试：BV号提取")

        # 测试BV号
        bv1 = self.scraper._extract_bv_code('BV1xx411c7m')
        self.assertEqual(bv1, 'BV1xx411c7m')

        # 测试完整URL
        bv2 = self.scraper._extract_bv_code('https://www.bilibili.com/video/BV1yy411d7mE')
        self.assertEqual(bv2, 'BV1yy411d7mE')

        # 测试短链接
        bv3 = self.scraper._extract_bv_code('https://b23.tv/BV1zz411e7mF')
        self.assertEqual(bv3, 'BV1zz411e7mF')

        # 测试无效输入
        bv4 = self.scraper._extract_bv_code('invalid_string')
        self.assertIsNone(bv4)

        print("BV号提取测试通过")

    def test_get_video_info_with_valid_bv(self):
        """测试使用有效BV号获取视频信息"""
        print("\n测试：获取有效视频信息")

        # 使用一个已知的视频BV号
        video_info = self.scraper.get_video_info('BV1xx411c7mD')

        self.assertIsNotNone(video_info, "视频信息不应为None")
        self.assertIn('bv', video_info)
        self.assertIn('title', video_info)
        self.assertIn('author', video_info)
        self.assertIn('views', video_info)

        print(f"[OK] 成功获取视频: {video_info.get('title')}")

    def test_get_video_info_with_url(self):
        """测试使用URL获取视频信息"""
        print("\n测试：使用URL获取视频信息")

        url = 'https://www.bilibili.com/video/BV1xx411c7mD'
        video_info = self.scraper.get_video_info(url)

        self.assertIsNotNone(video_info, "视频信息不应为None")
        self.assertEqual(video_info.get('bv'), 'BV1xx411c7mD')

        print("[OK] URL解析测试通过")

    def test_get_video_info_invalid_input(self):
        """测试无效输入"""
        print("\n测试：无效输入处理")

        # 无效BV号
        info1 = self.scraper.get_video_info('invalid_bv')
        self.assertIsNone(info1)

        # 空字符串
        info2 = self.scraper.get_video_info('')
        self.assertIsNone(info2)

        print("[OK] 无效输入处理测试通过")

    def test_batch_get_videos(self):
        """测试批量获取视频"""
        print("\n测试：批量获取视频")

        video_list = ['BV1xx411c7mD', 'BV1y41197p7']
        results = self.scraper.batch_get_videos(video_list)

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        for video in results:
            self.assertIn('bv', video)
            self.assertIn('title', video)

        print(f"[OK] 批量获取测试通过，获取 {len(results)} 个视频")

    def test_batch_get_videos_with_invalid(self):
        """测试包含无效视频的批量获取"""
        print("\n测试：包含无效视频的批量获取")

        video_list = [
            'BV1xx411c7mD',  # 有效
            'invalid_bv',    # 无效
            'BV1y41197p7',   # 有效
        ]

        results = self.scraper.batch_get_videos(video_list)

        # 应该至少获取部分有效视频
        self.assertGreater(len(results), 0)
        self.assertLessEqual(len(results), 2)

        print(f"[OK] 混合输入测试通过，成功获取 {len(results)} 个视频")

    def test_search_videos(self):
        """测试视频搜索"""
        print("\n测试：视频搜索")

        # 搜索一个常见关键词
        results = self.scraper.search_videos('Python', max_results=3)

        self.assertIsInstance(results, list)
        # 搜索结果可能为空（取决于网络和网站状态）
        print(f"[OK] 搜索测试完成，找到 {len(results)} 个视频")

    def test_export_to_csv(self):
        """测试CSV导出功能"""
        print("\n测试：CSV导出")

        # 创建测试数据
        test_data = [
            {
                'bv': 'BV1xx411c7mD',
                'title': '测试视频1',
                'author': '测试作者1',
                'views': 1000000,
                'likes': 50000,
                'coins': 20000,
                'favorites': 10000,
                'shares': 5000,
                'url': 'https://www.bilibili.com/video/BV1xx411c7mD'
            },
            {
                'bv': 'BV1yy411d7mE',
                'title': '测试视频2',
                'author': '测试作者2',
                'views': 500000,
                'likes': 25000,
                'coins': 10000,
                'favorites': 5000,
                'shares': 2500,
                'url': 'https://www.bilibili.com/video/BV1yy411d7mE'
            }
        ]

        # 导出到CSV
        test_file = 'test_output.csv'
        self.scraper.export_to_csv(test_data, test_file)

        # 验证文件存在
        self.assertTrue(os.path.exists(test_file))

        # 验证文件内容
        df = pd.read_csv(test_file, encoding='utf-8-sig')
        self.assertEqual(len(df), 2)
        self.assertIn('title', df.columns)
        self.assertIn('views', df.columns)

        # 清理测试文件
        os.remove(test_file)

        print("[OK] CSV导出测试通过")

    def test_export_empty_data(self):
        """测试导出空数据"""
        print("\n测试：导出空数据")

        # 不应该抛出异常
        self.scraper.export_to_csv([], 'empty_test.csv')

        # 文件不应该存在
        self.assertFalse(os.path.exists('empty_test.csv'))

        print("[OK] 空数据处理测试通过")

    def test_generate_report(self):
        """测试报告生成功能"""
        print("\n测试：生成分析报告")

        # 创建测试数据
        test_data = [
            {
                'bv': 'BV1xx411c7mD',
                'title': '测试视频1',
                'author': '测试作者1',
                'author_id': '123456',
                'views': 1000000,
                'likes': 50000,
                'coins': 20000,
                'favorites': 10000,
                'shares': 5000,
                'duration': '10:00',
                'publish_time': '2024-01-01',
                'url': 'https://www.bilibili.com/video/BV1xx411c7mD'
            },
            {
                'bv': 'BV1yy411d7mE',
                'title': '测试视频2',
                'author': '测试作者2',
                'author_id': '234567',
                'views': 500000,
                'likes': 25000,
                'coins': 10000,
                'favorites': 5000,
                'shares': 2500,
                'duration': '05:00',
                'publish_time': '2024-01-02',
                'url': 'https://www.bilibili.com/video/BV1yy411d7mE'
            }
        ]

        # 生成报告
        report_file = 'test_report.html'
        self.scraper.generate_report(test_data, report_file)

        # 验证文件存在
        self.assertTrue(os.path.exists(report_file))

        # 验证文件内容
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('B站视频数据分析报告', content)
            self.assertIn('总体统计', content)
            self.assertIn('作者排行榜', content)
            self.assertIn('播放量分布', content)

        # 清理测试文件
        os.remove(report_file)

        print("[OK] 报告生成测试通过")

    def test_generate_report_empty_data(self):
        """测试生成空数据报告"""
        print("\n测试：生成空数据报告")

        # 不应该抛出异常
        self.scraper.generate_report([], 'empty_report.html')

        # 文件不应该存在
        self.assertFalse(os.path.exists('empty_report.html'))

        print("[OK] 空数据报告测试报告")

    def test_user_agent_rotation(self):
        """测试User-Agent轮换"""
        print("\n测试：User-Agent轮换")

        user_agents = set()
        for _ in range(10):
            ua = self.scraper._get_random_user_agent()
            user_agents.add(ua)

        # 应该有多个不同的User-Agent
        self.assertGreater(len(user_agents), 1)
        print(f"[OK] User-Agent轮换{len(user_agents)} 个不同的UA")

    def test_random_delay(self):
        """测试随机延时"""
        print("\n测试：随机延时")

        import time

        # 测试延时在合理范围内
        start = time.time()
        self.scraper._random_delay()
        elapsed = time.time() - start

        self.assertGreaterEqual(elapsed, self.scraper.min_delay)
        self.assertLessEqual(elapsed, self.scraper.max_delay + 1)  # +1秒容差

        print(f"[OK] 随机延时测试通过，延时 {elapsed:.2f} 秒")

    def test_video_info_structure(self):
        """测试视频信息结构完整性"""
        print("\n测试：视频信息结构完整性")

        video_info = self.scraper.get_video_info('BV1xx411c7mD')

        if video_info:
            # 检查所有必需字段
            required_fields = [
                'bv', 'title', 'author', 'views',
                'likes', 'coins', 'favorites', 'shares', 'url'
            ]

            for field in required_fields:
                self.assertIn(field, video_info, f"缺少字段: {field}")

            # 检查数据类型
            self.assertIsInstance(video_info['views'], (int, type(None)))
            self.assertIsInstance(video_info['likes'], (int, type(None)))

            print("[OK] 视频信息结构完整性测试通过")
        else:
            print("[WARN] 跳过结构测试（无法获取视频信息）")


def run_all_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestBiliBiliScraper)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # 打印测试总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 60)

    return result.wasSuccessful()


if __name__ == '__main__':
    import sys

    success = run_all_tests()
    sys.exit(0 if success else 1)
