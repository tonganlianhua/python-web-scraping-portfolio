"""
豆瓣豆瓣电影爬虫测试脚本
测试各个功能模块
"""

import unittest
import os
import json
import csv
from scraper import DoubanMovieScraper
from utils import AntiSpider, DataExporter, DataAnalyzer


class TestAntiSpider(unittest.TestCase):
    """测试反爬策略"""

    def test_get_random_user_agent(self):
        """测试获取随机 User-Agent"""
        ua = AntiSpider.get_random_user_agent()
        self.assertIsInstance(ua, str)
        self.assertTrue(len(ua) > 0)
        self.assertIn('Mozilla', ua)

    def test_get_headers(self):
        """测试获取请求头"""
        headers = AntiSpider.get_headers()
        self.assertIsInstance(headers, dict)
        self.assertIn('User-Agent', headers)
        self.assertIn('Accept', headers)
        self.assertIn('Referer', headers)

    def test_random_delay(self):
        """测试随机延时"""
        import time
        start = time.time()
        delay = AntiSpider.random_delay(0.1, 0.2)
        elapsed = time.time() - start
        self.assertGreaterEqual(elapsed, 0.1)
        self.assertLessEqual(elapsed, 0.2)


class TestDataExporter(unittest.TestCase):
    """测试数据导出"""

    def setUp(self):
        """设置测试数据"""
        self.test_data = [
            {'title': '电影1', 'rating': 9.0, 'year': 1994},
            {'title': '电影2', 'rating': 8.5, 'year': 1997},
            {'title': '电影3', 'rating': 9.2, 'year': 2000},
        ]
        self.output_dir = 'test_output'
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        """清理测试文件"""
        import shutil
        if (os.path.exists(self.output_dir)):
            shutil.rmtree(self.output_dir)

    def test_to_csv(self):
        """测试导出 CSV"""
        csv_file = f'{self.output_dir}/test.csv'
        result = DataExporter.to_csv(self.test_data, csv_file)

        self.assertTrue(os.path.exists(csv_file))
        self.assertEqual(result, csv_file)

        # 验证内容
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 3)

    def test_to_json(self):
        """测试导出 JSON"""
        json_file = f'{self.output_dir}/test.json'
        result = DataExporter.to_json(self.test_data, json_file)

        self.assertTrue(os.path.exists(json_file))
        self.assertEqual(result, json_file)

        # 验证内容
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data), 3)
            self.assertEqual(data[0]['title'], '电影1')


class TestDoubanMovieScraper(unittest.TestCase):
    """测试豆瓣电影爬虫"""

    def setUp(self):
        """设置爬虫实例"""
        self.scraper = DoubanMovieScraper()

    def tearDown(self):
        """关闭爬虫"""
        self.scraper.close()

    def test_get_top250(self):
        """测试爬取 Top250"""
        print("\n[测试] 爬取豆瓣电影 Top250...")
        movies = self.scraper.get_top250()

        self.assertIsInstance(movies, list)
        self.assertEqual(len(movies), 250)

        # 验证第一个电影的数据结构
        first_movie = movies[0]
        self.assertIn('rank', first_movie)
        self.assertIn('title', first_movie)
        self.assertIn('rating', first_movie)
        self.assertIn('year', first_movie)
        self.assertIn('directors', first_movie)
        self.assertIn('actors', first_movie)

        print(f"✓ 成功爬取 {len(movies)} 部电影")
        print(f"✓ 第一名: {first_movie['title']} - {first_movie['rating']}")

    def test_search_movies(self):
        """测试搜索电影"""
        print("\n[测试] 搜索电影...")
        results = self.scraper.search_movies('肖申克的救赎', limit=5)

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        # 验证搜索结果
        first_result = results[0]
        self.assertIn('title', first_result)
        self.assertIn('rating', first_result)

        print(f"✓ 找到 {len(results)} 部电影")
        print(f"✓ 第一部: {first_result['title']}")

    def test_get_movie_detail(self):
        """测试获取电影详情"""
        print("\n[测试] 获取电影详情...")
        # 肖申克的救赎的 ID
        detail = self.scraper.get_movie_detail('1292052')

        self.assertIsNotNone(detail)
        self.assertIn('title', detail)
        self.assertIn('rating', detail)
        self.assertIn('directors', detail)
        self.assertIn('actors', detail)
        self.assertIn('genres', detail)
        self.assertIn('summary', detail)

        print(f"✓ 电影: {detail['title']}")
        print(f"✓ 评分: {detail['rating']}")
        print(f"✓ 导演: {', '.join(detail['directors'])}")

    def test_get_comments(self):
        """测试获取评论"""
        print("\n[测试] 获取电影评论...")
        comments = self.scraper.get_comments('1292052', limit=10)

        self.assertIsInstance(comments, list)
        self.assertGreater(len(comments), 0)

        # 验证评论数据
        first_comment = comments[0]
        self.assertIn('user', first_comment)
        self.assertIn('content', first_comment)
        self.assertIn('rating', first_comment)

        print(f"✓ 获取到 {len(comments)} 条评论")
        print(f"✓ 第一条评论: {first_comment['content'][:30]}...")


