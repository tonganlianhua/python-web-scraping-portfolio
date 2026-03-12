"""
网易云音乐爬虫测试脚本
测试各个模块的功能
"""

import sys
import os
import unittest

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from config import get_random_user_agent, random_delay, TOP_LISTS, get_headers
from api_client import NetEaseMusicAPI
from export import DataExporter
from analyzer import MusicAnalyzer
from scraper import Music163Scraper


class TestConfig(unittest.TestCase):
    """测试配置模块"""

    def test_get_random_user_agent(self):
        """测试随机User-Agent获取"""
        ua = get_random_user_agent()
        self.assertIsInstance(ua, str)
        self.assertTrue(len(ua) > 0)
        print("✓ 测试通过: get_random_user_agent()")

    def test_random_delay(self):
        """测试随机延时"""
        import time
        start = time.time()
        delay = random_delay()
        end = time.time()
        actual_delay = end - start
        self.assertTrue(actual_delay >= delay * 0.9)  # 允许10%误差
        print(f"✓ 测试通过: random_delay() (延迟: {delay:.2f}s)")

    def test_get_headers(self):
        """测试获取请求头"""
        headers = get_headers()
        self.assertIsInstance(headers, dict)
        self.assertIn("User-Agent", headers)
        self.assertIn("Accept", headers)
        print("✓ 测试通过: get_headers()")

    def test_top_lists(self):
        """测试榜单配置"""
        self.assertIn("hot", TOP_LISTS)
        self.assertIn("new", TOP_LISTS)
        self.assertEqual(len(TOP_LISTS), 5)
        print("✓ 测试通过: TOP_LISTS 配置")


class TestNetEaseMusicAPI(unittest.TestCase):
    """测试API客户端"""

    def setUp(self):
        """测试前准备"""
        self.api = NetEaseMusicAPI()

    def test_get_all_top_lists_info(self):
        """测试获取榜单信息"""
        lists_info = self.api.get_all_top_lists_info()
        self.assertIsInstance(lists_info, dict)
        self.assertTrue(len(lists_info) > 0)
        print("✓ 测试通过: get_all_top_lists_info()")

    def test_get_top_list_songs(self):
        """测试获取排行榜歌曲"""
        songs = self.api.get_top_list_songs("hot", limit=5)
        self.assertIsNotNone(songs)
        self.assertIsInstance(songs, list)
        if songs:
            self.assertIsInstance(songs[0], dict)
            self.assertIn("name", songs[0])
            self.assertIn("artist", songs[0])
        print("✓ 测试通过: get_top_list_songs()")

    def test_search_songs(self):
        """测试搜索歌曲"""
        songs = self.api.search_songs("周杰伦", limit=5)
        self.assertIsNotNone(songs)
        self.assertIsInstance(songs, list)
        if songs:
            self.assertIsInstance(songs[0], dict)
            self.assertIn("name", songs[0])
        print("✓ 测试通过: search_songs()")

    def test_get_song_comments(self):
        """测试获取歌曲评论"""
        # 先获取一首歌曲
        songs = self.api.get_top_list_songs("hot", limit=1)
        if songs and songs[0].get("id"):
            song_id = songs[0]["id"]
            comments = self.api.get_song_comments(song_id, limit=3)
            self.assertIsNotNone(comments)
            self.assertIsInstance(comments, list)
            print("✓ 测试通过: get_song_comments()")
        else:
            print("⚠ 跳过测试: get_song_comments() (无法获取歌曲ID)")


