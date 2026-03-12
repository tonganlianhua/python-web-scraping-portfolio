"""
微博帖子模块
用于解析和存储微博帖子数据
"""

from typing import Dict, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WeiboPost:
    """微博帖子类"""

    def __init__(
        self,
        post_id: str = '',
        user_id: str = '',
        username: str = '',
        content: str = '',
        created_at: str = '',
        likes: int = 0,
        comments: int = 0,
        reposts: int = 0,
        is_repost: bool = False,
        original_post_id: str = '',
        images: List[str] = None,
        topics: List[str] = None,
        url: str = '',
        device: str = '',
        location: str = ''
    ):
        """
        初始化微博帖子

        Args:
            post_id: 帖子ID
            user_id: 用户ID
            username: 用户名
            content: 帖子内容
            created_at: 发布时间
            likes: 点赞数
            comments: 评论数
            reposts: 转发数
            is_repost: 是否转发
            original_post_id: 原帖ID
            images: 图片URL列表
            topics: 话题标签列表
            url: 帖子URL
            device: 发布设备
            location: 位置
        """
        self.post_id = post_id
        self.user_id = user_id
        self.username = username
        self.content = content
        self.created_at = created_at
        self.likes = likes
        self.comments = comments
        self.reposts = reposts
        self.is_repost = is_repost
        self.original_post_id = original_post_id
        self.images = images or []
        self.topics = topics or []
        self.url = url
        self.device = device
        self.location = location
        self.crawled_at = datetime.now().isoformat()

    @classmethod
    def from_dict(cls, data: Dict) -> 'WeiboPost':
        """从字典创建帖子对象"""
        return cls(
            post_id=data.get('post_id', ''),
            user_id=data.get('user_id', ''),
            username=data.get('username', ''),
            content=data.get('content', ''),
            created_at=data.get('created_at', ''),
            likes=data.get('likes', 0),
            comments=data.get('comments', 0),
            reposts=data.get('reposts', 0),
            is_repost=data.get('is_repost', False),
            original_post_id=data.get('original_post_id', ''),
            images=data.get('images', []),
            topics=data.get('topics', []),
            url=data.get('url', ''),
            device=data.get('device', ''),
            location=data.get('location', '')
        )

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'post_id': self.post_id,
            'user_id': self.user_id,
            'username': self.username,
            'content': self.content,
            'created_at': self.created_at,
            'likes': self.likes,
            'comments': self.comments,
            'reposts': self.reposts,
            'is_repost': self.is_repost,
            'original_post_id': self.original_post_id,
            'images': self.images,
            'topics': self.topics,
            'url': self.url,
            'device': self.device,
            'location': self.location,
            'crawled_at': self.crawled_at
        }

    def __repr__(self) -> str:
        content_preview = self.content[:30] + '...' if len(self.content) > 30 else self.content
        return f"WeiboPost(id='{self.post_id}', user='{self.username}', content='{content_preview}')"
