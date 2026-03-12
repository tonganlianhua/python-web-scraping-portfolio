# -*- coding: utf-8 -*-
"""
知乎爬虫核心模块
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import os

from config import (
    ZHIHU_BASE_URL,
    ZHIHU_API_URL,
    DEFAULT_HEADERS,
    MAX_RETRIES,
    REQUEST_TIMEOUT,
    get_headers,
    random_delay,
)


class ZhihuScraper:
    """知乎爬虫类"""

    def __init__(self):
        self.session = requests.Session()
        self.proxies = None

    def set_proxy(self, proxy: Optional[str] = None):
        """设置代理"""
        if proxy:
            self.proxies = {
                'http': proxy,
                'https': proxy
            }
        else:
            self.proxies = None

    def _request(self, url: str, method: str = 'GET', params: Optional[Dict] = None,
                 data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Optional[requests.Response]:
        """
        发送HTTP请求，带重试和反爬策略

        Args:
            url: 请求URL
            method: 请求方法 (GET/POST)
            params: URL参数
            data: POST数据
            headers: 额外请求头

        Returns:
            Response对象或None
        """
        request_headers = get_headers()
        if headers:
            request_headers.update(headers)

        for attempt in range(MAX_RETRIES):
            try:
                # 随机延迟
                random_delay()

                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    headers=request_headers,
                    proxies=self.proxies,
                    timeout=REQUEST_TIMEOUT
                )

                # 检查响应状态
                if response.status_code == 200:
                    return response
                elif response.status_code == 403:
                    print(f"警告: 请求被禁止，可能需要登录或更换IP ({url})")
                    return None
                elif response.status_code == 404:
                    print(f"警告: 页面不存在 ({url})")
                    return None
                else:
                    print(f"警告: 请求失败，状态码: {response.status_code} (尝试 {attempt + 1}/{MAX_RETRIES})")

            except requests.exceptions.RequestException as e:
                print(f"错误: 请求异常 ({url}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)  # 指数退避

        return None

    def search_questions(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        搜索知乎问题

        Args:
            keyword: 搜索关键词
            limit: 返回结果数量限制

        Returns:
            问题列表
        """
        search_url = f"{ZHIHU_API_URL}/search_v3"
        params = {
            'q': keyword,
            'gk': '',
            'type': 'content',
            'search_hash_id': '',
        }

        response = self._request(search_url, params=params)
        if not response:
            return []

        try:
            data = response.json()
            questions = []

            if 'data' in data:
                for item in data['data']:
                    if item.get('type') == 'search_result':
                        obj = item.get('object', {})
                        if obj.get('type') == 'answer':
                            question = obj.get('question', {})
                            if question:
                                questions.append({
                                    'question_id': question.get('id'),
                                    'title': question.get('title', ''),
                                    'url': f"{ZHIHU_BASE_URL}/question/{question.get('id')}",
                                })
                                if len(questions) >= limit:
                                    break

            return questions

        except json.JSONDecodeError as e:
            print(f"错误: 解析搜索结果失败: {e}")
            return []

    def get_topic_questions(self, topic_id: str, limit: int = 10) -> List[Dict]:
        """
        获取话题下的热门问题

        Args:
            topic_id: 话题ID (如 '19556668' for '技术')
            limit: 返回结果数量限制

        Returns:
            问题列表
        """
        # 获取话题基本信息
        topic_url = f"{ZHIHU_API_URL}/topics/{topic_id}"
        response = self._request(topic_url)
        if not response:
            return []

        try:
            topic_data = response.json()
            topic_name = topic_data.get('name', '')

            # 获取热门问题
            feed_url = f"{ZHIHU_API_URL}/topics/{topic_id}/feeds/essence"
            params = {
                'page_size': limit,
                'session_id': '',
            }

            response = self._request(feed_url, params=params)
            if not response:
                return []

            feed_data = response.json()
            questions = []

            if 'data' in feed_data:
                for item in feed_data['data']:
                    if item.get('target', {}).get('type') == 'answer':
                        question = item['target'].get('question', {})
                        if question:
                            questions.append({
                                'question_id': question.get('id'),
                                'title': question.get('title', ''),
                                'topic': topic_name,
                                'url': f"{ZHIHU_BASE_URL}/question/{question.get('id')}",
                            })

            return questions

        except (json.JSONDecodeError, KeyError) as e:
            print(f"错误: 解析话题数据失败: {e}")
            return []

    def get_question_detail(self, question_id: str) -> Optional[Dict]:
        """
        获取问题详情

        Args:
            question_id: 问题ID

        Returns:
            问题详情字典
        """
        detail_url = f"{ZHIHU_API_URL}/questions/{question_id}"
        params = {
            'include': 'data[*].comment_count,voteup_count,created_time,excerpt,author,answer_count,followers_count,visited_count,answer_extra_info'
        }

        response = self._request(detail_url, params=params)
        if not response:
            return None

        try:
            data = response.json()

            # 提取作者信息
            author = data.get('author', {})
            author_info = {
                'id': author.get('id'),
                'name': author.get('name', '匿名用户'),
                'url_token': author.get('url_token', ''),
            }

            # 转换时间戳
            created_time = data.get('created_time')
            if created_time:
                created_date = datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')
            else:
                created_date = ''

            question_detail = {
                'question_id': question_id,
                'title': data.get('title', ''),
                'author': author_info['name'],
                'author_id': author_info['id'],
                'description': data.get('detail', '').strip(),
                'answer_count': data.get('answer_count', 0),
                'follower_count': data.get('followers_count', 0),
                'visited_count': data.get('visited_count', 0),
                'created_time': created_date,
                'url': f"{ZHIHU_BASE_URL}/question/{question_id}",
            }

            return question_detail

        except (json.JSONDecodeError, KeyError) as e:
            print(f"错误: 解析问题详情失败: {e}")
            return None

    def get_question_answers(self, question_id: str, limit: int = 20,
                            offset: int = 0, sort: str = 'default') -> List[Dict]:
        """
        获取问题的回答

        Args:
            question_id: 问题ID
            limit: 每页回答数量
            offset: 偏移量（用于分页）
            sort: 排序方式 ('default' | 'voteup' | 'created')

        Returns:
            回答列表
        """
        answers_url = f"{ZHIHU_API_URL}/questions/{question_id}/answers"
        params = {
            'include': 'data[*].comment_count,voteup_count,created_time,excerpt,author,content',
            'limit': limit,
            'offset': offset,
            'order': sort,
        }

        response = self._request(answers_url, params=params)
        if not response:
            return []

        try:
            data = response.json()
            answers = []

            if 'data' in data:
                for answer in data['data']:
                    author = answer.get('author', {})

                    # 提取回答内容（去除HTML标签）
                    content = answer.get('content', '')
                    # 提取纯文本（简化处理）
                    content_text = re.sub('<[^<]+?>', '', content)
                    content_text = content_text.strip()[:500]  # 限制长度

                    # 转换时间戳
                    created_time = answer.get('created_time')
                    if created_time:
                        created_date = datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        created_date = ''

                    answer_info = {
                        'answer_id': answer.get('id'),
                        'question_id': question_id,
                        'author': author.get('name', '匿名用户'),
                        'author_id': author.get('id'),
                        'content': content_text,
                        'excerpt': answer.get('excerpt', ''),
                        'voteup_count': answer.get('voteup_count', 0),
                        'comment_count': answer.get('comment_count', 0),
                        'created_time': created_date,
                        'url': f"{ZHIHU_BASE_URL}/answer/{answer.get('id')}",
                    }

                    answers.append(answer_info)

            return answers

        except (json.JSONDecodeError, KeyError) as e:
            print(f"错误: 解析回答数据失败: {e}")
            return []

    def get_all_answers(self, question_id: str, max_answers: int = 100,
                       sort: str = 'default') -> List[Dict]:
        """
        获取问题的所有回答（分页获取）

        Args:
            question_id: 问题ID
            max_answers: 最大回答数量
            sort: 排序方式

        Returns:
            所有回答列表
        """
        all_answers = []
        offset = 0
        page_size = 20

        while len(all_answers) < max_answers:
            answers = self.get_question_answers(
                question_id=question_id,
                limit=page_size,
                offset=offset,
                sort=sort
            )

            if not answers:
                break

            all_answers.extend(answers)
            offset += page_size

            # 如果返回的回答少于请求的数量，说明已经获取完所有回答
            if len(answers) < page_size:
                break

        return all_answers[:max_answers]

    def close(self):
        """关闭会话"""
        self.session.close()


# 常用话题ID映射
TOPIC_IDS = {
    '技术': '19556668',
    '编程': '19554544',
    '互联网': '19550529',
    '生活': '19551513',
    '健康': '19555556',
    '美食': '19551464',
    '娱乐': '19551264',
    '电影': '19552498',
    '音乐': '19552476',
    '旅游': '19551501',
    '财经': '19550533',
    '教育': '19551118',
}
