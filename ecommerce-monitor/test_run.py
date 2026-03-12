#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证监控器基本功能
"""

import json
import os
import sys


def test_config():
    """测试配置文件加载"""
    print("测试 1: 配置文件加载")
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        print("[OK] 配置文件加载成功")
        print(f"   - 商品数量: {len(config.get('products', []))}")
        print(f"   - 监控间隔: {config.get('settings', {}).get('check_interval', 300)} 秒")
        return True
    except Exception as e:
        print(f"[FAIL] 配置文件加载失败: {e}")
        return False


def test_imports():
    """测试依赖包导入"""
    print("\n测试 2: 依赖包导入")
    try:
        import requests
        print(f"[OK] requests 版本: {requests.__version__}")
    except ImportError:
        print("[FAIL] requests 未安装")
        return False

    try:
        from bs4 import BeautifulSoup
        print(f"[OK] beautifulsoup4 已安装")
    except ImportError:
        print("[FAIL] beautifulsoup4 未安装")
        return False

    try:
        import lxml
        print(f"[OK] lxml 已安装")
    except ImportError:
        print("[FAIL] lxml 未安装")
        return False

    return True


def test_monitor_class():
    """测试监控器类初始化"""
    print("\n测试 3: 监控器类初始化")
    try:
        from monitor import PriceMonitor
        monitor = PriceMonitor("config.json")
        print(f"[OK] 监控器初始化成功")
        print(f"   - 商品配置数: {len(monitor.products)}")
        print(f"   - 历史文件: {monitor.history_file}")
        return True
    except Exception as e:
        print(f"[FAIL] 监控器初始化失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("="*60)
    print("电商价格监控爬虫 - 功能测试")
    print("="*60)

    results = []

    # 测试1: 配置文件
    results.append(test_config())

    # 测试2: 依赖包
    results.append(test_imports())

    # 测试3: 监控器类
    results.append(test_monitor_class())

    # 汇总结果
    print("\n" + "="*60)
    print("测试汇总")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("\n[OK] 所有测试通过！项目可以正常运行。")
        print("\n使用方法:")
        print("  python monitor.py              # 单次监控")
        print("  python monitor.py -c           # 持续监控")
        print("  python monitor.py -h           # 查看历史")
        return 0
    else:
        print("\n[FAIL] 部分测试失败，请检查错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
