"""
豆瓣电影爬虫 - 主模块
提供爬取 Top250、搜索电影、获取电影详情等功能
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import re
from utils import AntiSpider


class DoubanMovieScraper:
    """豆瓣电影爬虫类"""

    def __init__(self, base_url: str = 'https://movie.douban.com'):
        self.base_url = base_url
        self.session = requests.Session()
        self.top250_url = f'{base_url}/top250'
        self.search_url = f'{base_url}/search'

    def _get_page(self, url: str, params: Optional[Dict] = None, retries: int = 3) -> BeautifulSoup:
        """
        获取网页内容

        Args:
            url: 请求 URL
            params: 查询参数
            retries: 重试次数

        Returns:
            BeautifulSoup 解析后的对象
        """
        headers = AntiSpider.get_headers()

        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params, headers=headers, timeout=10)
                response.raise_for_status()

                # 检查是否被反爬
                if response.status_code == 403:
                    print(f"⚠ 被反爬虫检测到，第 {attempt + 1} 次重试...")
                    AntiSpider.random_delay(2, 5)
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                return soup

            except requests.RequestException as e:
                print(f"⚠ 请求失败（第 {attempt + 1} 次）: {e}")
                if attempt < retries - 1:
                    AntiSpider.random_delay(1, 3)
                continue

        raise Exception(f"无法获取页面内容: {url}")

    def get_top250(self) -> List[Dict[str, Any]]:
        """
        爬取豆瓣电影 Top250

        Returns:
            电影信息列表
        """
        print("=== 开始爬取豆瓣电影 Top250 ===")
        movies = []

        for start in range(0, 250, 25):
            print(f"正在爬取第 {start // 25 + 1} 页...")
            AntiSpider.random_delay(1, 2)

            params = {'start': start}
            soup = self._get_page(self.top250_url, params=params)

            # 解析电影列表
            movie_list = soup.find('ol', class_='grid_view')
            if not movie_list:
                print(f"⚠ 第 {start // 25 + 1} 页没有找到电影列表")
                continue

            items = movie_list.find_all('li', class_='item')

            for idx, item in enumerate(items):
                rank = start + idx + 1
                movie = self._parse_top250_item(item, rank)
                if movie:
                    movies.append(movie)

            print(f"✓ 第 {start // 25 + 1} 页完成，共 {len(items)} 部电影")

        print(f"=== 爬取完成，共 {len(movies)} 部电影 ===")
        return movies

    def _parse_top250_item(self, item, rank: int) -> Optional[Dict[str, Any]]:
        """
        解析 Top250 电影项

        Args:
            item: BeautifulSoup 元素
            rank: 排名

        Returns:
            电影信息字典
        """
        try:
            # 标题
            title_div = item.find('div', class_='pic')
            title_link = title_div.find('a') if title_div else None
            title = title_link.get('title') if title_link else ''
            movie_id = title_link.get('href').split('/')[-2] if title_link else ''

            # 评分
            rating_div = item.find('div', class_='star')
            rating_span = rating_div.find_all('span') if rating_div else []
            rating = float(rating_span[2].text.strip()) if len(rating_span) > 2 else 0

            # 评价人数
            rating_people_str = rating_span[3].text.strip() if len(rating_span) > 3 else '0人评价'
            rating_people = int(re.sub(r'\D', '', rating_people_str))

            # 信息（年份、导演、主演）
            info_div = item.find('div', class_='bd')
            info_p = info_div.find('p', class_='') if info_div else None
            info_text = info_p.text.strip() if info_p else ''

            # 提取年份
            year_match = re.search(r'(\d{4})', info_text)
            year = int(year_match.group(1)) if year_match else 0

            # 提取导演和主演
            director_match = re.search(r'导演: (.*?)\s+主演:', info_text)
            director_str = director_match.group(1).strip() if director_match else ''
            directors = [d.strip() for d in director_str.split('/') if d.strip()]

            actor_match = re.search(r'主演: (.*?)\s+(\d{4}|$)', info_text)
            actor_str = actor_match.group(1).strip() if actor_match else ''
            actors = [a.strip() for a in actor_str.split('/') if a.strip()]

            # 引用语
            quote_div = item.find('span', class_='inq')
            quote = quote_div.text.strip() if quote_div else ''

            return {
                'rank': rank,
                'title': title,
                'movie_id': movie_id,
                'rating': rating,
                'rating_people': rating_people,
                'year': year,
                'directors': directors,
                'actors': actors,
                'quote': quote,
                'url': f'{self.base_url}/subject/{movie_id}/'
            }

        except Exception as e:
            print(f"⚠ 解析电影项失败: {e}")
            return None

    def search_movies(self, keyword: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        搜索电影

        Args:
            keyword: 搜索关键词
            limit: 返回结果数量限制

        Returns:
            搜索结果列表
        """
        print(f"=== 搜索电影: {keyword} ===")
        AntiSpider.random_delay()

        params = {
            'q': keyword,
            'cat': '1002',  # 电影分类
        }

        soup = self._get_page(self.search_url, params=params)
        results = []

        # 查找搜索结果列表
        result_list = soup.find('div', class_='article')
        if not result_list:
            print("⚠ 没有找到搜索结果")
            return results

        items = result_list.find_all('div', class_='item')

        for idx, item in enumerate(items[:limit]):
            try:
                movie = self._parse_search_item(item)
                if movie:
                    results.append(movie)
            except Exception as e:
                print(f"⚠ 解析搜索结果失败: {e}")
                continue

        print(f"✓ 搜索完成，找到 {len(results)} 部电影")
        return results

    def _parse_search_item(self, item) -> Optional[Dict[str, Any]]:
        """解析搜索结果项"""
        try:
            # 标题和链接
            title_div = item.find('div', class_='title')
            title_link = title_div.find('a') if title_div else None
            title = title_link.text.strip() if title_link else ''
            movie_id = title_link.get('href').split('/')[-2] if title_link else ''

            # 评分
            rating_span = item.find('span', class_='rating_nums')
            rating = float(rating_span.text.strip()) if rating_span else 0

            # 评价人数
            people_span = item.find('span', class_='rating_people')
            people_str = people_span.text.strip() if people_span else '0'
            rating_people = int(re.sub(r'\D', '', people_str))

            # 信息
            info_div = item.find('div', class_='abstract')
            info_text = info_div.text.strip() if info_div else ''

            # 提取年份
            year_match = re.search(r'(\d{4})', info_text)
            year = int(year_match.group(1)) if year_match else 0

            # 提取导演
            director_match = re.search(r'导演:\s*(.*?)(?:主演:|$)', info_text)
            director_str = director_match.group(1).strip() if director_match else ''
            directors = [d.strip() for d in director_str.split('/') if d.strip()]

            return {
                'title': title,
                'movie_id': movie_id,
                'rating': rating,
                'rating_people': rating_people,
                'year': year,
                'directors': directors,
                'info': info_text,
                'url': f'{self.base_url}/subject/{movie_id}/'
            }

        except Exception as e:
            print(f"⚠ 解析搜索项失败: {e}")
            return None

    def get_movie_detail(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """
        获取电影详细信息

        Args:
            movie_id: 电影 ID

        Returns:
            电影详细信息
        """
        print(f"=== 获取电影详情: {movie_id} ===")
        AntiSpider.random_delay()

        url = f'{self.base_url}/subject/{movie_id}/'
        soup = self._get_page(url)

        try:
            # 标题
            title = soup.find('span', property='v:itemreviewed').text.strip()

            # 年份
            year_span = soup.find('span', class_='year')
            year = int(re.sub(r'[()]', '', year_span.text.strip())) if year_span else 0

            # 评分
            rating_span = soup.find('strong', class_='ll rating_num')
            rating = float(rating_span.text.strip()) if rating_span else 0

            # 评价人数
            rating_people_span = soup.find('span', property='v:votes')
            rating_people = int(rating_people_span.text.strip()) if rating_people_span else 0

            # 导演
            directors = []
            director_links = soup.find_all('a', rel='v:directedBy')
            for link in director_links:
                directors.append(link.text.strip())

            # 主演
            actors = []
            actor_links = soup.find_all('a', rel='v:starring')
            for link in actor_links[:5]:  # 只取前5个主演
                actors.append(link.text.strip())

            # 类型/类型
            genres = []
            genre_links = soup.find_all('span', property='v:genre')
            for link in genre_links:
                genres.append(link.text.strip())

            # 剧情简介
            summary_div = soup.find('div', id='link-report')
            summary_div = summary_div.find('div', class_='indent') if summary_div else None
            summary_span = summary_div.find_all('span') if summary_div else []
            summary = summary_span[0].text.strip() if summary_span else ''

            # 一句话评价
            quote_div = soup.find('div', id='interest_sectl')
            rating_people_div = quote_div.find('div', class_='rating_people') if quote_div else None
            quote = rating_people_div.text.strip() if rating_people_div else ''

            # IMDb 链接
            imdb_link = soup.find('a', href=re.compile(r'imdb\.com'))
            imdb_id = imdb_link.get('href').split('/')[-2] if imdb_link else ''

            return {
                'movie_id': movie_id,
                'title': title,
                'year': year,
                'rating': rating,
                'rating_people': rating_people,
                'directors': directors,
                'actors': actors,
                'genres': genres,
                'summary': summary,
                'quote': quote,
                'imdb_id': imdb_id,
                'url': url
            }

        except Exception as e:
            print(f"⚠ 解析电影详情失败: {e}")
            return None

    def get_comments(self, movie_id: str, limit: int = 20, sort: str = 'new_score') -> List[Dict[str, Any]]:
        """
        获取电影评论

        Args:
            movie_id: 电影 ID
            limit: 评论数量
            sort: 排序方式 (new_score=最新, hot=热门)

        Returns:
            评论列表
        """
        print(f"=== 获取电影评论: {movie_id} (最多 {limit} 条) ===")

        comments = []
        start = 0

        while len(comments) < limit:
            AntiSpider.random_delay(1, 2)

            url = f'{self.base_url}/subject/{movie_id}/comments'
            params = {
                'start': start,
                'limit': 20,
                'sort': sort,
                'status': 'P'
            }

            soup = self._get_page(url, params=params)

            # 解析评论列表
            comment_list = soup.find('div', class_='comment-list')
            if not comment_list:
                print(f"⚠ 没有找到更多评论")
                break

            items = comment_list.find_all('div', class_='comment-item')

            if not items:
                print(f"⚠ 没有更多评论")
                break

            for item in items:
                comment = self._parse_comment_item(item)
                if comment:
                    comments.append(comment)
                    if len(comments) >= limit:
                        break

            start += 20

            if len(items) < 20:
                print(f"✓ 已获取所有评论")
                break

        print(f"✓ 评论获取完成，共 {len(comments)} 条")
        return comments

    def _parse_comment_item(self, item) -> Optional[Dict[str, Any]]:
        """解析评论项"""
        try:
            # 用户
            user_span = item.find('span', class_='comment-info')
            user_link = user_span.find('a') if user_span else None
            user = user_link.text.strip() if user_link else ''

            # 评分
            rating_span = user_span.find('span', class_='rating') if user_span else None
            rating_str = rating_span.get('title', '') if rating_span else ''
            rating_map = {
                '力荐': 5, '推荐': 4, '还行': 3, '较差': 2, '很差': 1
            }
            rating = rating_map.get(rating_str, 0)

            # 时间
            time_span = user_span.find('span', class_='comment-time') if user_span else None
            comment_time = time_span.get('title', '') if time_span else ''

            # 内容
            content_div = item.find('span', class_='short')
            content = content_div.text.strip() if content_div else ''

            # 投票
            votes_span = item.find('span', class_='vote-count')
            votes = int(votes_span.text.strip()) if votes_span else 0

            return {
                'user': user,
                'rating': rating,
                'rating_str': rating_str,
                'time': comment_time,
                'content': content,
                'votes': votes
            }

        except Exception as e:
            print(f"⚠ 解析评论项失败: {e}")
            return None

    def close(self):
        """关闭会话"""
        self.session.close()


def main():
    """测试函数"""
    scraper = DoubanMovieScraper()

    try:
        # 爬取 Top250
        movies = scraper.get_top250()
        print(f"\n成功爬取 {len(movies)} 部电影")

        # 打印前5部电影
        print("\n=== Top 5 电影 ===")
        for movie in movies[:5]:
            print(f"{movie['rank']}. {movie['title']} ({movie['year']}) - {movie['rating']}")

    finally:
        scraper.close()


if __name__ == '__main__':
    main()
