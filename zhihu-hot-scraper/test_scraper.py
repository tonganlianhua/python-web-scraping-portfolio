"""
知乎热榜爬虫测试脚本
测试所有核心功能
"""

import unittest
from zhihu_scraper import ZhihuHotScraper
from data_exporter import DataExporter
import os
import shutil


class TestZhihuScraper(unittest.TestCase):
    """测试知乎爬虫核心功能"""

    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        cls.scraper = ZhihuHotScraper()
        cls.exporter = DataExporter(output_dir="test_output")

    def setUp(self):
        """每个测试前的准备工作"""
        # 创建测试输出目录
        os.makedirs("test_output", exist_ok=True)

    def tearDown(self):
        """每个测试后的清理工作"""
        # 可以在这里清理测试文件
        pass

    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        # 删除测试输出目录
        if os.path.exists("test_output"):
            shutil.rmtree("test_output")

    def test_init(self):
        """测试爬虫初始化"""
        self.assertIsNotNone(self.scraper)
        self.assertEqual(self.scraper.base_url, "https://www.zhihu.com")
        self.assertTrue(len(self.scraper.user_agents) > 0)

    def test_get_random_user_agent(self):
        """测试随机User-Agent"""
        ua = self.scraper._get_random_user_agent()
        self.assertIsNotNone(ua)
        self.assertTrue(len(ua) > 0)
        self.assertIn("Mozilla", ua)

    def test_get_hot_list(self):
        """测试获取热榜列表"""
        hot_list = self.scraper.get_hot_list()
        
        # 验证返回类型
        self.assertIsInstance(hot_list, list)
        
        # 验证数据结构
        if len(hot_list) > 0:
            item = hot_list[0]
            self.assertIn('rank', item)
            self.assertIn('title', item)
            self.assertIn('hot_value', item)
            self.assertIn('link', item)
            self.assertIn('excerpt', item)
            self.assertIn('created_time', item)
            
            # 验证数据类型
            self.assertIsInstance(item['rank'], int)
            self.assertIsInstance(item['title'], str)
            self.assertIsInstance(item['hot_value'], (int, float))
            self.assertIsInstance(item['link'], str)
            self.assertIsInstance(item['excerpt'], str)
            self.assertIsInstance(item['created_time'], str)

    def test_keyword_filter(self):
        """测试关键词过滤"""
        # 先获取所有热榜
        all_hot_list = self.scraper.get_hot_list()
        
        # 使用关键词过滤
        keyword = "科技"
        filtered_list = self.scraper.get_hot_list(keyword=keyword)
        
        # 验证过滤结果
        self.assertIsInstance(filtered_list, list)
        
        # 验证所有结果都包含关键词
        for item in filtered_list:
            self.assertIn(keyword.lower(), item['title'].lower())

    def test_get_topic_detail(self):
        """测试获取话题详情"""
        # 先获取热榜
        hot_list = self.scraper.get_hot_list()
        
        if len(hot_list) > 0:
            # 获取第一个话题的详情
            topic_url = hot_list[0]['link']
            detail = self.scraper.get_topic_detail(topic_url)
            
            # 验证返回数据结构
            self.assertIn('url', detail)
            self.assertIn('answer_count', detail)
            self.assertIn('follower_count', detail)
            self.assertIn('view_count', detail)
            self.assertIn('tags', detail)
            
            # 验证数据类型
            self.assertEqual(detail['url'], topic_url)
            self.assertIsInstance(detail['answer_count'], int)
            self.assertIsInstance(detail['follower_count'], int)
            self.assertIsInstance(detail['view_count'], int)
            self.assertIsInstance(detail['tags'], list)

    def test_compare_hot_values(self):
        """测试热度对比"""
        # 获取两次热榜数据
        hot_list_1 = self.scraper.get_hot_list()
        import time
        time.sleep(5)
        hot_list_2 = self.scraper.get_hot_list()
        
        # 对比热度变化
        comparison = self.scraper.compare_hot_values(hot_list_1, hot_list_2)
        
        # 验证对比结果
        self.assertIsInstance(comparison, list)
        
        if len(comparison) > 0:
            item = comparison[0]
            self.assertIn('title', item)
            self.assertIn('hot_value_1', item)
            self.assertIn('hot_value_2', item)
            self.assertIn('change', item)
            self.assertIn('change_percent', item)
            self.assertIn('link', item)
            
            # 验证变化值计算正确
            expected_change = item['hot_value_2'] - item['hot_value_1']
            self.assertEqual(item['change'], expected_change)

    def test_random_delay(self):
        """测试随机延时"""
        import time
        
        start = time.time()
        self.scraper._random_delay(0.1, 0.2)
        end = time.time()
        
        # 验证延时在合理范围内
        delay = end - start
        self.assertGreaterEqual(delay, 0.1)
        self.assertLessEqual(delay, 0.3)


