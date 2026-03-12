# -*- coding: utf-8 -*-
"""
快速测试脚本 - 测试项目结构和基本功能（不涉及网络请求）
"""

import sys
import os
import json

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from config import get_random_user_agent, random_delay, TOP_LISTS, get_headers
from export import DataExporter
from analyzer import MusicAnalyzer


def test_imports():
    """测试导入"""
    print("[OK] 测试模块导入成功")


def test_config():
    """测试配置模块"""
    print("\n测试配置模块...")

    # 测试User-Agent
    ua = get_random_user_agent()
    assert isinstance(ua, str) and len(ua) > 0
    print(f"  [OK] User-Agent: {ua[:50]}...")

    # 测试请求头
    headers = get_headers()
    assert "User-Agent" in headers
    assert "Accept" in headers
    print("  [OK] 请求头生成成功")

    # 测试榜单配置
    assert len(TOP_LISTS) == 5
    assert "hot" in TOP_LISTS
    print("  [OK] 榜单配置正确")

    # 测试随机延时（小值）
    import time
    start = time.time()
    delay = random_delay()
    end = time.time()
    actual = end - start
    print(f"  [OK] 随机延时: {delay:.2f}s")


def test_exporter():
    """测试导出器"""
    print("\n测试数据导出器...")

    exporter = DataExporter()
    print("  [OK] 导出器初始化成功")

    # 测试数据
    test_songs = [
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

    # 测试CSV导出
    csv_path = exporter.export_songs_to_csv(test_songs, "test_songs.csv")
    assert os.path.exists(csv_path)
    print(f"  [OK] CSV导出成功: {csv_path}")

    # 测试JSON导出
    json_path = exporter.export_songs_to_json(test_songs, "test_songs.json")
    assert os.path.exists(json_path)
    print(f"  [OK] JSON导出成功: {json_path}")

    # 测试读取
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["name"] == "测试歌曲"
    print("  [OK] JSON读取验证成功")


def test_analyzer():
    """测试分析器"""
    print("\n测试音乐分析器...")

    analyzer = MusicAnalyzer()
    print("  [OK] 分析器初始化成功")

    # 测试数据
    test_songs = [
        {
            "id": 1,
            "name": "歌曲1",
            "artist": "歌手A",
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
            "artist": "歌手B",
            "album": "专辑3",
            "play_count": 600000,
            "comment_count": 2000,
            "duration": 200000,
            "url": "https://test3.com"
        }
    ]

    # 测试歌手排行
    ranking = analyzer.analyze_artists_ranking(test_songs, top_n=10)
    assert len(ranking) == 2
    assert ranking[0]["artist"] == "歌手A"
    assert ranking[0]["song_count"] == 2
    print(f"  [OK] 歌手排行分析成功: {ranking[0]['artist']} ({ranking[0]['song_count']}首)")

    # 测试歌曲热度
    popularity = analyzer.analyze_songs_popularity(test_songs, top_n=10)
    assert len(popularity) == 3
    assert popularity[0]["name"] == "歌曲1"
    print(f"  [OK] 歌曲热度分析成功: {popularity[0]['name']}")

    # 测试统计
    stats = analyzer._calculate_statistics(test_songs)
    assert stats["total_songs"] == 3
    assert stats["total_artists"] == 2
    assert stats["total_plays"] == 2400000
    print(f"  [OK] 统计计算成功: {stats['total_songs']}首歌曲, {stats['total_artists']}位歌手")


def test_file_structure():
    """测试文件结构"""
    print("\n测试项目文件结构...")

    base_dir = os.path.dirname(__file__)

    # 检查必要文件和目录
    required = {
        "src/config.py": "配置文件",
        "src/api_client.py": "API客户端",
        "src/export.py": "导出模块",
        "src/analyzer.py": "分析模块",
        "src/scraper.py": "爬虫主模块",
        "demo.py": "演示脚本",
        "test.py": "测试脚本",
        "README.md": "README文档",
        "requirements.txt": "依赖列表",
        "examples/get_toplist.py": "示例1",
        "examples/search_music.py": "示例2",
        "examples/export_data.py": "示例3",
        "examples/analyze_data.py": "示例4",
    }

    all_exist = True
    for path, desc in required.items():
        full_path = os.path.join(base_dir, path)
        exists = os.path.exists(full_path)
        status = "[OK]" if exists else "[FAIL]"
        print(f"  {status} {desc}: {path}")
        if not exists:
            all_exist = False

    assert all_exist, "部分文件缺失"


def main():
    """运行所有测试"""
    print("="*60)
    print("网易云音乐爬虫 - 快速测试")
    print("="*60)

    try:
        test_imports()
        test_file_structure()
        test_config()
        test_exporter()
        test_analyzer()

        print("\n" + "="*60)
        print("[SUCCESS] 所有测试通过!")
        print("="*60)
        print("\n项目结构完整,基础功能正常。")
        print("注意: 完整的网络API测试需要运行: python test.py")
        print("功能演示可以运行: python demo.py")
        print("="*60 + "\n")

        return 0

    except AssertionError as e:
        print(f"\n[FAIL] 测试错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n[ERROR] 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
