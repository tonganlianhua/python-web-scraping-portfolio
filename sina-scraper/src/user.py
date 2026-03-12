"""
微博用户信息模块
用于解析和存储微博用户数据
"""

from typing import Dict, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WeiboUser:
    """微博用户类"""

    def __init__(
        self,
        user_id: str = '',
        username: str = '',
        nickname: str = '',
        avatar: str = '',
        fans_count: int = 0,
        follow_count: int = 0,
        weibo_count: int = 0,
        bio: str = '',
        verified: bool = False,
        verified_type: str = '',
        location: str = '',
        gender: str = '',
        birthday: str = '',
        register_date: str = '',
        url: str = ''
    ):
        """
        初始化用户信息

        Args:
            user_id: 用户ID
            username: 用户名
            nickname: 昵称
            avatar: 头像URL
            fans_count: 粉丝数
            follow_count: 关注数
            weibo_count: 微博数
            bio: 个人简介
           
        verified: 是否认证
            verified_type: 认证类型
            location: 位置
            gender: 性别
            birthday: 生日
            register_date: 注册日期
            url: 用户主页URL
        """
        self.user_id = user_id
        self.username = username
        self.nickname = nickname
        self.avatar = avatar
        self.fans_count = fans_count
        self.follow_count = follow_count
        self.weibo_count = weibo_count
        self.bio = bio
        self.verified = verified
        self.verified_type = verified_type
        self.location = location
        self.gender = gender
        self.birthday = birthday
        self.register_date = register_date
        self.url = url
        self.crawled_at = datetime.now().isoformat()

    @classmethod
    def from_dict(cls, data: Dict) -> 'WeiboUser':
        """从字典创建用户对象"""
        return cls(
            user_id=data.get('user_id', ''),
            username=data.get('username', ''),
            nickname=data.get('nickname', ''),
            avatar=data.get('avatar', ''),
            fans_count=data.get('fans_count', 0),
            follow_count=data.get('follow_count', 0),
            weibo_count=data.get('weibo_count', 0),
            bio=data.get('bio', ''),
            verified=data.get('verified', False),
            verified_type=data.get('verified_type', ''),
            location=data.get('location', ''),
            gender=data.get('gender', ''),
            birthday=data.get('birthday', ''),
            register_date=data.get('register_date', ''),
            url=data.get('url', '')
        )

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'fans_count': self.fans_count,
            'follow_count': self.follow_count,
            'weibo_count': self.weibo_count,
            'bio': self.bio,
            'verified': self.verified,
            'verified_type': self.verified_type,
            'location': self.location,
            'gender': self.gender,
            'birthday': self.birthday,
            'register_date': self.register_date,
            'url': self.url,
            'crawled_at': self.crawled_at
        }

    def __repr__(self) -> str:
        return f"WeiboUser(username='{self.username}', fans={self.fans_count}, weibos={self.weibo_count})"