class TestDataExporter(unittest.TestCase):
    """测试数据导出功能"""

    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        cls.exporter = DataExporter(output_dir="test_output")

    def setUp(self):
        """每个测试前的准备工作"""
        os.makedirs("test_output", exist_ok=True)

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        if os.path.exists("test_output"):
            shutil.rmtree("test_output")

    def test_init(self):
        """测试导出器初始化"""
        self.assertEqual(self.exporter.output_dir, "test_output")
        self.assertTrue(os.path.exists("test_output"))

    def test_export_to_excel(self):
        """测试导出Excel"""
        # 创建测试数据
        hot_list = [
            {
                'rank': 1,
                'title': '测试标题',
                'hot_value': 1000000,
                'link': 'https://www.zhihu.com/question/1',
                'excerpt': '测试摘要',
                'created_time': '2026-03-12 10:00:00'
            }
        ]
        
        # 导出Excel
        filepath = self.exporter.export_to_excel(hot_list, filename="test_hot")
        
        # 验证文件存在
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.xlsx'))

    def test_export_comparison_to_excel(self):
        """测试导出对比数据到Excel"""
        # 创建测试数据
        comparison = [
            {
                'title': '测试话题',
                'hot_value_1': 1000000,
                'hot_value_2': 1100000,
                'change': 100000,
                'change_percent': 10.0,
                'link': 'https://www.zhihu.com/question/1'
            }
        ]
        
        # 导出Excel
        filepath = self.exporter.export_comparison_to_excel(comparison, filename="test_comparison")
        
        # 验证文件存在
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.xlsx'))

    def test_export_detail_to_excel(self):
        """测试导出详情到Excel"""
        # 创建测试数据
        details = [
            {
                'url': 'https://www.zhihu.com/question/1',
                'answer_count': 100,
                'follower_count': 1000,
                'view_count': 100000,
                'tags': ['测试', '标签']
            }
        ]
        
        # 导出Excel
        filepath = self.exporter.export_detail_to_excel(details, filename="test_detail")
        
        # 验证文件存在
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.xlsx'))

    def test_generate_comparison_chart(self):
        """测试生成对比图"""
        # 创建测试数据
        comparison = [
            {
                'title': f'测试话题{i}',
                'hot_value_1': 1000000 + i * 100000,
                'hot_value_2': 1100000 + i * 100000,
                'change': 100000,
                'change_percent': 10.0,
                'link': f'https://www.zhihu.com/question/{i}'
            }
            for i in range(5)
        ]
        
        # 生成图表
        filepath = self.exporter.generate_comparison_chart(comparison, filename="test_chart")
        
        # 验证文件存在
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.png'))

    def test_generate_trend_chart(self):
        """测试生成趋势图"""
        # 创建测试数据
        hot_history = [
            [
                {
                    'rank': i + 1,
                    'title': f'测试话题{i}',
                    'hot_value': 1000000 + i * 100000 + j * 50000,
                    'link': f'https://www.zhihu.com/question/{i}',
                    'excerpt': '测试摘要',
                    'created_time': '2026-03-12 10:00:00'
                }
                for i in range(5)
            ]
            for j in range(3)
        ]
        
        # 生成图表
        filepath = self.exporter.generate_trend_chart(hot_history, filename="test_trend")
        
        # 验证文件存在
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.png'))


def run_tests():
    """运行所有测试"""
    print("=" * 80)
    print("知乎热榜爬虫测试套件")
    print("=" * 80)
    print()
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestZhihuScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestDataExporter))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试结果摘要
    print()
    print("=" * 80)
    print("测试结果摘要")
    print("=" * 80)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
