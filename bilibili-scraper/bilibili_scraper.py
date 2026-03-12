# -*- coding: utf-8 -*-
"""
B站视频B站爬虫模块
支持获取视频信息、批量处理、搜索、导出和分析
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('bilibili_scraper')


class BiliBiliScraper:
    """B站视频信息爬虫"""

    # User-Agent池
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    ]

    def __init__(self, min_delay: float = 2.0, max_delay: float = 5.0):
        """
        初始化爬虫

        Args:
            min_delay: 最小延时（秒）
            max_delay: 最大延时（秒）
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        logger.info(f"爬虫初始化完成，延时范围：{min_delay}-{max_delay}秒")

    def _get_random_user_agent(self) -> str:
        """获取随机User-Agent"""
        return random.choice(self.USER_AGENTS)

    def _random_delay(self):
        """随机延时"""
        delay = random.uniform(self.min_delay, self.max_delay)
        logger.debug(f"随机延时 {delay:.2f} 秒")
        time.sleep(delay)

    def _extract_bv_code(self, input_str: str) -> Optional[str]:
        """
        从输入字符串中提取BV号

        Args:
            input_str: 视频链接或BV号

        Returns:
            BV号，如果提取失败返回None
        """
        # 如果是BV号
        if input_str.startswith('BV'):
            return input_str

        # 如果是URL，提取BV号（BV号通常是BV后面跟着10个字符）
        bv_match = re.search(r'BV[a-zA-Z0-9]+', input_str)
        if bv_match:
            bv_code = bv_match.group()
            # 确保BV号长度合理（通常12字符：BV + 10字符）
            if len(bv_code) >= 12:
                return bv_code

        logger.warning(f"无法提取BV号: {input_str}")
        return None

    def _make_request(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """
        发送HTTP请求（带重试）

        Args:
            url: 请求URL
            max_retries: 最大重试次数

        Returns:
            响应对象，失败返回None
        """
        self.session.headers['User-Agent'] = self._get_random_user_agent()

        for attempt in range(max_retries):
            try:
                logger.info(f"请求: {url} (尝试 {attempt + 1}/{max_retries})")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.warning(f"请求失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避

        logger.error(f"请求失败，已达最大重试次数: {url}")
        return None

    def get_video_info(self, bv_or_url: str) -> Optional[Dict]:
        """
        获取视频详细信息

        Args:
            bv_or_url: 视频链接或BV号

        Returns:
            视频信息字典，失败返回None
        """
        bv_code = self._extract_bv_code(bv_or_url)
        if not bv_code:
            return None

        url = f"https://www.bilibili.com/video/{bv_code}"

        response = self._make_request(url)
        if not response:
            return None

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 尝试从HTML中提取视频信息
        try:
            video_info = self._extract_from_html(soup, bv_code, url)
            if video_info:
                logger.info(f"成功获取视频信息: {video_info.get('title', 'N/A')}")
                return video_info
        except Exception as e:
            logger.warning(f"从HTML提取失败: {e}")

        # 尝试从页面中的JSON数据提取
        try:
            video_info = self._extract_from_json(soup, bv_code, url)
            if video_info:
                logger.info(f"成功获取视频信息: {video_info.get('title', 'N/A')}")
                return video_info
        except Exception as e:
            logger.error(f"从JSON提取失败: {e}")

        logger.error(f"获取视频信息失败: {bv_code}")
        return None

    def _extract_from_html(self, soup: BeautifulSoup, bv_code: str, url: str) -> Optional[Dict]:
        """从HTML中提取视频信息"""
        video_info = {
            'bv': bv_code,
            'url': url,
            'title': None,
            'author': None,
            'author_id': None,
            'views': 0,
            'likes': 0,
            'coins': 0,
            'favorites': 0,
            'shares': 0,
            'duration': None,
            'publish_time': None,
        }

        # 提取标题
        title_tag = soup.find('meta', property='og:title')
        if title_tag:
            video_info['title'] = title_tag.get('content', '').strip()

        # 提取作者
        author_tag = soup.find('meta', itemprop='author')
        if author_tag:
            video_info['author'] = author_tag.get('content', '').strip()

        # 提取作者ID
        author_id_match = re.search(r'"mid":(\d+)', str(soup))
        if author_id_match:
            video_info['author_id'] = author_id_match.group(1)

        # 提取统计数据（从script标签中的JSON）
        scripts = soup.find_all('script')
        for script in scripts:
            script_text = script.string
            if script_text and 'stat' in script_text:
                try:
                    # 查找stat对象
                    stat_match = re.search(r'"stat":\{[^}]+\}', script_text)
                    if stat_match:
                        stat_str = stat_match.group()
                        stat_str = stat_str.replace('"stat":', '')
                        stat_data = json.loads('{' + stat_str + '}')
                        video_info['views'] = stat_data.get('view', 0)
                        video_info['likes'] = stat_data.get('like', 0)
                        video_info['coins'] = stat_data.get('coin', 0)
                        video_info['favorites'] = stat_data.get('favorite', 0)
                        video_info['shares'] = stat_data.get('share', 0)
                        break
                except Exception as e:
                    logger.debug(f"解析stat失败: {e}")

        # 提取时长
        duration_tag = soup.find('meta', itemprop='duration')
        if duration_tag:
            video_info['duration'] = duration_tag.get('content', '').strip()

        # 提取发布时间
        publish_tag = soup.find('meta', itemprop='uploadDate')
        if publish_tag:
            video_info['publish_time'] = publish_tag.get('content', '').strip()

        # 如果至少有标题，返回结果
        if video_info['title']:
            return video_info

        return None

    def _extract_from_json(self, soup: BeautifulSoup, bv_code: str, url: str) -> Optional[Dict]:
        """从页面中的JSON数据提取视频信息"""
        # 查找包含视频数据的script标签
        scripts = soup.find_all('script')
        for script in scripts:
            script_text = script.string
            if script_text and 'videoData' in script_text:
                try:
                    # 提取JSON数据
                    match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.+?});', script_text)
                    if not match:
                        continue

                    json_str = match.group(1)
                    data = json.loads(json_str)

                    # 提取视频信息
                    video_data = data.get('videoData', {})
                    if not video_data:
                        continue

                    video_info = {
                        'bv': bv_code,
                        'url': url,
                        'title': video_data.get('title', ''),
                        'author': '',
                        'author_id': '',
                        'views': 0,
                        'likes': 0,
                        'coins': 0,
                        'favorites': 0,
                        'shares': 0,
                        'duration': '',
                        'publish_time': '',
                    }

                    # 提取作者信息
                    owner = video_data.get('owner', {})
                    if owner:
                        video_info['author'] = owner.get('name', '')
                        video_info['author_id'] = owner.get('mid', '')

                    # 提取统计信息
                    stat = video_data.get('stat', {})
                    if stat:
                        video_info['views'] = stat.get('view', 0)
                        video_info['likes'] = stat.get('like', 0)
                        video_info['coins'] = stat.get('coin', 0)
                        video_info['favorites'] = stat.get('favorite', 0)
                        video_info['shares'] = stat.get('share', 0)

                    # 提取时长
                    pages = video_data.get('pages', [])
                    if pages:
                        video_info['duration'] = str(pages[0].get('duration', ''))

                    # 提取发布时间
                    video_info['publish_time'] = str(video_data.get('pubdate', ''))

                    return video_info

                except Exception as e:
                    logger.debug(f"解析JSON失败: {e}")

        return None

    def batch_get_videos(self, video_list: List[str]) -> List[Dict]:
        """
        批量获取视频信息

        Args:
            video_list: 视频链接或BV号列表

        Returns:
            视频信息列表
        """
        logger.info(f"开始批量获取 {len(video_list)} 个视频信息")
        results = []

        for i, video in enumerate(video_list, 1):
            logger.info(f"处理第 {i}/{len(video_list)} 个视频: {video}")
            video_info = self.get_video_info(video)
            if video_info:
                results.append(video_info)
            else:
                logger.warning(f"获取失败: {video}")

            # 随机延时
            self._random_delay()

        logger.info(f"批量获取完成，成功获取 {len(results)} 个视频信息")
        return results

    def search_videos(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """
        搜索视频

        Args:
            keyword: 搜索关键词
            max_results: 最大结果数量

        Returns:
            视频信息列表
        """
        logger.info(f"搜索关键词: {keyword} (最多 {max_results} 个结果)")
        results = []

        # 构建搜索URL
        search_url = f"https://search.bilibili.com/all?keyword={keyword}"

        response = self._make_request(search_url)
        if not response:
            return results

        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找视频卡片
        video_items = soup.find_all('div', class_='bili-video-card')
        if not video_items:
            logger.warning("未找到搜索结果")
            return results

        for item in video_items[:max_results]:
            try:
                # 提取BV号
                link = item.find('a', href=re.compile)
                if not link:
                    continue

                href = link.get('href', '')
                bv_match = re.search(r'BV[a-zA-Z0-9]{10}', href)
                if not bv_match:
                    continue

                bv_code = bv_match.group()
                logger.info(f"从搜索结果获取视频: {bv_code}")

                # 获取详细信息
                video_info = self.get_video_info(bv_code)
                if video_info:
                    results.append(video_info)

                # 随机延时
                self._random_delay()

            except Exception as e:
                logger.warning(f"处理搜索结果失败: {e}")

        logger.info(f"搜索完成，获取 {len(results)} 个视频")
        return results

    def export_to_csv(self, data: List[Dict], filename: str = 'videos.csv'):
        """
        导出数据到CSV文件

        Args:
            data: 视频信息列表
            filename: 输出文件名
        """
        if not data:
            logger.warning("没有数据可导出")
            return

        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logger.info(f"数据已导出到: {filename}")

    def generate_report(self, data: List[Dict], filename: str = 'report.html'):
        """
        生成HTML数据分析报告

        Args:
            data: 视频信息列表
            filename: 输出文件名
        """
        if not data:
            logger.warning("没有数据可分析")
            return

        logger.info(f"生成分析报告: {filename}")

        # 转换为DataFrame
        df = pd.DataFrame(data)

        # 基本统计
        total_videos = len(df)
        total_views = df['views'].sum()
        avg_views = df['views'].mean()
        max_views = df['views'].max()
        total_likes = df['likes'].sum()
        total_coins = df['coins'].sum()

        # 作者排行
        author_stats = df.groupby('author').agg({
            'views': 'sum',
            'likes': 'sum',
            'bv': 'count'
        }).rename(columns={'bv': 'video_count'}).sort_values('views', ascending=False).head(10)

        # 播放量分布
        view_ranges = pd.cut(df['views'], bins=[0, 10000, 100000, 1000000, float('inf')],
                            labels=['<1万', '1-10万', '10-100万', '>100万'])
        view_distribution = view_ranges.value_counts().sort_index()

        # 生成HTML报告
        html = self._generate_html_report(
            total_videos, total_views, avg_views, max_views,
            total_likes, total_coins, author_stats, view_distribution, df
        )

        # 保存报告
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        logger.info(f"分析报告已生成: {filename}")

    def _generate_html_report(self, total_videos, total_views, avg_views, max_views,
                               total_likes, total_coins, author_stats, view_distribution, df):
        """生成HTML报告内容"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>B站视频数据分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #00a1d6, #20b2aa); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .header h1 {{ font-size: 32px; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .card {{ background: white; border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .card h2 {{ color: #00a1d6; margin-bottom: 20px; font-size: 24px; border-bottom: 2px solid #00a1d6; padding-bottom: 10px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
        .stat-item {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-value {{ font-size: 28px; font-weight: bold; color: #00a1d6; margin-bottom: 5px; }}
        .stat-label {{ color: #666; font-size: 14px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #f8f9fa; color: #00a1d6; font-weight: bold; }}
        tr:hover {{ background: #f0f7fa; }}
        .bar {{ background: #00a1d6; height: 20px; border-radius: 10px; margin: 5px 0; }}
        .progress {{ width: 100%; background: #e0e0e0; border-radius: 10px; overflow: hidden; }}
        .progress-bar {{ background: linear-gradient(90deg, #00a1d6, #20b2aa); height: 100%; border-radius: 10px; }}
        .footer {{ text-align: center; color: #999; margin-top: 30px; padding: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 B站视频数据分析报告</h1>
            <p>生成时间: {now}</p>
        </div>

        <div class="card">
            <h2>📈 总体统计</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{total_videos}</div>
                    <div class="stat-label">视频总数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{total_views:,}</div>
                    <div class="stat-label">总播放量</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{avg_views:,.0f}</div>
                    <div class="stat-label">平均播放量</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{max_views:,}</div>
                    <div class="stat-label">最高播放量</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{total_likes:,}</div>
                    <div class="stat-label">总点赞数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{total_coins:,}</div>
                    <div class="stat-label">总投币数</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>👑 作者排行榜（Top 10）</h2>
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>作者</th>
                        <th>视频数</th>
                        <th>总播放量</th>
                        <th>总点赞数</th>
                    </tr>
                </thead>
                <tbody>
"""

        for idx, (author, row) in enumerate(author_stats.iterrows(), 1):
            html += f"""                    <tr>
                        <td>{idx}</td>
                        <td>{author}</td>
                        <td>{int(row['video_count'])}</td>
                        <td>{int(row['views']):,}</td>
                        <td>{int(row['likes']):,}</td>
                    </tr>
"""

        html += """                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>📊 播放量分布</h2>
"""

        max_count = view_distribution.max() if len(view_distribution) > 0 else 1

        for range_name, count in view_distribution.items():
            percentage = (count / max_count) * 100
            html += f"""            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>{range_name}</span>
                    <span>{count} 个视频</span>
                </div>
                <div class="progress">
                    <div class="progress-bar" style="width: {percentage}%"></div>
                </div>
            </div>
"""

        html += """        </div>

        <div class="card">
            <h2>🎬 视频列表</h2>
            <table>
                <thead>
                    <tr>
                        <th>标题</th>
                        <th>作者</th>
                        <th>播放量</th>
                        <th>点赞</th>
                        <th>投币</th>
                        <th>收藏</th>
                    </tr>
                </thead>
                <tbody>
"""

        for _, row in df.iterrows():
            html += f"""                    <tr>
                        <td><a href="{row['url']}" target="_blank">{row['title']}</a></td>
                        <td>{row['author']}</td>
                        <td>{row['views']:,}</td>
                        <td>{row['likes']:,}</td>
                        <td>{row['coins']:,}</td>
                        <td>{row['favorites']:,}</td>
                    </tr>
"""

        html += """                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>报告由 B站视频爬虫生成 | Made with ❤️</p>
        </div>
    </div>
</body>
</html>"""

        return html

    def close(self):
        """关闭会话"""
        self.session.close()
        logger.info("爬虫会话已关闭")

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理器"""
        self.close()
        return False


if __name__ == '__main__':
    # 示例用法
    scraper = BiliBiliScraper()

    # 获取单个视频信息
    print("=== 获取单个视频信息 ===")
    video_info = scraper.get_video_info('BV1xx411c7mD')
    if video_info:
        print(json.dumps(video_info, ensure_ascii=False, indent=2))

    # 批量获取
    print("\n=== 批量获取视频信息 ===")
    video_list = ['BV1xx411c7mD', 'BV1y44y1K7KL']
    results = scraper.batch_get_videos(video_list)
    print(f"成功获取 {len(results)} 个视频信息")

    # 关闭会话
    scraper.close()
