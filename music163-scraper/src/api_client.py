"""
网易云音乐API客户端
使用网易云音乐非官方API接口
"""

import requests
import json
from typing import Dict, List, Any, Optional
import time

from config import (
    API_BASE_URL,
    TOP_LISTS,
    MAX_RETRIES,
    RETRY_DELAY,
    get_headers,
    random_delay
)


class NetEaseMusicAPI:
    """网易云音乐API客户端"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(get_headers())

    def _request(self, url: str, params: Optional[Dict] = None, retries: int = MAX_RETRIES) -> Optional[Dict]:
        """
        发送HTTP请求，带重试机制

        Args:
            url: 请求URL
            params: 请求参数
            retries: 剩余重试次数

        Returns:
            响应数据字典，失败返回None
        """
        try:
            random_delay()
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            if retries > 0:
                print(f"等待 {RETRY_DELAY} 秒后重试... (剩余重试次数: {retries})")
                time.sleep(RETRY_DELAY)
                return self._request(url, params, retries - 1)
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析响应失败: {e}")
            return None

    def get_top_list_songs(self, list_type: str = "hot", limit: int = 50) -> Optional[List[Dict]]:
        """
        获取排行榜歌曲列表

        Args:
            list_type: 榜单类型（hot, new, original, soar, recommend）
            limit: 获取歌曲数量

        Returns:
            歌曲信息列表
        """
        list_id = TOP_LISTS.get(list_type)
        if not list_id:
            print(f"未找到榜单类型: {list_type}")
            return None

        url = f"{API_BASE_URL}/playlist/detail"
        params = {"id": list_id}

        data = self._request(url, params)
        if not data or data.get("code") != 200:
            print(f"获取榜单失败: {data}")
            return None

        tracks = data.get("playlist", {}).get("tracks", [])
        songs = []

        for track in tracks[:limit]:
            song_info = {
                "id": track.get("id"),
                "name": track.get("name"),
                "artist": ", ".join([ar.get("name", "") for ar in track.get("artists", [])]),
                "album": track.get("album", {}).get("name", ""),
                "play_count": track.get("playCount", 0),
                "comment_count": track.get("commentCount", 0),
                "duration": track.get("duration", 0),
                "url": f"https://music.163.com/#/song?id={track.get('id')}"
            }
            songs.append(song_info)

        print(f"成功获取 {len(songs)} 首歌曲")
        return songs

    def get_song_comments(self, song_id: int, limit: int = 20) -> Optional[List[Dict]]:
        """
        获取歌曲热门评论

        Args:
            song_id: 歌曲ID
            limit: 获取评论数量

        Returns:
            评论列表
        """
        url = f"{API_BASE_URL}/v1/comment/hot"
        params = {
            "id": song_id,
            "limit": limit,
            "type": 0  # 0表示歌曲评论
        }

        data = self._request(url, params)
        if not data or data.get("code") != 200:
            print(f"获取评论失败: {data}")
            return None

        comments = []
        hot_comments = data.get("hotComments", [])

        for comment in hot_comments:
            comment_info = {
                "id": comment.get("id"),
                "content": comment.get("content", ""),
                "liked_count": comment.get("likedCount", 0),
                "time": comment.get("time", 0),
                "time_str": self._format_timestamp(comment.get("time", 0)),
                "user": comment.get("user", {}).get("nickname", ""),
                "song_id": song_id
            }
            comments.append(comment_info)

        print(f"成功获取 {len(comments)} 条评论")
        return comments

    def search_songs(self, keyword: str, limit: int = 30) -> Optional[List[Dict]]:
        """
        搜索歌曲

        Args:
            keyword: 搜索关键词
            limit: 返回结果数量

        Returns:
            歌曲列表
        """
        url = f"{API_BASE_URL}/search"
        params = {
            "keywords": keyword,
            "type": 1,  # 1表示搜索单曲
            "limit": limit
        }

        data = self._request(url, params)
        if not data or data.get("code") != 200:
            print(f"搜索失败: {data}")
            return None

        songs = []
        song_songs = data.get("result", {}).get("songs", [])

        for song in song_songs[:limit]:
            song_info = {
                "id": song.get("id"),
                "name": song.get("name"),
                "artist": ", ".join([ar.get("name", "") for ar in song.get("artists", [])]),
                "album": song.get("album", {}).get("name", ""),
                "duration": song.get("duration", 0),
                "url": f"https://music.163.com/#/song?id={song.get('id')}"
            }
            songs.append(song_info)

        print(f"搜索到 {len(songs)} 首歌曲")
        return songs

    def get_all_top_lists_info(self) -> Dict[str, str]:
        """
        获取所有排行榜信息

        Returns:
            榜单类型与名称的映射
        """
        return {
            "hot": "热歌榜",
            "new": "新歌榜",
            "original": "原创榜",
            "soar": "飙升榜",
            "recommend": "推荐榜"
        }

    @staticmethod
    def _format_timestamp(timestamp: int) -> str:
        """
        将时间戳转换为可读格式

        Args:
            timestamp: 毫秒时间戳

        Returns:
            格式化的时间字符串
        """
        dt = time.localtime(timestamp / 1000)
        return time.strftime("%Y-%m-%d %H:%M:%S", dt)
