"""
数据分析模块
生成价格分布、销量排行、店铺排行等分析报告
"""

import os
from typing import List, Dict, Optional
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


class DataAnalyzer:
    """数据分析类"""

    def __init__(self, products: List[Dict]):
        """
        初始化数据分析器

        Args:
            products: 商品数据列表
        """
        self.products = products
        self.df = pd.DataFrame(products) if products else pd.DataFrame()

    def get_basic_stats(self) -> Dict:
        """
        获取基础统计信息

        Returns:
            Dict: 基础统计信息
        """
        if self.df.empty:
            return {}

        stats = {
            'total_products': len(self.df),
            'unique_shops': self.df['shop_name'].nunique() if 'shop_name' in self.df else 0,
        }

        # 价格统计
        if 'price' in self.df:
            prices = self.df['price'].dropna()
            if not prices.empty:
                stats['price'] = {
                    'min': float(prices.min()),
                    'max': float(prices.max()),
                    'mean': float(prices.mean()),
                    'median': float(prices.median()),
                }

        # 销量统计
        if 'sales' in self.df:
            sales = self.df['sales'].dropna()
            if not sales.empty:
                stats['sales'] = {
                    'total': int(sales.sum()),
                    'mean': float(sales.mean()),
                    'median': float(sales.median()),
                }

        # 店铺评分统计
        if 'shop_score' in self.df:
            scores = self.df['shop_score'].dropna()
            if not scores.empty:
                stats['shop_score'] = {
                    'min': float(scores.min()),
                    'max': float(scores.max()),
                    'mean': float(scores.mean()),
                }

        return stats

    def get_price_distribution(self, bins: int = 10) -> Dict:
        """
        获取价格分布

        Args:
            bins: 分箱数量

        Returns:
            Dict: 价格分布数据
        """
        if self.df.empty or 'price' not in self.df:
            return {}

        prices = self.df['price'].dropna()
        if prices.empty:
            return {}

        # 创建分箱
        price_min = prices.min()
        price_max = prices.max()

        if price_min == price_max:
            # 所有价格相同，创建单个分箱
            distribution = [{
                'range': f'{price_min:.2f}',
                'count': len(prices),
                'percentage': 100.0
            }]
        else:
            # 创建分箱
            hist, bin_edges = np.histogram(prices, bins=bins)

            distribution = []
            total = len(prices)

            for i in range(len(hist)):
                lower = bin_edges[i]
                upper = bin_edges[i + 1]
                count = hist[i]
                percentage = (count / total) * 100

                distribution.append({
                    'range': f'{lower:.2f} - {upper:.2f}',
                    'lower': lower,
                    'upper': upper,
                    'count': int(count),
                    'percentage': round(percentage, 2)
                })

        return {
            'min': float(price_min),
            'max': float(price_max),
            'bins': bins,
            'distribution': distribution
        }

    def get_top_products_by_sales(self, top_n: int = 20) -> List[Dict]:
        """
        获取销量 TOP N 商品

        Args:
            top_n: 返回前 N 个

        Returns:
            List[Dict]: 商品列表
        """
        if self.df.empty or 'sales' not in self.df:
            return []

        # 按销量排序
        top_products = self.df.nlargest(top_n, 'sales')

        # 转换为字典列表
        result = []
        for _, row in top_products.iterrows():
            result.append({
                'title': row.get('title', ''),
                'price': float(row.get('price', 0)),
                'sales': int(row.get('sales', 0)),
                'shop_name': row.get('shop_name', ''),
                'product_url': row.get('product_url', ''),
            })

        return result

    def get_top_shops_by_sales(self, top_n: int = 20) -> List[Dict]:
        """
        获取销量 TOP N 店铺

        Args:
            top_n: 返回前 N 个

        Returns:
            List[Dict]: 店铺列表
        """
        if self.df.empty or 'sales' not in self.df:
            return []

        # 按店铺分组并统计销量
        if 'shop_name' in self.df:
            shop_sales = self.df.groupby('shop_name')['sales'].sum().sort_values(ascending=False)
        else:
            return []

        # 转换为字典列表
        result = []
        for shop_name, sales in shop_sales.head(top_n).items():
            # 获取该店铺的第一个商品信息
            shop_data = self.df[self.df['shop_name'] == shop_name].iloc[0]

            result.append({
                'shop_name': shop_name,
                'sales': int(sales),
                'shop_location': shop_data.get('shop_location', ''),
                'shop_score': float(shop_data.get('shop_score', 0)),
            })

        return result

    def get_shops_by_score(self, top_n: int = 20) -> List[Dict]:
        """
        获取评分 TOP N 店铺

        Args:
            top_n: 返回前 N 个

        Returns:
            List[Dict]: 店铺列表
        """
        if self.df.empty or 'shop_score' not in self.df:
            return []

        # 按店铺分组并获取评分
        if 'shop_name' in self.df:
            shop_scores = self.df.groupby('shop_name')['shop_score'].mean().sort_values(ascending=False)
        else:
            return []

        # 转换为字典列表
        result = []
        for shop_name, score in shop_scores.head(top_n).items():
            # 获取该店铺的第一个商品信息
            shop_data = self.df[self.df['shop_name'] == shop_name].iloc[0]

            result.append({
                'shop_name': shop_name,
                'shop_score': float(score),
                'shop_location': shop_data.get('shop_location', ''),
                'shop_url': shop_data.get('shop_url', ''),
            })

        return result

    def save_price_distribution_chart(self, filename: str, bins: int = 10) -> bool:
        """
        保存价格分布图

        Args:
            filename: 输出文件名
            bins: 分箱数量

        Returns:
            bool: 是否成功
        """
        if self.df.empty or 'price' not in self.df:
            return False

        try:
            prices = self.df['price'].dropna()

            # 确保目录存在
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            # 创建图形
            fig, ax = plt.subplots(figsize=(10, 6))

            # 绘制直方图
            ax.hist(prices, bins=bins, edgecolor='black', alpha=0.7)

            # 设置标题和标签
            ax.set_xlabel('价格 (元)', fontsize=12)
            ax.set_ylabel('商品数量', fontsize=12)
            ax.set_title(f'价格分布直方图 (共 {len(prices)} 个商品)', fontsize=14)

            # 添加网格
            ax.grid(True, alpha=0.3)

            # 保存图形
            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()

            return True

        except Exception as e:
            print(f"保存价格分布图失败: {e}")
            return False

    def save_sales_chart(self, filename: str, top_n: int = 20) -> bool:
        """
        保存销量排行图

        Args:
            filename: 输出文件名
            top_n: 显示前 N 个

        Returns:
            bool: 是否成功
        """
        if self.df.empty or 'sales' not in self.df:
            return False

        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            # 获取 TOP N 商品
            top_products = self.get_top_products_by_sales(top_n)

            if not top_products:
                return False

            # 提取数据
            titles = [p['title'][:15] + '...' if len(p['title']) > 15 else p['title'] for p in top_products]
            sales = [p['sales'] for p in top_products]

            # 创建图形
            fig, ax = plt.subplots(figsize=(12, 8))

            # 绘制柱状图
            bars = ax.barh(range(len(titles)), sales[::-1], color='skyblue', edgecolor='black')

            # 设置标题和标签
            ax.set_yticks(range(len(titles)))
            ax.set_yticklabels(titles[::-1], fontsize=10)
            ax.set_xlabel('销量 (件)', fontsize=12)
            ax.set_title(f'TOP {len(top_products)} 畅销商品', fontsize=14)

            # 添加数值标签
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2,
                       f'{int(width)}',
                       ha='left', va='center', fontsize=9)

            # 添加网格
            ax.grid(True, alpha=0.3, axis='x')

            # 保存图形
            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()

            return True

        except Exception as e:
            print(f"保存销量排行图失败: {e}")
            return False

    def generate_report(
        self,
        output_file: str = "reports/analysis.html",
        top_n: int = 20,
        price_bins: int = 10
    ) -> str:
        """
        生成 HTML 分析报告

        Args:
            output_file: 输出文件名
            top_n: TOP N 数量
            price_bins: 价格分箱数量

        Returns:
            str: 报告文件路径
        """
        # 确保目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # 生成图表文件名
        base_dir = os.path.dirname(output_file)
        price_chart_file = os.path.join(base_dir, 'price_distribution.png')
        sales_chart_file = os.path.join(base_dir, 'sales_ranking.png')

        # 保存图表
        self.save_price_distribution_chart(price_chart_file, price_bins)
        self.save_sales_chart(sales_chart_file, top_n)

        # 获取数据
        basic_stats = self.get_basic_stats()
        price_distribution = self.get_price_distribution(price_bins)
        top_products = self.get_top_products_by_sales(top_n)
        top_shops = self.get_top_shops_by_sales(top_n)
        shops_by_score = self.get_shops_by_score(top_n)

        # 生成 HTML 报告
        html = self._generate_html_report(
            basic_stats=basic_stats,
            price_distribution=price_distribution,
            top_products=top_products,
            top_shops=top_shops,
            shops_by_score=shops_by_score,
            price_chart_file='price_distribution.png',
            sales_chart_file='sales_ranking.png',
            generated_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        # 保存报告
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_file

    def _generate_html_report(
        self,
        basic_stats: Dict,
        price_distribution: Dict,
        top_products: List[Dict],
        top_shops: List[Dict],
        shops_by_score: List[Dict],
        price_chart_file: str,
        sales_chart_file: str,
        generated_time: str
    ) -> str:
        """
        生成 HTML 报告内容

        Returns:
            str: HTML 内容
        """
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>淘宝商品数据分析报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background-color: #f5f5f5;
            line-height: 1.6;
            color: #333;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}

        .header .time {{
            font-size: 14px;
            opacity: 0.9;
        }}

        .card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .card h2 {{
            font-size: 20px;
            margin-bottom: 20px;
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}

        .stat-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}

        .stat-item .label {{
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }}

        .stat-item .value {{
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }}

        .chart-container {{
            text-align: center;
            margin: 20px 0;
        }}

        .chart-container img {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}

        th {{
            background-color: #667eea;
            color: white;
            font-weight: bold;
        }}

        tr:hover {{
            background-color: #f8f9fa;
        }}

        .rank {{
            display: inline-block;
            width: 30px;
            height: 30px;
            line-height: 30px;
            text-align: center;
            background: #667eea;
            color: white;
            border-radius: 50%;
            font-weight: bold;
            margin-right: 10px;
        }}

        .rank-1 {{ background: #ffd700; }}
        .rank-2 {{ background: #c0c0c0; }}
        .rank-3 {{ background: #cd7f32; }}

        .price-range {{
            font-size: 14px;
            padding: 8px 12px;
            margin: 5px 0;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 淘宝商品数据分析报告</h1>
            <p class="time">生成时间: {generated_time}</p>
        </div>

        <!-- 基础统计 -->
        <div class="card">
            <h2>📈 基础统计</h2>
            <div class="stats-grid">
"""

        # 添加基础统计
        if 'total_products' in basic_stats:
            html += f"""
                <div class="stat-item">
                    <div class="label">商品总数</div>
                    <div class="value">{basic_stats['total_products']}</div>
                </div>
            """

        if 'unique_shops' in basic_stats:
            html += f"""
                <div class="stat-item">
                    <div class="label">店铺数量</div>
                    <div class="value">{basic_stats['unique_shops']}</div>
                </div>
            """

        if 'price' in basic_stats:
            html += f"""
                <div class="stat-item">
                    <div class="label">平均价格</div>
                    <div class="value">¥{basic_stats['price']['mean']:.2f}</div>
                </div>
                <div class="stat-item">
                    <div class="label">价格范围</div>
                    <div class="value">¥{basic_stats['price']['min']:.2f} - ¥{basic_stats['price']['max']:.2f}</div>
                </div>
            """

        if 'sales' in basic_stats:
            html += f"""
                <div class="stat-item">
                    <div class="label">总销量</div>
                    <div class="value">{basic_stats['sales']['total']}</div>
                </div>
                <div class="stat-item">
                    <div class="label">平均销量</div>
                    <div class="value">{int(basic_stats['sales']['mean'])}</div>
                </div>
            """

        html += """
            </div>
        </div>
"""

        # 价格分布图表
        if price_chart_file:
            html += f"""
        <div class="card">
            <h2>💰 价格分布</h2>
            <div class="chart-container">
                <img src="{price_chart_file}" alt="价格分布图">
            </div>
"""

            if 'distribution' in price_distribution:
                html += """
            <div>
                <h3>价格区间统计</h3>
"""

                for item in price_distribution['distribution']:
                    html += f"""
                <div class="price-range">
                    <strong>{item['range']}</strong>
                    <span style="float: right;">
                        数量: {item['count']} | 占比: {item['percentage']}%
                    </span>
                </div>
"""

                html += """
            </div>
"""

            html += """
        </div>
"""

        # 销量排行图表
        if sales_chart_file:
            html += f"""
        <div class="card">
            <h2>🏆 销量排行</h2>
            <div class="chart-container">
                <img src="{sales_chart_file}" alt="销量排行图">
            </div>
"""

            if top_products:
                html += f"""
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>商品名称</th>
                        <th>价格</th>
                        <th>销量</th>
                        <th>店铺</th>
                    </tr>
                </thead>
                <tbody>
"""

                for i, product in enumerate(top_products, 1):
                    rank_class = f'rank-{i}' if i <= 3 else ''
                    title = product['title'][:50] + '...' if len(product['title']) > 50 else product['title']
                    html += f"""
                    <tr>
                        <td><span class="rank {rank_class}">{i}</span></td>
                        <td><a href="{product['product_url']}" target="_blank">{title}</a></td>
                        <td>¥{product['price']:.2f}</td>
                        <td>{product['sales']}</td>
                        <td>{product['shop_name']}</td>
                    </tr>
"""

                html += """
                </tbody>
            </table>
"""

            html += """
        </div>
"""

        # 店铺排行
        if top_shops:
            html += f"""
        <div class="card">
            <h2>🏪 店铺销量排行 TOP {len(top_shops)}</h2>
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>店铺名称</th>
                        <th>总销量</th>
                        <th>店铺地址</th>
                    </tr>
                </thead>
                <tbody>
"""

            for i, shop in enumerate(top_shops, 1):
                rank_class = f'rank-{i}' if i <= 3 else ''
                html += f"""
                    <tr>
                        <td><span class="rank {rank_class}">{i}</span></td>
                        <td>{shop['shop_name']}</td>
                        <td>{shop['sales']}</td>
                        <td>{shop['shop_location']}</td>
                    </tr>
"""

            html += """
                </tbody>
            </table>
        </div>
"""

        # 店铺评分排行
        if shops_by_score:
            html += f"""
        <div class="card">
            <h2>⭐ 店铺评分排行 TOP {len(shops_by_score)}</h2>
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>店铺名称</th>
                        <th>评分</th>
                        <th>店铺地址</th>
                    </tr>
                </thead>
                <tbody>
"""

            for i, shop in enumerate(shops_by_score, 1):
                rank_class = f'rank-{i}' if i <= 3 else ''
                html += f"""
                    <tr>
                        <td><span class="rank {rank_class}">{i}</span></td>
                        <td>{shop['shop_name']}</td>
                        <td>{shop['shop_score']:.2f}</td>
                        <td>{shop['shop_location']}</td>
                    </tr>
"""

            html += """
                </tbody>
            </table>
        </div>
"""

        html += f"""
        <div class="footer">
            <p>本报告由淘宝商品爬虫自动生成</p>
            <p>仅供学习研究使用</p>
        </div>
    </div>
</body>
</html>
"""

        return html