class TestDataAnalyzer(unittest.TestCase):
    """测试数据分析"""

    def setUp(self):
        """设置测试数据"""
        self.test_movies = [
            {'title': '电影1', 'rating': 9.0, 'year': 1994, 'directors': ['导演A']},
            {'title': '电影2', 'rating': 8.5, 'year': 1997, 'directors': ['导演A']},
            {'title': '电影3', 'rating': 9.2, 'year': 2000, 'directors': ['导演B']},
            {'title': '电影4', 'rating': 8.8, 'year': 1994, 'directors': ['导演B']},
            {'title': '电影5', 'rating': 7.5, 'year': 2010, 'directors': ['导演C']},
        ]
        self.output_dir = 'test_output'
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        """清理测试文件"""
        import shutil
        if (os.path.exists(self.output_dir)):
            shutil.rmtree(self.output_dir)

    def test_analyze_rating_distribution(self):
        """测试评分分布分析"""
        analysis = DataAnalyzer.analyze_rating_distribution(self.test_movies)

        self.assertIn('stats', analysis)
        self.assertIn('distribution', analysis)
        self.assertAlmostEqual(analysis['stats']['mean'], 8.6, places=1)

        print(f"✓ 平均评分: {analysis['stats']['mean']:.2f}")

    def test_analyze_year_distribution(self):
        """测试年份分布分析"""
        analysis = DataAnalyzer.analyze_year_distribution(self.test_movies)

        self.assertIn('stats', analysis)
        self.assertIn('by_decade', analysis)
        self.assertEqual(analysis['stats']['earliest'], 1994)
        self.assertEqual(analysis['stats']['latest'], 2010)

        print(f"✓ 年份范围: {analysis['stats']['earliest']} - {analysis['stats']['latest']}")

    def test_analyze_director_ranking(self):
        """测试导演排行分析"""
        ranking = DataAnalyzer.analyze_director_ranking(self.test_movies, top_n=3)

        self.assertIsInstance(ranking, list)
        self.assertLessEqual(len(ranking), 3)

        if ranking:
            self.assertIn('director', ranking[0])
            self.assertIn('count', ranking[0])
            self.assertIn('avg_rating', ranking[0])

            print(f"✓ 第一名导演: {ranking[0]['director']} ({ranking[0]['count']} 部作品)")

    def test_generate_report(self):
        """测试生成分析报告"""
        report_files = DataAnalyzer.generate_report(self.test_movies, self.output_dir)

        self.assertIn('report', report_files)
        self.assertTrue(os.path.exists(report_files['report']))

        # 验证报告内容
        with open(report_files['report'], 'r', encoding='utf-8') as f:
            report = json.load(f)
            self.assertIn('summary', report)
            self.assertIn('rating_analysis', report)
            self.assertIn('year_analysis', report)
            self.assertIn('director_ranking', report)

        print(f"✓ 分析报告已生成: {report_files['report']}")


def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("豆瓣电影爬虫 - 测试套件")
    print("=" * 60)

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试用例
    suite.addTests(loader.loadTestsFromTestCase(TestAntiSpider))
    suite.addTests(loader.loadTestsFromTestCase(TestDataExporter))
    suite.addTests(loader.loadTestsFromTestCase(TestDoubanMovieScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestDataAnalyzer))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 输出摘要
    print("\n" + "=" * 60)
    print("测试摘要")
    print("=" * 60)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 60)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
