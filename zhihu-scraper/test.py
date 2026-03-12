# -*- coding: utf-8 -*-
"""
知乎爬虫测试脚本
测试各个模块的功能
"""

import unittest
import sys
import os
import io
from pathlib import Path

# 设置输出编码为UTF-8（针对Windows）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加项目目录到路径
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from zhihu_scraper import ZhihuScraper, TOPIC_IDS
from data_exporter import DataExporter
from analyzer import DataAnalyzer


class TestZhihuScraper(unittest.TestCase):
    """测试爬虫核心功能"""

    def setUp(self):
        """测试前准备"""
        self.scraper = ZhihuScraper()

    def tearDown(self):
        """测试后清理"""
        self.scraper.close()

    def test_search_questions(self):
        """测试搜索问题功能"""
        print("\n📝 测试搜索问题...")
        questions = self.scraper.search_questions("Python", limit=3)

        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
        self.assertIn('question_id', questions[0])
        self.assertIn('title', questions[0])

        print(f"✓ 搜索功能正常，找到 {len(questions)} 个问题")

    def test_get_question_detail(self):
        """测试获取问题详情"""
        print("\n📝 测试获取问题详情...")

        # 使用一个已知的问题ID
        question_id = "27446676"
        detail = self.scraper.get_question_detail(question_id)

        self.assertIsNotNone(detail)
        self.assertEqual(detail['question_id'], question_id)
        self.assertIn('title', detail)
        self.assertIn('author', detail)
        self.assertIn('answer_count', detail)

        print(f"✓ 获取问题详情正常: {detail['title'][:30]}...")

    def test_get_question_answers(self):
        """测试获取问题回答"""
        print("\n📝 测试获取问题回答...")

        question_id = "27446676"
        answers = self.scraper.get_question_answers(question_id, limit=5)

        self.assertIsInstance(answers, list)
        # 可能某些问题没有回答
        if answers:
            self.assertIn('answer_id', answers[0])
            self.assertIn('author', answers[0])

        print(f"✓ 获取回答功能正常，找到 {len(answers)} 个回答")

    def test_get_all_answers_pagination(self):
        """测试分页获取所有回答"""
        print("\n📝 测试分页获取回答...")

        question_id = "27446676"
        all_answers = self.scraper.get_all_answers(question_id, max_answers=30)

        self.assertIsInstance(all_answers, list)
        self.assertLessEqual(len(all_answers), 30)

        print(f"✓ 分页获取功能正常，获取到 {len(all_answers)} 个回答")

    def test_topic_ids(self):
        """测试话题ID映射"""
        print("\n📝 测试话题ID映射...")

        self.assertIn('技术', TOPIC_IDS)
        self.assertIn('生活', TOPIC_IDS)
        self.assertIn('编程', TOPIC_IDS)

        print(f"✓ 话题ID映射正常，包含 {len(TOPIC_IDS)} 个话题")


class TestDataExporter(unittest.TestCase):
    """测试数据导出功能"""

    def setUp(self):
        """测试前准备"""
        self.exporter = DataExporter('output/test')

    def test_export_to_json(self):
        """测试JSON导出"""
        print("\n📝 测试JSON导出...")

        test_data = [
            {'id': 1, 'name': '测试1', 'value': 100},
            {'id': 2, 'name': '测试2', 'value': 200},
        ]

        filepath = self.exporter.export_to_json(test_data, 'test_json')
        self.assertTrue(Path(filepath).exists())

        # 验证可以读取
        loaded_data = self.exporter.load_json(filepath)
        self.assertEqual(len(loaded_data), len(test_data))

        print(f"✓ JSON导出正常: {filepath}")

    def test_export_to_csv(self):
        """测试CSV导出"""
        print("\n📝 测试CSV导出...")

        test_data = [
            {'id': 1, 'name': '测试1', 'value': 100},
            {'id': 2, 'name': '测试2', 'value': 200},
        ]

        filepath = self.exporter.export_to_csv(test_data, 'test_csv')
        self.assertTrue(Path(filepath).exists())

        # 验证可以读取
        loaded_data = self.exporter.load_csv(filepath)
        self.assertEqual(len(loaded_data), len(test_data))

        print(f"✓ CSV导出正常: {filepath}")

    def test_export_questions(self):
        """测试问题数据导出"""
        print("\n📝 测试问题数据导出...")

        test_questions = [
            {
                'question_id': '123',
                'title': '测试问题1',
                'author': '作者1',
                'answer_count': 10,
                'url': 'https://example.com/q/123'
            },
            {
                'question_id': '456',
                'title': '测试问题2',
                'author': '作者2',
                'answer_count': 20,
                'url': 'https://example.com/q/456'
            }
        ]

        results = self.exporter.export_questions(test_questions, 'test_questions')

        self.assertIn('json', results)
        self.assertIn('csv', results)
        self.assertTrue(Path(results['json']).exists())
        self.assertTrue(Path(results['csv']).exists())

        print(f"✓ 问题数据导出正常: {len(results)} 个文件")


