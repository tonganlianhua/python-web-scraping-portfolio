#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
演示脚本 - 模拟监控功能
"""

import json
import os
from datetime import datetime


def main():
    """运行演示"""
    print("="*60)
    print("电商价格监控爬虫 - 功能演示")
    print("="*60)
    print()

    # 模拟监控结果
    demo_data = {
        "products": [
            {
                "name": "京东iPhone 15",
                "platform": "jd",
                "url": "https://item.jd.com/100046560532.html",
                "current_price": 5999.0,
                "previous_price": 6299.0
            },
            {
                "name": "京东小米14",
                "platform": "jd",
                "url": "https://item.jd.com/100060977554.html",
                "current_price": 3999.0,
                "previous_price": None
            }
        ]
    }

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始监控 {len(demo_data['products'])} 个商品...")
    print()

    for idx, product in enumerate(demo_data["products"], 1):
        name = product["name"]
        platform = product["platform"]
        current_price = product["current_price"]
        previous_price = product["previous_price"]

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在监控: {name}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 当前价格: ￥{current_price:.2f}")

        # 显示通知
        if previous_price is None:
            message = f"新商品上架\n平台: {platform}\n商品: {name}\n价格: ￥{current_price:.2f}"
        else:
            if current_price < previous_price:
                diff = previous_price - current_price
                percent = (diff / previous_price) * 100
                message = f"价格下降！\n平台: {platform}\n商品: {name}\n原价: ￥{previous_price:.2f}\n现价: ￥{current_price:.2f}\n降幅: ￥{diff:.2f} ({percent:.1f}%)"
            else:
                message = f"价格记录\n平台: {platform}\n商品: {name}\n价格: ￥{current_price:.2f}"

        print()
        print("="*60)
        print(message)
        print("="*60)
        print()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 监控完成！")
    print()

    # 显示历史记录示例
    print("="*60)
    print("价格历史记录 (模拟数据)")
    print("="*60)
    print()

    history_data = [
        {"name": "京东iPhone 15", "prices": [
            (datetime(2026, 3, 11, 22, 30), 6299.0),
            (datetime(2026, 3, 11, 22, 35), 6199.0),
            (datetime(2026, 3, 11, 22, 40), 6109.0),
            (datetime(2026, 3, 11, 22, 45), 5999.0),
        ]},
        {"name": "京东小米14", "prices": [
            (datetime(2026, 3, 11, 22, 30), 3999.0),
            (datetime(2026, 3, 11, 22, 35), 3999.0),
            (datetime(2026, 3, 11, 22, 40), 3899.0),
        ]}
    ]

    for product in history_data:
        print(f"{product['name']}:")
        print(f"{'时间':<20} {'价格':<10}")
        print("-" * 30)

        for timestamp, price in product["prices"]:
            time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{time_str:<20} ￥{price:>7.2f}")

        print()

    print("="*60)
    print("演示完成！")
    print("="*60)
    print()
    print("使用说明:")
    print("  1. 编辑 config.json 添加需要监控的商品")
    print("  2. 运行: python monitor.py")
    print("  3. 持续监控: python monitor.py -c")
    print("  4. 查看历史: python monitor.py -h")
    print()


if __name__ == "__main__":
    main()