class TestDataExporter(unittest.TestCase):
    """测试数据导出器"""

    def setUp(self):
        """测试前准备"""
        self.exporter = DataExporter()
        self.test_songs = [
            {
                "id": 1,
                "name": "测试歌曲",
                "artist": "测试歌手",
                "album": "测试专辑",
                "play_count": 100000,
                "comment_count": 1000,
                "duration": 300000,
                "url": "https://test.com"
            }
        ]
        self.test_comments = [
            {
                "id": 1,
                "song_id": 1,
                "content": "测试评论内容",
                "liked_count": 100,
                "time": 1704067200000,
                "time_str": "2024-01-01 00:00:00",
                "user": "测试用户"
            }
        ]

    def tearDown(self):
        """测试后清理"""
        # 清理生成的测试文件
        import glob
        for file in glob.glob(os.path.join(self.exporter.export_dir, "test_*")):
            try:
                os.remove(file)
            except:
                pass

    def test_export_songs_to_csv(self):
        """测试导出歌曲到CSV"""
        filepath = self.exporter.export_songs_to_csv(
            self.test_songs,
            "test_songs.csv"
        )
        self.assertIsNotNone(filepath)
        self.assertTrue(os.path.exists(filepath))
        print("✓ 测试通过: export_songs_to_csv()")

    def test_export_songs_to_json(self):
        """测试导出歌曲到JSON"""
        filepath = self.exporter.export_songs_to_json(
            self.test_songs,
            "test_songs.json"
        )
        self.assertIsNotNone(filepath)
        self.assertTrue(os.path.exists(filepath))
        print("✓ 测试通过: export_songs_to_json()")

    def test_export_comments_to_csv(self):
        """测试导出评论到CSV"""
        filepath = self.exporter.export_comments_to_csv(
            self.test_comments,
            "test_comments.csv"
        )
        self.assertIsNotNone(filepath)
        self.assertTrue(os.path.exists(filepath))
        print("✓ 测试通过: export_comments_to_csv()")

    def test_export_comments_to_json(self):
        """测试导出评论到JSON"""
        filepath = self.exporter.export_comments_to_json(
            self.test_comments,
            "test_comments.json"
        )
        self.assertIsNotNone(filepath)
        self.assertTrue(os.path.exists(filepath))
        print("✓ 测试通过: export_comments_to_json()")


class TestMusicAnalyzer(unittest.TestCase):
    """测试音乐分析器"""

    def setUp(self):
        """测试前准备"""
        self.analyzer = MusicAnalyzer()
        self.test_songs = [
            {
                "id": 1,
                "name": "歌曲1",
                "artist": "歌手A, 歌手B",
                "album": "专辑1",
                "play_count": 1000000,
                "comment_count": 5000,
                "duration": 300000,
                "url": "https://test1.com"
            },
            {
                "id": 2,
                "name": "歌曲2",
                "artist": "歌手A",
                "album": "专辑2",
                "play_count": 800000,
                "comment_count": 3000,
                "duration": 250000,
                "url": "https://test2.com"
            },
            {
                "id": 3,
                "name": "歌曲3",
                "artist": "歌手C",
                "album": "专辑3",
                "play_count": 600000,
                "comment_count": 2000,
                "duration": 200000,
                "url": "https://test3.com"
            }
        ]

    def test_analyze_artists_ranking(self):
        """测试歌手排行分析"""
        ranking = self.analyzer.analyze_artists_ranking(self.test_songs, top_n=5)
        self.assertIsInstance(ranking, list)
        self.assertTrue(len(ranking) > 0)
        self.assertEqual(ranking[0]["artist"], "歌手A")
        self.assertEqual(ranking[0]["song_count"], 2)
        print("✓ 测试通过: analyze_artists_ranking()")

    def test_analyze_songs_popularity(self):
        """测试歌曲热度分析"""
        popularity = self.analyzer.analyze_songs_popularity(self.test_songs, top_n=5)
        self.assertIsInstance(popularity, list)
        self.assertEqual(len(popularity), 3)
        self.assertEqual(popularity[0]["name"], "歌曲1")
        print("✓ 测试通过: analyze_songs_popularity()")

    def test_calculate_statistics(self):
        """测试统计数据计算"""
        stats = self.analyzer._calculate_statistics(self.test_songs)
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats["total_songs"], 3)
        self.assertEqual(stats["total_artists"], 3)
        print("✓ 测试通过: _calculate_statistics()")


class TestMusic163Scraper(unittest.TestCase):
    """测试爬虫主类"""

    def setUp(self):
        """测试前准备"""
        self.scraper = Music163Scraper()

    def test_get_available_top_lists(self):
        """测试获取可用榜单"""
        lists_info = self.scraper.get_available_top_lists()
        self.assertIsInstance(lists_info, dict)
        self.assertTrue(len(lists_info) > 0)
        print("✓ 测试通过: get_available_top_lists()")

    def test_scrape_top_list(self):
        """测试爬取排行榜（少量数据）"""
        result = self.scraper.scrape_top_list(
            list_type="hot",
            limit=3,
            fetch_comments=False,
            export=False,
            analyze=False
        )
        self.assertIsInstance(result, dict)
        self.assertIn("songs", result)
        self.assertTrue(len(result["songs"]) > 0)
        print("✓ 测试通过: scrape_top_list()")


def run_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("网易云音乐爬虫 - 单元测试")
    print("="*60 + "\n")

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestNetEaseMusicAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestDataExporter))
    suite.addTests(loader.loadTestsFromTestCase(TestMusicAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestMusic163Scraper))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 输出总结
    print("\n" + "="*60)
    print(f"测试完成！")
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("="*60 + "\n")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
