#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电商价格监控爬虫 / E-commerce Price Monitor
功能：监控电商平台（京东、淘宝等）商品价格变化，记录历史数据
作者：AI助手
日期：2026-03-11
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
import logging
from typing import List, Dict, Optional
from datetime import datetime
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体支持
matplotlib.rcParams['axes.unicode_minus'] = False

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EcommerceMonitor:
    """电商价格监控类 / E-commerce Price Monitor Class"""
    
    def __init__(self, config_file: str = 'config.json'):
        """
        初始化监控器 / Initialize Monitor
        
        Args:
            config_file: 配置文件路径 / Config file path
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.headers = self._get_headers()
        self.session = requests.Session()
        self.price_history = []
        
        # 加载历史数据
        self._load_history()
    
    def _load_config(self) -> Dict:
        """
        加载配置文件 / Load Config File
        
        Returns:
            配置字典 / Config dict
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f'成功加载配置文件 / Config loaded: {self.config_file}')
            return config
        except Exception as e:
            logger.error(f'加载配置文件失败 / Failed to load config: {e}')
            # 返回默认配置
            return {
                'products': [],
                'settings': {
                    'check_interval': 300,
                    'log_file': 'price_history.log',
                    'history_file': 'price_history.json'
                }
            }
    
    def _load_history(self):
        """加载历史价格数据 / Load Historical Price Data"""
        history_file = self.config['settings'].get('history_file', 'price_history.json')
        
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.price_history = json.load(f)
                logger.info(f'加载历史数据: {len(self.price_history)} 条记录')
            except Exception as e:
                logger.error(f'加载历史数据失败 / Failed to load history: {e}')
                self.price_history = []
    
    def _save_history(self):
        """保存历史价格数据 / Save Historical Price Data"""
        history_file = self.config['settings'].get('history_file', 'price_history.json')
        
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.price_history, f, ensure_ascii=False, indent=2)
            logger.info(f'保存历史数据: {len(self.price_history)} 条记录')
        except Exception as e:
            logger.error(f'保存历史数据失败 / Failed to save history: {e}')
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头 / Get Request Headers"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
    
    def _delay(self):
        """随机延时 / Random Delay"""
        delay = random.uniform(1, 3)
        time.sleep(delay)
    
    def get_jd_price(self, url: str) -> Optional[float]:
        """
        获取京东商品价格 / Get JD Product Price
        
        Args:
            url: 商品链接 / Product URL
            
        Returns:
            商品价格 / Product price
        """
        try:
            # 这里是模拟数据，实际需要解析京东页面
            # This is simulated data, actual implementation requires parsing JD page
            logger.info(f'获取京东价格: {url}')
            
            # 模拟价格
            price = round(random.uniform(100, 10000), 2)
            logger.info(f'京东价格: ¥{price}')
            
            self._delay()
            return price
            
        except Exception as e:
            logger.error(f'获取京东价格失败 / Failed to get JD price: {e}')
            return None
    
    def get_taobao_price(self, url: str) -> Optional[float]:
        """
        获取淘宝商品价格 / Get Taobao Product Price
        
        Args:
            url: 商品链接 / Product URL
            
        Returns:
            商品价格 / Product price
        """
        try:
            logger.info(f'获取淘宝价格: {url}')
            
            # 模拟价格
            price = round(random.uniform(100, 10000), 2)
            logger.info(f'淘宝价格: ¥{price}')
            
            self._delay()
            return price
            
        except Exception as e:
            logger.error(f'获取淘宝价格失败 / Failed to get Taobao price: {e}')
            return None
    
    def check_product_price(self, product: Dict) -> Optional[Dict]:
        """
        检查单个商品价格 / Check Single Product Price
        
        Args:
            product: 商品信息 / Product info
            
        Returns:
            价格记录 / Price record
        """
        if not product.get('enabled', False):
            logger.info(f'商品已禁用 / Product disabled: {product.get("name", "")}')
            return None
        
        platform = product.get('platform', '')
        url = product.get('url', '')
        
        if platform == 'jd':
            price = self.get_jd_price(url)
        elif platform == 'taobao':
            price = self.get_taobao_price(url)
        else:
            logger.warning(f'未知平台 / Unknown platform: {platform}')
            return None
        
        if price is None:
            return None
        
        # 记录价格
        record = {
            '商品名称': product.get('name', ''),
            '平台': platform,
            '价格': price,
            '时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '链接': url
        }
        
        return record
    
    def check_all_products(self) -> List[Dict]:
        """
        检查所有商品价格 / Check All Products Price
        
        Returns:
            价格记录列表 / List of price records
        """
        products = self.config.get('products', [])
        records = []
        
        print(f'\n开始检查 {len(products)} 个商品价格...')
        print('=' * 50)
        
        for i, product in enumerate(products, 1):
            print(f'\n[{i}/{len(products)}] 检查商品: {product.get("name", "")}')
            
            record = self.check_product_price(product)
            
            if record:
                records.append(record)
                self.price_history.append(record)
                print(f'✅ 当前价格: ¥{record["价格"]}')
            else:
                print(f'❌ 获取价格失败')
        
        # 保存历史数据
        if records:
            self._save_history()
        
        return records
    
    def get_price_history(self, product_name: str) -> List[Dict]:
        """
        获取指定商品的价格历史 / Get Price History for Specific Product
        
        Args:
            product_name: 商品名称 / Product name
            
        Returns:
            价格历史列表 / Price history list
        """
        history = [
            record for record in self.price_history
            if record['商品名称'] == product_name
        ]
        return history
    
    def generate_price_chart(self, product_name: str, output_file: str = 'price_chart.png'):
        """
        生成价格趋势图 / Generate Price Trend Chart
        
        Args:
            product_name: 商品名称 / Product name
            output_file: 输出文件名 / Output filename
        """
        history = self.get_price_history(product_name)
        
        if not history:
            print(f'没有找到 "{product_name}" 的价格数据')
            return
        
        try:
            # 准备数据
            times = [record['时间'] for record in history]
            prices = [record['价格'] for record in history]
            
            # 创建图表
            plt.figure(figsize=(12, 6))
            plt.plot(times, prices, marker='o', linewidth=2, markersize=8)
            
            # 设置标题和标签
            plt.title(f'{product_name} - 价格趋势', fontsize=16)
            plt.xlabel('时间 / Time', fontsize=12)
            plt.ylabel('价格 (¥)', fontsize=12)
            plt.grid(True, alpha=0.3)
            
            # 旋转x轴标签
            plt.xticks(rotation=45, ha='right')
            
            # 调整布局
            plt.tight_layout()
            
            # 保存图表
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f'✅ 价格趋势图已保存: {output_file}')
            
            # 显示图表
            plt.show()
            
        except Exception as e:
            logger.error(f'生成价格趋势图失败 / Failed to generate chart: {e}')
    
    def print_summary(self):
        """打印价格统计摘要 / Print Price Summary"""
        if not self.price_history:
            print('暂无价格数据 / No price data available')
            return
        
        print('\n=== 价格统计摘要 / Price Statistics Summary ===')
        
        # 按商品统计
        product_stats = {}
        for record in self.price_history:
            name = record['商品名称']
            platform = record['平台']
            price = record['价格']
            
            key = f'{name} ({platform})'
            if key not in product_stats:
                product_stats[key] = []
            product_stats[key].append(price)
        
        for key, prices in product_stats.items():
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)
            
            print(f'\n{key}:')
            print(f'  记录数: {len(prices)}')
            print(f'  最低价: ¥{min_price:.2f}')
            print(f'  最高价: ¥{max_price:.2f}')
            print(f'  平均价: ¥{avg_price:.2f}')
        
        print('=' * 40)


def main():
    """主函数 / Main Function"""
    print('=' * 60)
    print('电商价格监控爬虫 / E-commerce Price Monitor')
    print('=' * 60)
    
    # 创建监控器实例
    monitor = EcommerceMonitor()
    
    # 检查所有商品价格
    records = monitor.check_all_products()
    
    if records:
        print(f'\n✅ 成功检查 {len(records)} 个商品')
        
        # 打印统计
        monitor.print_summary()
        
        # 生成价格趋势图（可选）
        if len(records) > 0:
            product_name = records[0]['商品名称']
            chart_file = f'{product_name}_price_trend.png'
            
            choice = input(f'\n是否生成 "{product_name}" 价格趋势图？(y/n): ').strip().lower()
            
            if choice == 'y':
                monitor.generate_price_chart(product_name, chart_file)
        
    else:
        print('\n❌ 未能获取到价格数据')
    
    print('=' * 60)


if __name__ == '__main__':
    main()
