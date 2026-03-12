"""
网易云音乐爬虫主模块
整合API客户端、数据导出和分析功能
"""

from typing import List, Dict, Optional

from api_client import NetEaseMusicAPI
from export import DataExporter
from analyzer import MusicAnalyzer


class Music163Scraper:
    """网易云音乐爬虫主类"""

    def __init__(self):
        """初始化爬虫"""
        self.api = NetEaseMusicAPI()
        self.exporter = DataExporter()
        self.analyzer = MusicAnalyzer()

    def scrape_top_list(self, list_type: str = "hot", limit: int = 50,
                       fetch_comments: bool = True, comments_limit: int = 20,
                       export: bool = True, analyze: bool = True) -> Dict:
        """
        爬取排行榜数据

        Args:
            list_type: 榜单类型（hot, new, original, soar, recommend）
            limit: 获取歌曲数量
            fetch_comments: 是否获取评论
            comments_limit: 每首歌获取评论数
            export: 是否导出数据
            analyze: 是否生成分析报告

        Returns:
            包含所有数据的字典
        """
        print(f"\n{'='*50}")
        print(f"开始爬取 {list_type} 榜单")
        print(f"{'='*50}\n")

        # 获取榜单歌曲
        songs = self.api.get_top_list_songs(list_type, limit)
        if not songs:
            print("获取歌曲列表失败")
            return {}

        result = {
            "list_type": list_type,
            "list_name": self.api.get_all_top_lists_info().get(list_type, ""),
            "songs": songs,
            "comments": []
        }

        # 获取评论
        if fetch_comments:
            print(f"\n开始获取评论...")
            all_comments = []

            for idx, song in enumerate(songs[:10], 1):  # 限制获取前10首歌的评论
                print(f"进度: {idx}/{min(len(songs), 10)}")
                comments = self.api.get_song_comments(song["id"], comments_limit)
                if comments:
                    all_comments.extend(comments)

            result["comments"] = all_comments
            print(f"共获取 {len(all_comments)} 条评论")

        # 导出数据
        if export:
            print(f"\n开始导出数据...")
            export_results = self.exporter.export_all(
                songs,
                result["comments"] if fetch_comments else None,
                prefix=f"{list_type}_toplist"
            )
            result["export"] = export_results

        # 生成分析报告
        if analyze:
            print(f"\n开始生成分析报告...")
            report_path = self.analyzer.generate_report(
                songs,
                result["comments"] if fetch_comments else None,
                include_wordcloud=fetch_comments and len(result["comments"]) > 0,
                filename=f"{list_type}_analysis_report.json"
            )
            result["report"] = report_path

        print(f"\n{'='*50}")
        print(f"爬取完成！")
        print(f"歌曲数: {len(songs)}")
        print(f"评论数: {len(result.get('comments', []))}")
        print(f"{'='*50}\n")

        return result

    def search_and_scrape(self, keyword: str, limit: int = 30,
                         fetch_comments: bool = True, comments_limit: int = 20,
                         export: bool = True) -> Dict:
        """
        搜索歌曲并爬取数据

        Args:
            keyword: 搜索关键词
            limit: 搜索结果数量
            fetch_comments: 是否获取评论
            comments_limit: 每首歌获取评论数
            export: 是否导出数据

        Returns:
            包含所有数据的字典
        """
        print(f"\n{'='*50}")
        print(f"搜索关键词: {keyword}")
        print(f"{'='*50}\n")

        # 搜索歌曲
        songs = self.api.search_songs(keyword, limit)
        if not songs:
            print("搜索结果为空")
            return {}

        result = {
            "keyword": keyword,
            "songs": songs,
            "comments": []
        }

        # 获取评论
        if fetch_comments:
            print(f"\n开始获取评论...")
            all_comments = []

            for idx, song in enumerate(songs[:5], 1):  # 限制获取前5首歌的评论
                print(f"进度: {idx}/{min(len(songs), 5)}")
                comments = self.api.get_song_comments(song["id"], comments_limit)
                if comments:
                    all_comments.extend(comments)

            result["comments"] = all_comments
            print(f"共获取 {len(all_comments)} 条评论")

        # 导出数据
        if export:
            print(f"\n开始导出数据...")
            export_results = self.exporter.export_all(
                songs,
                result["comments"] if fetch_comments else None,
                prefix=f"search_{keyword}"
            )
            result["export"] = export_results

        print(f"\n{'='*50}")
        print(f"搜索爬取完成！")
        print(f"歌曲数: {len(songs)}")
        print(f"评论数: {len(result.get('comments', []))}")
        print(f"{'='*50}\n")

        return result

    def get_available_top_lists(self) -> Dict[str, str]:
        """
        获取所有可用榜单

        Returns:
            榜单字典
        """
        return self.api.get_all_top_lists_info()