class TestDataAnalyzer(unittest.TestCase):
    """测试数据分析功能"""

    def setUp(self):
        """测试前准备"""
        self.analyzer = DataAnalyzer()

        # 准备测试数据
        self.test_questions = [
            {
                'question_id': '1',
                'title': '问题1',
                'author': '作者A',
                'answer_count': 10,
                'follower_count': 100,
                'visited_count': 1000,
                'url': 'url1'
            },
            {
                'question_id': '2',
                'title': '问题2',
                'author': '作者B',
                'answer_count': 20,
                'follower_count': 200,
                'visited_count': 2000,
                'url': 'url2'
            },
            {
                'question_id': '3',
                'title': '问题3',
                'author': '作者A',
                'answer_count': 5,
                'follower_count': 50,
                'visited_count': 500,
                'url': 'url3'
            }
        ]

        self.test_answers = [
            {
                'answer_id': 'a1',
                'author': '作者A',
                'voteup_count': 100,
                'comment_count': 10,
                'content': '回答内容1',
                'url': 'url1'
            },
            {
                'answer_id': 'a2',
                'author': '作者B',
                'voteup_count': 200,
                'comment_count': 20,
                'content': '回答内容2',
                'url': 'url2'
            },
            {
                'answer_id': 'a3',
                'author': '作者A',
                'voteup_count': 50,
                'comment_count': 5,
                'content': '回答内容3',
                'url': 'url3'
            }
        ]

    def test_analyze_questions(self):
        """测试问题分析"""
        print("\n📝 测试问题分析...")

        report = self.analyzer.analyze_questions(self.test_questions)

        self.assertIn('summary', report)
        self.assertEqual(report['summary']['total_questions'], 3)
        self.assertEqual(report['summary']['total_answers'], 35)

        self.assertIn('top_questions_by_answers', report)
        self.assertEqual(len(report['top_questions_by_answers']), 3)

        self.assertIn('top_authors', report)

        print(f"✓ 问题分析正常")
        print(f"  - 总问题数: {report['summary']['total_questions']}")
        print(f"  - 总回答数: {report['summary']['total_answers']}")

    def test_analyze_answers(self):
        """测试回答分析"""
        print("\n📝 测试回答分析...")

        report = self.analyzer.analyze_answers(self.test_answers)

        self.assertIn('summary', report)
        self.assertEqual(report['summary']['total_answers'], 3)
        self.assertEqual(report['summary']['total_votes'], 350)

        self.assertIn('top_answers_by_votes', report)
        self.assertEqual(len(report['top_answers_by_votes']), 3)

        print(f"✓ 回答分析正常")
        print(f"  - 总回答数: {report['summary']['total_answers']}")
        print(f"  - 总点赞数: {report['summary']['total_votes']}")

    def test_generate_text_report(self):
        """测试文本报告生成"""
        print("\n📝 测试文本报告生成...")

        report = self.analyzer.analyze_questions(self.test_questions)
        text_report = self.analyzer.generate_text_report(report, 'questions')

        self.assertIsInstance(text_report, str)
        self.assertIn('知乎数据分析报告', text_report)
        self.assertIn('数据概览', text_report)
        self.assertIn('热门问题排行', text_report)

        print(f"✓ 文本报告生成正常")
        print(f"  - 报告长度: {len(text_report)} 字符")

    def test_generate_comparison_report(self):
        """测试综合分析报告生成"""
        print("\n📝 测试综合分析报告生成...")

        question_detail = {
            'title': '测试问题',
            'author': '作者A',
            'answer_count': 10,
            'follower_count': 100,
            'visited_count': 1000,
            'created_time': '2024-01-01',
            'url': 'test_url'
        }

        report = self.analyzer.generate_comparison_report(question_detail, self.test_answers)

        self.assertIn('question', report)
        self.assertIn('answers_analysis', report)
        self.assertIn('summary', report)

        print(f"✓ 综合分析报告生成正常")


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_full_workflow(self):
        """测试完整工作流"""
        print("\n📝 测试完整工作流...")

        scraper = ZhihuScraper()
        analyzer = DataAnalyzer()
        exporter = DataExporter('output/test')

        try:
            # 1. 搜索问题
            questions = scraper.search_questions("编程", limit=2)
            self.assertGreater(len(questions), 0)

            # 2. 获取问题详情
            question_id = questions[0]['question_id']
            detail = scraper.get_question_detail(question_id)
            self.assertIsNotNone(detail)

            # 3. 获取回答
            answers = scraper.get_all_answers(question_id, max_answers=10)
            self.assertIsInstance(answers, list)

            # 4. 分析数据
            report = analyzer.generate_comparison_report(detail, answers)

            # 5. 导出数据
            exporter.export_questions([detail], 'test_workflow')
            if answers:
                exporter.export_answers(answers, question_id)

            print(f"✓ 完整工作流测试通过")
            print(f"  - 问题: {detail['title'][:30]}...")
            print(f"  - 回答数: {len(answers)}")

        finally:
            scraper.close()


def run_tests():
    """运行所有测试"""
    print("🧪 开始运行知乎爬虫测试套件")
    print("=" * 60)

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestZhihuScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestDataExporter))
    suite.addTests(loader.loadTestsFromTestCase(TestDataAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 打印总结
    print("\n" + "=" * 60)
    print("🧪 测试总结")
    print("=" * 60)
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"耗时: {result.duration:.2f} 秒")

    if result.wasSuccessful():
        print("\n✅ 所有测试通过！")
        return 0
    else:
        print("\n❌ 部分测试失败！")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
