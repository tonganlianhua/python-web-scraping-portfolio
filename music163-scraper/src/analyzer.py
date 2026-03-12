"""
数据分析模块
生成歌手排行、歌曲热度分析和词云
"""

import json
import os
from typing import List, Dict
from collections import Counter
import re

# 词云库（可选，如果没有安装会跳过词云生成）
try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    print("提示: 安装 wordcloud 和 matplotlib 库以生成词云: pip install wordcloud matplotlib")

from config import EXPORT_DIR, WORDCLOUD_MAX_WORDS, TOP_N_ARTISTS, TOP_N_SONGS


class MusicAnalyzer:
    """音乐数据分析器"""

    def __init__(self, output_dir: str = EXPORT_DIR):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def analyze_artists_ranking(self, songs: List[Dict], top_n: int = TOP_N_ARTISTS) -> List[Dict]:
        """
        分析歌手排行

        Args:
            songs: 歌曲数据列表
            top_n: 返回前N名

        Returns:
            歌手排行列表
        """
        artist_counts = Counter()

        for song in songs:
            artists = song.get("artist", "").split(", ")
            for artist in artists:
                if artist.strip():
                    artist_counts[artist.strip()] += 1

        ranking = []
        for artist, count in artist_counts.most_common(top_n):
            ranking.append({
                "rank": len(ranking) + 1,
                "artist": artist,
                "song_count": count
            })

        print(f"生成歌手排行，共 {len(ranking)} 位歌手")
        return ranking

    def analyze_songs_popularity(self, songs: List[Dict], top_n: int = TOP_N_SONGS) -> List[Dict]:
        """
        分析歌曲热度排行

        Args:
            songs: 歌曲数据列表
            top_n: 返回前N名

        Returns:
            歌曲热度排行列表
        """
        # 按播放量排序
        sorted_songs = sorted(
            songs,
            key=lambda x: x.get("play_count", 0),
            reverse=True
        )[:top_n]

        popularity = []
        for idx, song in enumerate(sorted_songs):
            popularity.append({
                "rank": idx + 1,
                "name": song.get("name", ""),
                "artist": song.get("artist", ""),
                "play_count": song.get("play_count", 0),
                "comment_count": song.get("comment_count", 0)
            })

        print(f"生成歌曲热度排行，共 {len(popularity)} 首歌曲")
        return popularity

    def generate_wordcloud(self, comments: List[Dict], max_words: int = WORDCLOUD_MAX_WORDS,
                          filename: str = None, save_json: bool = True) -> Dict[str, str]:
        """
        生成评论词云

        Args:
            comments: 评论数据列表
            max_words: 最多显示词汇数
            filename: 自定义文件名（可选）
            save_json: 是否保存词频统计JSON

        Returns:
            生成的文件路径字典
        """
        if not WORDCLOUD_AVAILABLE:
            print("wordcloud库未安装，跳过词云生成")
            return {}

        if not comments:
            print("没有评论数据，跳过词云生成")
            return {}

        # 提取所有评论文本
        all_text = " ".join([comment.get("content", "") for comment in comments])

        # 提取中英文词汇
        words = self._extract_words(all_text)

        if not words:
            print("未提取到有效词汇")
            return {}

        # 生成词云
        wordcloud = WordCloud(
            width=800,
            height=600,
            background_color="white",
            font_path="C:/Windows/Fonts/msyh.ttc",  # 微软雅黑字体，支持中文
            max_words=max_words,
            repeat=False
        ).generate(" ".join(words))

        # 保存词云图片
        if filename is None:
            filename = "wordcloud.png"
        image_path = os.path.join(self.output_dir, filename)

        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(image_path, bbox_inches="tight", dpi=300)
        plt.close()

        print(f"词云图片已保存到: {image_path}")

        results = {"wordcloud_image": image_path}

        # 保存词频统计
        if save_json:
            word_freq = Counter(words).most_common(max_words)
            freq_filename = filename.replace(".png", "_word_freq.json")
            freq_path = os.path.join(self.output_dir, freq_filename)

            freq_data = [
                {"word": word, "count": count}
                for word, count in word_freq
            ]

            with open(freq_path, "w", encoding="utf-8") as f:
                json.dump(freq_data, f, ensure_ascii=False, indent=2)

            print(f"词频统计已保存到: {freq_path}")
            results["word_freq_json"] = freq_path

        return results

    def _extract_words(self, text: str) -> List[str]:
        """
        从文本中提取中英文词汇

        Args:
            text: 输入文本

        Returns:
            词汇列表
        """
        words = []

        # 提取中文词汇（简单按字分割，实际建议使用jieba分词）
        chinese_chars = re.findall(r"[\u4e00-\u9fff]+", text)
        for chars in chinese_chars:
            # 将连续中文字符分割成单个词（简单处理）
            if len(chars) >= 2:
                words.extend(chars)  # 使用单个字符作为词汇
            else:
                words.append(chars)

        # 提取英文单词
        english_words = re.findall(r"[a-zA-Z]{2,}", text.lower())
        words.extend(english_words)

        # 过滤停用词
        stopwords = {"的", "了", "是", "在", "我", "有", "和", "就", "不",
                   "人", "都", "一", "一个", "上", "也", "很", "到", "说",
                   "the", "and", "is", "of", "to", "a", "in", "that", "it",
                   "for", "on", "with", "as", "this", "was", "at", "be"}

        words = [word for word in words if word not in stopwords and len(word) > 1]

        return words

    def generate_report(self, songs: List[Dict], comments: List[Dict] = None,
                       include_wordcloud: bool = True, filename: str = None) -> str:
        """
        生成完整的数据分析报告

        Args:
            songs: 歌曲数据列表
            comments: 评论数据列表（可选）
            include_wordcloud: 是否生成词云
            filename: 报告文件名（可选）

        Returns:
            报告文件路径
        """
        if filename is None:
            from datetime import datetime
            filename = f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        report_path = os.path.join(self.output_dir, filename)

        report = {
            "generated_at": None,
            "artists_ranking": self.analyze_artists_ranking(songs),
            "songs_popularity": self.analyze_songs_popularity(songs),
            "statistics": self._calculate_statistics(songs)
        }

        from datetime import datetime
        report["generated_at"] = datetime.now().isoformat()

        # 生成词云（如果启用且有评论）
        if include_wordcloud and comments and WORDCLOUD_AVAILABLE:
            wordcloud_results = self.generate_wordcloud(comments)
            if wordcloud_results:
                report["wordcloud"] = wordcloud_results

        # 保存报告
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"数据分析报告已保存到: {report_path}")
        return report_path

    def _calculate_statistics(self, songs: List[Dict]) -> Dict:
        """
        计算基本统计数据

        Args:
            songs: 歌曲数据列表

        Returns:
            统计数据字典
        """
        if not songs:
            return {}

        total_songs = len(songs)
        total_plays = sum(song.get("play_count", 0) for song in songs)
        total_comments = sum(song.get("comment_count", 0) for song in songs)

        # 统计所有歌手
        artists = set()
        for song in songs:
            song_artists = song.get("artist", "").split(", ")
            artists.update([a.strip() for a in song_artists if a.strip()])

        # 计算平均数据
        avg_plays = total_plays / total_songs if total_songs > 0 else 0
        avg_comments = total_comments / total_songs if total_songs > 0 else 0

        return {
            "total_songs": total_songs,
            "total_artists": len(artists),
            "total_plays": total_plays,
            "total_comments": total_comments,
            "avg_plays_per_song": round(avg_plays, 2),
            "avg_comments_per_song": round(avg_comments, 2)
        }
