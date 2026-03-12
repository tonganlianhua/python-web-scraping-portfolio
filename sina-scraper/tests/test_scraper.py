"""
单元测试：爬虫基础功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from src.scraper import WeiboScraper
from src.user import WeiboUser
from src.weibo import WeiboPost
from src.exporter import DataExporter
from src.analyzer import DataAnalyzer
import tempfile
import shutil


class TestWeiboScraper(unittest.TestCase):
    """测试WeiboScraper类"""

    def setUp(self):
        """测试前准备"""
        self.scraper = WeiboScraper()

    def tearDown(self):
        """测试后清理"""
        self.scraper.close()

    def test_scraper_initialization(self):
        """测试爬虫初始化"""
        self.assertIsNotNone(self.scraper.session)
        self.assertIsNotNone(self.scraper.ua)

    def test_random_delay(self):
        """测试随机延时"""
        import time
        start = time.time()
        self.scraper._random_delay()
        elapsed = time.time() - start
        # 延时应该在2-5秒之间
        self.assertGreaterEqual(elapsed, 2.0)
        self.assertLessEqual(elapsed, 5.0)


class TestWeiboUser(unittest.TestCase):
    """测试WeiboUser类"""

    def test_user_initialization(self):
        """测试用户初始化"""
        user = WeiboUser(
            user_id='123',
            username='test_user',
            fans_count=1000
        )
        self.assertEqual(user.user_id, '123')
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.fans_count, 1000)

    def test_user_to_dict(self):
        """测试用户转字典"""
        user = WeiboUser(
            user_id='123',
            username='test_user',
            fans_count=1000
        )
        data = user.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['user_id'], '123')
        self.assertEqual(data['username'], 'test_user')

    def test_user_from_dict(self):
        """测试从字典创建用户"""
        data = {
            'user_id': '123',
            'username': 'test_user',
            'fans_count': 1000
        }
        user = WeiboUser.from_dict(data)
        self.assertEqual(user.user_id, '123')
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.fans_count, 1000)


class TestWeiboPost(unittest.TestCase):
    """测试WeiboPost类"""

    def test_post_initialization(self):
        """测试帖子初始化"""
        post = WeiboPost(
            post_id='456',
            user_id='123',
            content='test content',
            likes=100
        )
        self.assertEqual(post.post_id, '456')
        self.assertEqual(post.user_id, '123')
        self.assertEqual(post.content, 'test content')
        self.assertEqual(post.likes, 100)

    def test_post_to_dict(self):
        """测试帖子转字典"""
        post = WeiboPost(
            post_id='456',
            content='test content',
            likes=100
        )
        data = post.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['post_id'], '456')
        self.assertEqual(data['content'], 'test content')

    def test_post_from_dict(self):
        """测试从字典创建帖子"""
        data = {
            'post_id': '456',
            'content': 'test content',
            'likes': 100
        }
        post = WeiboPost.from_dict(data)
        self.assertEqual(post.post_id, '456')
        self.assertEqual(post.content, 'test content')
        self.assertEqual(post.likes, 100)


class TestDataExporter(unittest.TestCase):
    """测试DataExporter类"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.exporter = DataExporter(self.temp_dir)
        self.users = [
            WeiboUser(user_id='1', username='user1', fans_count=100),
            WeiboUser(user_id='2', username='user2', fans_count=200),
        ]
        self.posts = [
            WeiboPost(post_id='1', content='post1', likes=10),
            WeiboPost(post_id='2', content='post2', likes=20),
        ]

    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.temp_dir)

    def test_export_users_json(self):
        """测试导出用户到JSON"""
        filepath = self.exporter.export_users(self.users, 'test_users', 'json')
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.json'))

    def test_export_users_csv(self):
        """测试导出用户到CSV"""
        filepath = self.exporter.export_users(self.users, 'test_users', 'csv')
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.csv'))

    def test_export_posts_json(self):
        """测试导出帖子到JSON"""
        filepath = self.exporter.export_posts(self.posts, 'test_posts', 'json')
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.json'))

    def test_export_posts_csv(self):
        """测试导出帖子到CSV"""
        filepath = self.exporter.export_posts(self.posts, 'test_posts', 'csv')
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.csv'))


class TestDataAnalyzer(unittest.TestCase):
    """测试DataAnalyzer类"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.analyzer = DataAnalyzer(self.temp_dir)
        self.users = [
            WeiboUser(user_id='1', username='user1', fans_count=100, weibo_count=10, verified=True),
            WeiboUser(user_id='2', username='user2', fans_count=200, weibo_count=20, verified=False),
            WeiboUser(user_id='3', username='user3', fans_count=300, weibo_count=30, verified=True),
        ]
        self.posts = [
            WeiboPost(post_id='1', content='test #topic1', likes=10, comments=1, reposts=0, topics=['topic1']),
            WeiboPost(post_id='2', content='test #topic2', likes=20, comments=2, reposts=1, topics=['topic2']),
            WeiboPost(post_id='3', content='test #topic1', likes=30, comments=3, reposts=2, topics=['topic1']),
        ]

    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.temp_dir)

    def test_analyze_users(self):
        """测试用户分析"""
        result = self.analyzer.analyze_users(self.users)
        self.assertIn('total_users', result)
        self.assertEqual(result['total_users'], 3)
        self.assertIn('verified_users', result)
        self.assertEqual(result['verified_users'], 2)

    def test_analyze_posts(self):
        """测试帖子分析"""
        result = self.analyzer.analyze_posts(self.posts)
        self.assertIn('total_posts', result)
        self.assertEqual(result['total_posts'], 3)
        self.assertIn('likes_total', result)
        self.assertEqual(result['likes_total'], 60)
        self.assertIn('total_topics', result)
        self.assertEqual(result['total_topics'], 2)

    def test_generate_report(self):
        """测试生成报告"""
        filepath = self.analyzer.generate_report(self.users, self.posts, 'test_report')
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.txt'))


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestWeiboScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestWeiboUser))
    suite.addTests(loader.loadTestsFromTestCase(TestWeiboPost))
    suite.addTests(loader.loadTestsFromTestCase(TestDataExporter))
    suite.addTests(loader.loadTestsFromTestCase(TestDataAnalyzer))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    print("="*80)
    print("运行新浪微博爬虫单元测试")
    print("="*80)
    success = run_tests()
    if success:
        print("\n" + "="*80)
        print("所有测试通过！")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("部分测试失败，请检查输出")
        print("="*80)
