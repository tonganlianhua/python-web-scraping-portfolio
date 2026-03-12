"""
淘宝商品爬虫核心模块
提供商品搜索、分类筛选、价格筛选、排序等功能
"""

import re
import json
from typing import List, Dict, Optional, Tuple, Any
from bs4 import BeautifulSoup
from bs4.element import Tag
from .anti_spider import AntiSpiderMiddleware


class TaobaoScraper:
    """淘宝商品爬虫类"""

    # 分类映射
    CATEGORIES = {
        'all': '全部',
        'clothing': '服装',
        'digital': '数码',
        'home_appliance': '家电',
        'beauty': '美妆',
        'food': '食品',
        'sports': '运动',
        'books': '图书',
    }

    # 排序参数映射
    SORT_PARAMS = {
        'sales': 'sale-desc',      # 销量降序
        'price_asc': 'price-asc',  # 价格升序
        'price_desc': 'price-desc', # 价格降序
    }

    def __init__(
        self,
        delay_range: Tuple[float, float] = (2, 4),
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        初始化淘宝爬虫

        Args:
            delay_range: 请求延时范围（秒），默认 (2, 4)
            max_retries: 最大重试次数，默认 3
            timeout: 请求超时时间（秒），默认 30
        """
        self.anti_spider = AntiSpiderMiddleware(
            delay_range=delay_range,
            max_retries=max_retries,
            timeout=timeout
        )

    def search(
        self,
        keyword: str,
        category: Optional[str] = None,
        price_range: Optional[Tuple[float, float]] = None,
        sort_by: str = 'sales',
        sort_order: str = 'desc',
        page_num: int = 1,
        page_size: int = 20
    ) -> List[Dict]:
        """
        搜索商品

        Args:
            keyword: 搜索关键词
            category: 商品分类（可选）
            price_range: 价格区间，格式 (min_price, max_price)
            sort_by: 排序方式，'sales' 或 'price'
            sort_order: 排序顺序，'asc' 或 'desc'
            page_num: 页码，从 1 开始
            page_size: 每页数量

        Returns:
            List[Dict]: 商品列表
        """
        # 构建 URL
        url = self._build_search_url(
            keyword=keyword,
            category=category,
            price_range=price_range,
            sort_by=sort_by,
            sort_order=sort_order,
            page_num=page_num
        )

        # 发起请求
        try:
            response = self.anti_spider.get(url)
            html = response.text

            # 解析商品数据
            products = self._parse_products(html)

            # 限制返回数量
            if len(products) > page_size:
                products = products[:page_size]

            return products

        except Exception as e:
            print(f"搜索失败: {e}")
            return []

    def search_all_pages(
        self,
        keyword: str,
        category: Optional[str] = None,
        price_range: Optional[Tuple[float, float]] = None,
        sort_by: str = 'sales',
        sort_order: str = 'desc',
        page_num: int = 1,
        page_count: int = 1,
        page_size: int = 20
    ) -> List[Dict]:
        """
        搜索多页商品

        Args:
            keyword: 搜索关键词
            category: 商品分类（可选）
            price_range: 价格区间
            sort_by: 排序方式
            sort_order: 排序顺序
            page_num: 起始页码
            page_count: 爬取页数
            page_size: 每页数量

        Returns:
            List[Dict]: 所有商品列表
        """
        all_products = []

        for i in range(page_count):
            current_page = page_num + i
            print(f"正在爬取第 {current_page} 页...")

            products = self.search(
                keyword=keyword,
                category=category,
                price_range=price_range,
                sort_by=sort_by,
                sort_order=sort_order,
                page_num=current_page,
                page_size=page_size
            )

            if not products:
                print(f"第 {current_page} 页没有数据，停止爬取")
                break

            all_products.extend(products)

            # 如果最后一页数据不足，提前停止
            if len(products) < page_size:
                break

        return all_products

    def _build_search_url(
        self,
        keyword: str,
        category: Optional[str] = None,
        price_range: Optional[Tuple[float, float]] = None,
        sort_by: str = 'sales',
        sort_order: str = 'desc',
        page_num: int = 1
    ) -> str:
        """
        构建搜索 URL

        Args:
            keyword: 搜索关键词
            category: 商品分类
            price_range: 价格区间
            sort_by: 排序方式
            sort_order: 排序顺序
            page_num: 页码

        Returns:
            str: 完整的搜索 URL
        """
        # 淘宝搜索 URL
        base_url = "https://s.taobao.com/search"

        # 搜索参数
        params = {
            'q': keyword,
            'imgfile': '',
            'js': '1',
            'stats_click': 'search_radio_all%3A1',
            'initiative_id': 'staobaoz_20260312',
            'ie': 'utf8',
        }

        # 添加排序参数
        if sort_by == 'sales':
            params['sort'] = 'sale-desc'
        elif sort_by == 'price':
            if sort_order == 'asc':
                params['sort'] = 'price-asc'
            else:
                params['sort'] = 'price-desc'

        # 添加价格区间
        if price_range:
            min_price, max_price = price_range
            params['filter'] = f'startPrice:{min_price}..{max_price}'

        # 添加页码
        params['bcoffset'] = str((page_num - 1) * 20)
        params['ntoffset'] = str((page_num - 1) * 20)

        # 构建查询字符串
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])

        return f"{base_url}?{query_string}"

    def _parse_products(self, html: str) -> List[Dict]:
        """
        解析商品数据

        Args:
            html: HTML 内容

        Returns:
            List[Dict]: 商品列表
        """
        products = []

        try:
            # 方案1: 尝试从 JSON 数据中解析
            json_data = self._extract_json_data(html)
            if json_data:
                products = self._parse_from_json(json_data)
                if products:
                    return products

            # 方案2: 从 HTML 解析
            soup = BeautifulSoup(html, 'lxml')
            products = self._parse_from_html(soup)

        except Exception as e:
            print(f"解析商品数据失败: {e}")

        return products

    def _extract_json_data(self, html: str) -> Optional[dict]:
        """
        从 HTML 中提取 JSON 数据

        Args:
            html: HTML 内容

        Returns:
            Optional[dict]: JSON 数据
        """
        # 尝试匹配 g_page_config 变量
        pattern = r'g_page_config\s*=\s*({[^;]+});'
        match = re.search(pattern, html)

        if match:
            try:
                json_str = match.group(1)
                # 处理可能的转义字符
                json_str = json_str.replace('\\/', '/')
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        return None

    def _parse_from_json(self, data: dict) -> List[Dict]:
        """
        从 JSON 数据解析商品

        Args:
            data: JSON 数据

        Returns:
            List[Dict]: 商品列表
        """
        products = []

        try:
            # 尝试不同的数据路径
            items = None

            # 路径1: data.mods.itemlist.data.auctions
            if 'mods' in data and 'itemlist' in data['mods']:
                itemlist = data['mods']['itemlist']
                if 'data' in itemlist and 'auctions' in itemlist['data']:
                    items = itemlist['data']['auctions']

            # 路径2: data.items
            elif 'items' in data:
                items = data['items']

            if not items:
                return []

            for item in items:
                product = {
                    'title': self._safe_get(item, 'raw_title') or self._safe_get(item, 'title', ''),
                    'price': self._parse_price(self._safe_get(item, 'view_price') or self._safe_get(item, 'price', '0')),
                    'sales': self._parse_sales(self._safe_get(item, 'view_sales') or self._safe_get(item, 'sales', '0')),
                    'shop_name': self._safe_get(item, 'nick') or '',
                    'shop_score': self._parse_shop_score(item),
                    'shop_location': self._safe_get(item, 'shopLink', {}).get('city', ''),
                    'product_url': f"https://item.taobao.com/item.htm?id={self._safe_get(item, 'nid', '')}",
                    'shop_url': f"https://shop{self._safe_get(item, 'user_id', '')}.taobao.com",
                    'image_id': self._safe_get(item, 'pic_url', ''),
                    'image_url': f"https://g.search.alicdn.com/img/bao/uploaded/i4/{self._safe_get(item, 'pic_url', '')}_60x60.jpg",
                }
                products.append(product)

        except Exception as e:
            print(f"从 JSON 解析商品失败: {e}")

        return products

    def _parse_from_html(self, soup: BeautifulSoup) -> List[Dict]:
        """
        从 HTML 解析商品

        Args:
            soup: BeautifulSoup 对象

        Returns:
            List[Dict]: 商品列表
        """
        products = []

        try:
            # 查找商品卡片
            items = soup.select('.J_MouserOnverReq')

            for item in items:
                try:
                    product = {
                        'title': self._extract_text(item, '.title a'),
                        'price': self._extract_price(item),
                        'sales': self._extract_sales(item),
                        'shop_name': self._extract_text(item, '.shopname a'),
                        'shop_score': self._extract_shop_score(item),
                        'shop_location': self._extract_location(item),
                        'product_url': self._extract_link(item, '.title a'),
                        'shop_url': self._extract_link(item, '.shopname a'),
                        'image_url': self._extract_image_url(item),
                    }
                    products.append(product)
                except Exception as e:
                    print(f"解析单个商品失败: {e}")
                    continue

        except Exception as e:
            print(f"从 HTML 解析商品失败: {e}")

        return products

    def _safe_get(self, data: dict, key: str, default: Any = None) -> Any:
        """
        安全获取字典值

        Args:
            data: 字典
            key: 键
            default: 默认值

        Returns:
            Any: 值或默认值
        """
        return data.get(key, default) if isinstance(data, dict) else default

    def _parse_price(self, price_str: str) -> float:
        """
        解析价格

        Args:
            price_str: 价格字符串

        Returns:
            float: 价格
        """
        try:
            # 移除货币符号和逗号
            price_str = price_str.replace('¥', '').replace(',', '').strip()
            return float(price_str)
        except (ValueError, AttributeError):
            return 0.0

    def _parse_sales(self, sales_str: str) -> int:
        """
        解析销量

        Args:
            sales_str: 销量字符串

        Returns:
            int: 销量
        """
        try:
            # 移除中文和空格
            if not sales_str:
                return 0

            sales_str = sales_str.replace('人付款', '').replace('件', '').strip()

            # 处理"万"单位
            if '万' in sales_str:
                sales_str = sales_str.replace('万', '')
                return int(float(sales_str) * 10000)

            # 处理"+"号
            if '+' in sales_str:
                sales_str = sales_str.replace('+', '')

            return int(float(sales_str))
        except (ValueError, AttributeError):
            return 0

    def _parse_shop_score(self, item: dict) -> float:
        """
        解析店铺评分

        Args:
            item: 商品数据

        Returns:
            float: 店铺评分
        """
        try:
            if 'shopScore' in item:
                return float(item['shopScore'])
            return 5.0  # 默认评分
        except (ValueError, TypeError):
            return 5.0

    def _extract_text(self, element: Tag, selector: str) -> str:
        """
        提取文本内容

        Args:
            element: BeautifulSoup 元素
            selector: CSS 选择器

        Returns:
            str: 文本内容
        """
        try:
            el = element.select_one(selector)
            return el.get_text(strip=True) if el else ''
        except Exception:
            return ''

    def _extract_price(self, element: Tag) -> float:
        """
        提取价格

        Args:
            element: BeautifulSoup 元素

        Returns:
            float: 价格
        """
        try:
            price_el = element.select_one('.price')
            if price_el:
                price_text = price_el.get_text(strip=True)
                return self._parse_price(price_text)
            return 0.0
        except Exception:
            return 0.0

    def _extract_sales(self, element: Tag) -> int:
        """
        提取销量

        Args:
            element: BeautifulSoup 元素

        Returns:
            int: 销量
        """
        try:
            sales_el = element.select_one('.deal-cnt')
            if sales_el:
                sales_text = sales_el.get_text(strip=True)
                return self._parse_sales(sales_text)
            return 0
        except Exception:
            return 0

    def _extract_shop_score(self, element: Tag) -> float:
        """
        提取店铺评分

        Args:
            element: BeautifulSoup 元素

        Returns:
            float: 店铺评分
        """
        try:
            score_el = element.select_one('.dsr-score')
            if score_el:
                score_text = score_el.get_text(strip=True)
                return float(score_text)
            return 5.0
        except Exception:
            return 5.0

    def _extract_location(self, element: Tag) -> str:
        """
        提取店铺地址

        Args:
            element: BeautifulSoup 元素

        Returns:
            str: 店铺地址
        """
        try:
            location_el = element.select_one('.location')
            if location_el:
                return location_el.get_text(strip=True)
            return ''
        except Exception:
            return ''

    def _extract_link(self, element: Tag, selector: str) -> str:
        """
        提取链接

        Args:
            element: BeautifulSoup 元素
            selector: CSS 选择器

        Returns:
            str: 链接
        """
        try:
            el = element.select_one(selector)
            if el and el.has_attr('href'):
                return el['href']
            return ''
        except Exception:
            return ''

    def _extract_image_url(self, element: Tag) -> str:
        """
        提取图片链接

        Args:
            element: BeautifulSoup 元素

        Returns:
            str: 图片链接
        """
        try:
            img_el = element.select_one('.pic img')
            if img_el:
                if img_el.has_attr('data-src'):
                    return img_el['data-src']
                elif img_el.has_attr('src'):
                    return img_el['src']
            return ''
        except Exception:
            return ''

    def close(self):
        """
        关闭爬虫
        """
        self.anti_spider.close()

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理器"""
        self.close()
