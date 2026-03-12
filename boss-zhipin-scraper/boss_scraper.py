"""
Boss直聘职位爬虫
支持关键词搜索、城市筛选、薪资范围筛选、分页获取等功能
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
import pandas as pd
from fake_useragent import UserAgent
from typing import List, Dict, Optional
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BossZhipinScraper:
    """Boss直聘职位爬虫类"""

    def __init__(self):
        """初始化爬虫"""
        self.ua = UserAgent()
        self.session = requests.Session()
        self.base_url = "https://www.zhipin.com"
        self.job_list_url = f"{self.base_url}/web/geek/job"
        
        # 城市代码映射
        self.city_codes = {
            "全国": "100010000",
            "北京": "101010100",
            "上海": "101020100",
            "广州": "101280100",
            "深圳": "101290100",
            "杭州": "101210100",
            "成都": "101270100",
            "南京": "101190100",
            "武汉": "101200100",
            "西安": "101110100",
            "苏州": "101190200",
            "重庆": "101040100",
            "天津": "101030100",
            "长沙": "101250100",
            "郑州": "101180100",
            "东莞": "101280600",
            "青岛": "101120100",
            "沈阳": "101230100",
            "大连": "101230200",
            "厦门": "101210200",
            "合肥": "101220100",
        }

        # 薪资范围映射
        self.salary_ranges = {
            "不限": None,
            "3K以下": "0,3",
            "3-5K": "3,5",
            "5-10K": "5,10",
            "10-15K": "10,15",
            "15-20K": "15,20",
            "20-30K": "20,30",
            "30-50K": "30,50",
            "50K以上": "50,0",
        }

        # 请求头模板
        self.headers_template = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': self.base_url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

    def _get_random_delay(self, min_delay: float = 1.0, max_delay: float = 3.0) -> float:
        """
        获取随机延时时间

        Args:
            min_delay: 最小延时（秒）
            max_delay: 最大延时（秒）

        Returns:
            随机延时时间（秒）
        """
        return random.uniform(min_delay, max_delay)

    def _get_random_headers(self) -> Dict[str, str]:
        """
        获取随机请求头

        Returns:
            包含随机User-Agent的请求头字典
        """
        headers = self.headers_template.copy()
        headers['User-Agent'] = self.ua.random
        return headers

    def _get_cookie(self, city_code: str) -> str:
        """
        生成 Cookie

        Args:
            city_code: 城市代码

        Returns:
            Cookie 字符串
        """
        last_city = city_code
        return f"lastCity={last_city}; __zp_stoken__=;"

    def search_jobs(
        self,
        keyword: str,
        city: str = "全国",
        salary: str = "不限",
        page: int = 1,
        per_page: int = 30
    ) -> List[Dict]:
        """
        搜索职位

        Args:
            keyword: 搜索关键词
            city: 城市（默认"全国"）
            salary: 薪资范围（默认"不限"）
            page: 页码（默认1）
            per_page: 每页数量（默认30）

        Returns:
            职位信息列表
        """
        # 检查城市
        if city not in self.city_codes:
            logger.warning(f"城市 '{city}' 不支持，使用默认值 '全国'")
            city = "全国"

        # 检查薪资范围
        if salary not in self.salary_ranges:
            logger.warning(f"薪资范围 '{salary}' 不支持，使用默认值 '不限'")
            salary = "不限"

        city_code = self.city_codes[city]
        salary_range = self.salary_ranges[salary]

        # 构建请求参数
        params = {
            "query": keyword,
            "city": city_code,
            "page": page,
            "pageSize": per_page,
        }

        if salary_range:
            params["salary"] = salary_range

        # 构建请求头和Cookie
        headers = self._get_random_headers()
        cookie = self._get_cookie(city_code)
        headers['Cookie'] = cookie

        try:
            # 发送请求
            logger.info(f"正在搜索: 关键词='{keyword}', 城市={city}, 薪资={salary}, 页码={page}")
            response = self.session.get(
                self.job_list_url,
                params=params,
                headers=headers,
                timeout=10
            )

            # 检查响应状态
            if response.status_code != 200:
                logger.error(f"请求失败，状态码: {response.status_code}")
                return []

            # 解析响应（Boss直聘返回HTML，需要从script标签中提取数据）
            return self._parse_job_list(response.text)

        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {e}")
            return []
        except Exception as e:
            logger.error(f"解析异常: {e}")
            return []

    def _parse_job_list(self, html_content: str) -> List[Dict]:
        """
        解析职位列表HTML

        Args:
            html_content: HTML内容

        Returns:
            职位信息列表
        """
        jobs = []

        try:
            soup = BeautifulSoup(html_content, 'lxml')

            # 查找包含职位数据的script标签
            script_tags = soup.find_all('script')
            
            for script in script_tags:
                if script.string and '__INITIAL_STATE__' in script.string:
                    # 提取JSON数据
                    json_str = script.string
                    start_idx = json_str.find('__INITIAL_STATE__') + len('__INITIAL_STATE__')
                    json_str = json_str[start_idx:].strip().lstrip('=').strip()

                    # 解析JSON
                    try:
                        data = json.loads(json_str)
                        jobs = self._extract_jobs_from_data(data)
                        break
                    except json.JSONDecodeError:
                        continue

            # 如果没有找到数据，尝试解析HTML结构
            if not jobs:
                jobs = self._parse_job_list_from_html(soup)

            logger.info(f"成功解析 {len(jobs)} 个职位")
            return jobs

        except Exception as e:
            logger.error(f"解析HTML失败: {e}")
            return []

    def _extract_jobs_from_data(self, data: dict) -> List[Dict]:
        """
        从JSON数据中提取职位信息

        Args:
            data: JSON数据字典

        Returns:
            职位信息列表
        """
        jobs = []

        try:
            # Boss直聘的数据结构可能在不同的层级
            # 尝试多种路径
            job_list = None

            # 尝试路径1
            if 'jobList' in data:
                job_list = data['jobList']
            # 尝试路径2
            elif 'jobList' in str(data):
                # 递归查找
                def find_job_list(obj):
                    if isinstance(obj, dict):
                        if 'jobList' in obj and isinstance(obj['jobList'], list):
                            return obj['jobList']
                        for v in obj.values():
                            result = find_job_list(v)
                            if result:
                                return result
                    elif isinstance(obj, list):
                        for item in obj:
                            result = find_job_list(item)
                            if result:
                                return result
                    return None

                job_list = find_job_list(data)

            if job_list:
                for job in job_list:
                    jobs.append(self._parse_single_job(job))

        except Exception as e:
            logger.error(f"提取职位数据失败: {e}")

        return jobs

    def _parse_job_list_from_html(self, soup: BeautifulSoup) -> List[Dict]:
        """
        从HTML结构中解析职位列表

        Args:
            soup: BeautifulSoup对象

        Returns:
            职位信息列表
        """
        jobs = []

        try:
            # 查找职位卡片
            job_cards = soup.find_all('div', class_='job-card-wrapper')

            for card in job_cards:
                try:
                    job = {}

                    # 职位名称和链接
                    title_elem = card.find('span', class_='job-name')
                    if title_elem:
                        job['职位名称'] = title_elem.get_text(strip=True)

                    # 薪资
                    salary_elem = card.find('span', class_='salary')
                    if salary_elem:
                        job['薪资'] = salary_elem.get_text(strip=True)

                    # 公司名称
                    company_elem = card.find('span', class_='company-name')
                    if company_elem:
                        job['公司'] = company_elem.get_text(strip=True)

                    # 地点
                    location_elem = card.find('span', class_='job-area')
                    if location_elem:
                        job['地点'] = location_elem.get_text(strip=True)

                    # 经验要求
                    exp_elem = card.find('span', class_='job-limit')
                    if exp_elem:
                        job['经验要求'] = exp_elem.get_text(strip=True)

                    # 学历要求
                    edu_elem = card.find('span', class_='job-limit')
                    if edu_elem:
                        text = edu_elem.get_text(strip=True)
                        if '经验' in text:
                            parts = text.split('|')
                            if len(parts) > 1:
                                job['学历要求'] = parts[1].strip()

                    # 职位标签
                    tags = []
                    tag_elems = card.find_all('span', class_='tag-item')
                    for tag_elem in tag_elems:
                        tags.append(tag_elem.get_text(strip=True))
                    job['职位标签'] = '|'.join(tags) if tags else ''

                    # 职位链接
                    link_elem = card.find('a')
                    if link_elem:
                        job['职位链接'] = self.base_url + link_elem.get('href', '')
                    else:
                        job['职位链接'] = ''

                    # 添加爬取时间
                    job['爬取时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    jobs.append(job)

                except Exception as e:
                    logger.error(f"解析单个职位失败: {e}")
                    continue

        except Exception as e:
            logger.error(f"解析HTML职位列表失败: {e}")

        return jobs

    def _parse_single_job(self, job_data: dict) -> Dict:
        """
        解析单个职位数据

        Args:
            job_data: 职位数据字典

        Returns:
            解析后的职位信息字典
        """
        job = {}

        try:
            # 根据Boss直聘API返回的数据结构解析
            job['职位名称'] = job_data.get('jobName', job_data.get('title', ''))
            job['薪资'] = job_data.get('salaryDesc', job_data.get('salary', ''))
            job['公司'] = job_data.get('brandName', job_data.get('company', ''))
            job['地点'] = job_data.get('cityDistrict', job_data.get('location', ''))
            job['经验要求'] = job_data.get('workYearDesc', job_data.get('experience', ''))
            job['学历要求'] = job_data.get('eduDegreeDesc', job_data.get('education', ''))

            # 职位标签
            tags = job_data.get('skills', job_data.get('tags', []))
            if isinstance(tags, list):
                job['职位标签'] = '|'.join(tags)
            else:
                job['职位标签'] = str(tags)

            # 职位链接
            job_id = job_data.get('encryptJobId', job_data.get('jobId', ''))
            job['职位链接'] = f"{self.base_url}/job_detail/?jobId={job_id}" if job_id else ''

            # 添加爬取时间
            job['爬取时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        except Exception as e:
            logger.error(f"解析单个职位数据失败: {e}")

        return job

    def scrape_jobs(
        self,
        keyword: str,
        city: str = "全国",
        salary: str = "不限",
        max_pages: int = 5,
        delay: tuple = (1.0, 3.0)
    ) -> List[Dict]:
        """
        爬取多页职位信息

        Args:
            keyword: 搜索关键词
            city: 城市（默认"全国"）
            salary: 薪资范围（默认"不限"）
            max_pages: 最大页数（默认5）
            delay: 延时范围（秒）（默认(1.0, 3.0)）

        Returns:
            所有职位信息列表
        """
        all_jobs = []

        logger.info(f"开始爬取: 关键词='{keyword}', 城市={city}, 薪资={salary}, 最大页数={max_pages}")

        for page in range(1, max_pages + 1):
            # 搜索职位
            jobs = self.search_jobs(keyword, city, salary, page)

            if not jobs:
                logger.info(f"第 {page} 页没有数据，停止爬取")
                break

            all_jobs.extend(jobs)

            # 随机延时，避免被封
            if page < max_pages:
                delay_time = self._get_random_delay(delay[0], delay[1])
                logger.info(f"等待 {delay_time:.2f} 秒后继续...")
                time.sleep(delay_time)

        logger.info(f"爬取完成，共获取 {len(all_jobs)} 个职位")
        return all_jobs

    def get_cities(self) -> List[str]:
        """
        获取支持的城市列表

        Returns:
            城市名称列表
        """
        return list(self.city_codes.keys())

    def get_salary_ranges(self) -> List[str]:
        """
        获取支持的薪资范围列表

        Returns:
            薪资范围列表
        """
        return list(self.salary_ranges.keys())


def main():
    """主函数 - 用于测试"""
    scraper = BossZhipinScraper()

    # 打印支持的城市和薪资范围
    print("支持的城市:")
    for city in scraper.get_cities():
        print(f"  - {city}")

    print("\n支持的薪资范围:")
    for salary in scraper.get_salary_ranges():
        print(f"  - {salary}")

    # 爬取职位（示例）
    print("\n开始爬取职位...")
    jobs = scraper.scrape_jobs(
        keyword="Python",
        city="北京",
        salary="15-20K",
        max_pages=2
    )

    if jobs:
        print(f"\n共获取 {len(jobs)} 个职位")
        for i, job in enumerate(jobs[:5], 1):  # 只打印前5个
            print(f"\n职位 {i}:")
            for key, value in job.items():
                print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
