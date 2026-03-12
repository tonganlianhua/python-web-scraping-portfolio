#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
电商价格监控爬虫
支持京东、淘宝等电商平台的价格监控
"""

import json
import requests
from bs4 import BeautifulSoup
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
import os


class PriceMonitor:
    """价格监控核心类"""

    def __init__(self, config_path: str = "config.json"):
        """
        初始化监控器

        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.products = self.config.get("products", [])
        self.settings = self.config.get("settings", {})
        self._setup_logging()

        # 加载历史价格数据
        self.history_file = self.settings.get("history_file", "price_history.json")
        self.price_history = self._load_history()

    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"配置文件不存在: {config_path}")
            raise
        except json.JSONDecodeError:
            logging.error(f"配置文件格式错误: {config_path}")
            raise

    def _load_history(self) -> Dict:
        """加载历史价格数据"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                logging.warning("历史价格文件损坏，重新创建")
                return {}
        return {}

    def _save_history(self):
        """保存历史价格数据"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.price_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"保存历史价格失败: {e}")

    def _setup_logging(self):
        """设置日志"""
        log_file = self.settings.get("log_file", "price_history.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    def get_jd_price(self, url: str) -> Optional[float]:
        """
        获取京东商品价格

        Args:
            url: 商品URL

        Returns:
            价格（浮点数），失败返回None
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'lxml')

            # 尝试多种选择器获取价格
            price_selectors = [
                '.price .p-price .price',  # 京东标准价格
                '.price .p-price',         # 备用选择器1
                'span[class*="price"]',    # 备用选择器2
                '.p-price strong i',       # 备用选择器3
            ]

            price = None
            for selector in price_selectors:
                element = soup.select_one(selector)
                if element:
                    # 提取价格文本
                    price_text = element.get_text().strip()
                    # 移除货币符号和逗号
                    price_text = price_text.replace('¥', '').replace(',', '').replace('￥', '')
                    try:
                        price = float(price_text)
                        break
                    except ValueError:
                        continue

            if price is not None:
                return price
            else:
                logging.warning(f"无法从京东页面提取价格: {url}")
                return None

        except requests.RequestException as e:
            logging.error(f"请求京东商品失败: {url}, 错误: {e}")
            return None
        except Exception as e:
            logging.error(f"解析京东商品价格失败: {url}, 错误: {e}")
            return None

    def get_taobao_price(self, url: str) -> Optional[float]:
        """
        获取淘宝/天猫商品价格

        Args:
            url: 商品URL

        Returns:
            价格（浮点数），失败返回None
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'lxml')

            # 尝试多种选择器获取价格
            price_selectors = [
                '.tm-price',          # 天猫价格
                '.tb-price',          # 淘宝价格
                'span[class*="price"]',  # 通用价格
                '#J_price',           # 价格元素
            ]

            price = None
            for selector in price_selectors:
                element = soup.select_one(selector)
                if element:
                    price_text = element.get_text().strip()
                    price_text = price_text.replace('¥', '').replace(',', '').replace('￥', '')
                    try:
                        price = float(price_text)
                        break
                    except ValueError:
                        continue

            if price is not None:
                return price
            else:
                logging.warning(f"无法从淘宝/天猫页面提取价格: {url}")
                return None

        except requests.RequestException as e:
            logging.error(f"请求淘宝商品失败: {url}, 错误: {e}")
            return None
        except Exception as e:
            logging.error(f"解析淘宝商品价格失败: {url}, 错误: {e}")
            return None

    def get_price(self, product: Dict) -> Optional[float]:
        """
        根据平台获取商品价格

        Args:
            product: 商品配置字典

        Returns:
            价格（浮点数），失败返回None
        """
        platform = product.get("platform", "").lower()
        url = product.get("url", "")

        if platform == "jd":
            return self.get_jd_price(url)
        elif platform in ["taobao", "tmall"]:
            return self.get_taobao_price(url)
        else:
            logging.error(f"不支持的平台: {platform}")
            return None

    def check_price_change(self, product: Dict, current_price: float) -> bool:
        """
        检查价格是否变动

        Args:
            product: 商品配置
            current_price: 当前价格

        Returns:
            价格是否变动
        """
        product_id = product.get("url", "")
        if product_id in self.price_history:
            last_price = self.price_history[product_id][-1].get("price")
            if last_price is not None:
                return abs(current_price - last_price) > 0.01  # 避免浮点数精度问题
        return True  # 首次监控，视为变动

    def notify(self, product: Dict, current_price: float, previous_price: Optional[float] = None):
        """
        发送价格变动通知

        Args:
            product: 商品配置
            current_price: 当前价格
            previous_price: 历史价格（可选）
        """
        name = product.get("name", "未知商品")
        platform = product.get("platform", "未知平台")

        if previous_price is None:
            message = f"🛒 新商品上架\n平台: {platform}\n商品: {name}\n价格: ¥{current_price:.2f}"
        else:
            if current_price < previous_price:
                diff = previous_price - current_price
                percent = (diff / previous_price) * 100
                message = f"📉 价格下降！\n平台: {platform}\n商品: {name}\n原价: ¥{previous_price:.2f}\n现价: ¥{current_price:.2f}\n降幅: ¥{diff:.2f} ({percent:.1f}%)"
            elif current_price > previous_price:
                diff = current_price - previous_price
                percent = (diff / previous_price) * 100
                message = f"📈 价格上涨\n平台: {platform}\n商品: {name}\n原价: ¥{previous_price:.2f}\n现价: ¥{current_price:.2f}\n涨幅: ¥{diff:.2f} ({percent:.1f}%)"
            else:
                return  # 价格未变动，不发送通知

        # 打印到控制台
        print(f"\n{'='*60}")
        print(message)
        print(f"{'='*60}\n")

        # 记录到日志
        logging.info(message.replace('\n', ' | '))

    def record_price(self, product: Dict, price: float):
        """
        记录价格到历史

        Args:
            product: 商品配置
            price: 价格
        """
        product_id = product.get("url", "")

        if product_id not in self.price_history:
            self.price_history[product_id] = []

        # 添加价格记录
        self.price_history[product_id].append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "price": price
        })

        # 保存到文件
        self._save_history()

    def monitor_once(self):
        """执行一次价格监控"""
        logging.info(f"开始监控 {len(self.products)} 个商品...")

        for product in self.products:
            if not product.get("enabled", True):
                logging.info(f"跳过已禁用的商品: {product.get('name', '未知')}")
                continue

            name = product.get("name", "未知商品")
            url = product.get("url", "")

            logging.info(f"正在监控: {name} ({url})")

            # 获取当前价格
            current_price = self.get_price(product)

            if current_price is None:
                logging.error(f"获取价格失败: {name}")
                continue

            logging.info(f"当前价格: ¥{current_price:.2f}")

            # 检查价格变动
            product_id = product.get("url", "")
            previous_price = None

            if product_id in self.price_history and len(self.price_history[product_id]) > 0:
                previous_price = self.price_history[product_id][-1].get("price")

            # 发送通知
            self.notify(product, current_price, previous_price)

            # 记录价格
            self.record_price(product, current_price)

    def monitor_continuous(self, interval: int = None):
        """
        持续监控

        Args:
            interval: 监控间隔（秒），默认从配置读取
        """
        if interval is None:
            interval = self.settings.get("check_interval", 300)

        logging.info(f"开始持续监控，间隔 {interval} 秒...")

        while True:
            try:
                self.monitor_once()
                logging.info(f"等待 {interval} 秒后继续...")
                time.sleep(interval)
            except KeyboardInterrupt:
                logging.info("用户中断，停止监控")
                break
            except Exception as e:
                logging.error(f"监控过程出错: {e}")
                time.sleep(interval)

    def get_price_history(self, product: Dict) -> List[Dict]:
        """
        获取商品的历史价格

        Args:
            product: 商品配置

        Returns:
            历史价格列表
        """
        product_id = product.get("url", "")
        return self.price_history.get(product_id, [])

    def print_history(self):
        """打印所有商品的历史价格"""
        print("\n" + "="*60)
        print("价格历史记录")
        print("="*60)

        for product in self.products:
            name = product.get("name", "未知商品")
            history = self.get_price_history(product)

            if not history:
                print(f"\n{name}: 暂无记录")
                continue

            print(f"\n{name}:")
            print(f"{'时间':<20} {'价格':<10}")
            print("-" * 30)

            for record in history[-10:]:  # 只显示最近10条
                timestamp = record.get("timestamp", "")
                price = record.get("price", 0)
                print(f"{timestamp:<20} ¥{price:>7.2f}")


def main():
    """主函数"""
    import sys

    # 解析命令行参数
    config_path = "config.json"
    continuous = False
    show_history = False

    for arg in sys.argv[1:]:
        if arg == "--continuous" or arg == "-c":
            continuous = True
        elif arg == "--history" or arg == "-h":
            show_history = True
        elif arg.startswith("--config="):
            config_path = arg.split("=", 1)[1]
        elif arg == "--help" or arg == "-help":
            print("电商价格监控爬虫")
            print("\n用法:")
            print("  python monitor.py              # 单次监控")
            print("  python monitor.py -c           # 持续监控")
            print("  python monitor.py -h           # 显示价格历史")
            print("  python monitor.py --config=custom.json  # 使用自定义配置")
            return

    # 创建监控器
    try:
        monitor = PriceMonitor(config_path)
    except Exception as e:
        print(f"初始化失败: {e}")
        return

    # 显示历史价格
    if show_history:
        monitor.print_history()
        return

    # 执行监控
    if continuous:
        monitor.monitor_continuous()
    else:
        monitor.monitor_once()
        print("\n监控完成！使用 -h 参数查看价格历史")


if __name__ == "__main__":
    main()
