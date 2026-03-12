"""
微博API接口模块
提供搜索、用户信息获取等功能
注意：新浪微博API需要Cookie和登录状态，本模块提供基础框架
"""

from typing import List, Dict, Optional
from .scraper import WeiboScraper
from .user import WeiboUser
from .weibo import WeiboPost
import re
import json
import logging

logger = logging.getLogger(__name__)


class WeiboAPI(WeiboScraper):
    """微博API接口"""

    def __init__(self, cookie: Optional[str] = None, proxy: Optional[Dict[str, str]] = None):
        """
        初始化微博API

        Args:
            cookie: 登录Cookie（可选，用于访问需要登录的内容）
            proxy: 代理设置
        """
        super().__init__(proxy)
        if cookie:
            self.session.cookies.set('SUB', cookie, domain='.weibo.com')
            logger.info("Cookie loaded")

        self.base_url = 'https://weibo.com'
        self.api_base = 'https://weibo.com/ajax'

    def get_user_info(self, user_id: str) -> Optional[WeiboUser]:
        """
        获取用户信息

        Args:
            user_id: 用户ID或昵称

        Returns:
            WeiboUser对象或None
        """
        try:
            # 用户主页URL
            url = f'{self.base_url}/u/{user_id}'

            soup = self.get_soup(url)
            if not soup:
                logger.error(f"Failed to get user page: {user_id}")
                return None

            # 解析用户信息（实际解析需要根据页面结构调整）
            user = WeiboUser(
                user_id=user_id,
                username=self._extract_text(soup, '.screen-name'),
                bio=self._extract_text(soup, '.profile-bio'),
                url=url
            )

            logger.info(f"Got user info: {user.username}")
            return user

        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None

    def search_posts(
        self,
        keyword: str,
        page: int = 1,
        max_results: int = 20
    ) -> List[WeiboPost]:
        """
        搜索微博帖子

        Args:
            keyword: 搜索关键词
            page: 页码
            max_results: 最大结果数

        Returns:
            微博帖子列表
        """
        try:
            # 搜索URL
            url = f'{self.base_url}/search'
            params = {
                'q': keyword,
                'page': page
            }

            soup = self.get_soup(url, params=params)
            if not soup:
                logger.error(f"Failed to search: {keyword}")
                return []

            # 解析搜索结果（实际解析需要根据页面结构调整）
            posts = []
            # 这里是示例，实际需要解析HTML或JSON数据

            logger.info(f"Found {len(posts)} posts for keyword: {keyword}")
            return posts

        except Exception as e:
            logger.error(f"Error searching posts: {e}")
            return []

    def get_user_posts(
        self,
        user_id: str,
        page: int = 1,
        max_posts: int = 20
    ) -> List[WeiboPost]:
        """
        获取用户微博列表

        Args:
            user_id: 用户ID
            page: 页码
            max_posts: 最大微博数

        Returns:
            微博帖子列表
        """
        try:
            # API接口URL
            url = f'{self.api_base}/statuses/mymblog'
            params = {
                'uid': user_id,
                'page': page,
                'feature': 0
            }

            response = self.request(url, params=params)
            if not response:
                return []

            # 解析JSON数据
            data = response.json()
            posts = []

            if 'data' in data and 'list' in data['data']:
                for item in data['data']['list'][:max_posts]:
                    post = self._parse_post(item)
                    if post:
                        posts.append(post)

            logger.info(f"Got {len(posts)} posts for user: {user_id}")
            return posts

        except Exception as e:
            logger.error(f"Error getting user posts: {e}")
            return []

    def get_hot_topics(self) -> List[Dict]:
        """
        获取微博热搜话题

        Returns:
            热搜话题列表
        """
        try:
            # 热搜API
            url = f'{self.api_base}/side/hotSearch'

            response = self.request(url)
            if not response:
                return []

            data = response.json()
            topics = []

            if 'data' in data and 'realtime' in data['data']:
                for item in data['data']['realtime']:
                    topics.append({
                        'rank': item.get('rank'),
                        'word': item.get('word'),
                        'hot': item.get('num'),
                        'category': item.get('category')
                    })

            logger.info(f"Got {len(topics)} hot topics")
            return topics

        except Exception as e:
            logger.error(f"Error getting hot topics: {e}")
            return []

    def get_post_detail(self, post_id: str) -> Optional[WeiboPost]:
        """
        获取微博详情

        Args:
            post_id: 帖子ID

        Returns:
            WeiboPost对象或None
        """
        try:
            # 详情API
            url = f'{self.api_base}/statuses/show'
            params = {'id': post_id}

            response = self.request(url, params=params)
            if not response:
                return None

            data = response.json()
            post = self._parse_post(data)

            logger.info(f"Got post detail: {post_id}")
            return post

        except Exception as e:
            logger.error(f"Error getting post detail: {e}")
            return None

    def get_post_comments(
        self,
        post_id: str,
        max_comments: int = 50
    ) -> List[Dict]:
        """
        获取微博评论

        Args:
            post_id: 帖子ID
            max_comments: 最大评论数

        Returns:
            评论列表
        """
        try:
            # 评论API
            url = f'{self.api_base}/comments/show'
            params = {
                'id': post_id,
                'page': 1,
                'max_id_type': 0
            }

            response = self.request(url, params=params)
            if not response:
                return []

            data = response.json()
            comments = []

            if 'data' in data and 'data' in data['data']:
                for item in data['data']['data'][:max_comments]:
                    comments.append({
                        'comment_id': item.get('id'),
                        'user_id': item.get('user', {}).get('id'),
                        'username': item.get('user', {}).get('screen_name'),
                        'content': item.get('text'),
                        'likes': item.get('like_count', 0),
                        'created_at': item.get('created_at')
                    })

            logger.info(f"Got {len(comments)} comments for post: {post_id}")
            return comments

        except Exception as e:
            logger.error(f"Error getting comments: {e}")
            return []

    def _extract_text(self, soup, selector: str) -> str:
        """从BeautifulSoup提取文本"""
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else ''

    def _parse_post(self, data: Dict) -> Optional[WeiboPost]:
        """解析微博帖子数据"""
        try:
            # 提取话题标签
            content = data.get('text', '')
            topics = re.findall(r'#([^#]+)#', content)

            # 提取图片
            images = []
            if 'pics' in data:
                for pic in data['pics']:
                    images.append(pic.get('large', {}).get('url', ''))

            post = WeiboPost(
                post_id=data.get('id'),
                user_id=data.get('user', {}).get('id'),
                username=data.get('user', {}).get('screen_name'),
                content=content,
                created_at=data.get('created_at'),
                likes=data.get('attitudes_count', 0),
                comments=data.get('comments_count', 0),
                reposts=data.get('reposts_count', 0),
                is_repost=('retweeted_status' in data),
                original_post_id=data.get('retweeted_status', {}).get('id', ''),
                images=images,
                topics=topics,
                url=f"{self.base_url}/{data.get('id')}",
                device=data.get('source', '')
            )
            return post

        except Exception as e:
            logger.error(f"Error parsing post: {e}")
            return None
