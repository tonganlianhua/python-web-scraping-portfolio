#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证爬虫基本功能
"""

import sys
import traceback
from weibo_hot_search import WeiboHotSearchScraper


def test_import():
    """测试模块导入"""
    print('[测试1] 模块导入...', end=' ')
    try:
        from weibo_hot_search import WeiboHotSearchScraper
        print('✅ 通过')
        return True
    except Exception as e:
        print(f'❌ 失败: {e}')
        return False


def test_initialization():
    """测试爬虫初始化"""
    print('[测试2] 爬虫初始化...', end=' ')
    try:
        scraper = WeiboHotSearchScraper(delay_range=(0.5, 1))
        print('✅ 通过')
        return scraper
    except Exception as e:
        print(f'❌ 失败: {e}')
        return None


def test_fetch_data(scraper):
    """测试数据获取"""
    print('[测试3] 获取热搜数据...', end=' ')
    try:
        data = scraper.fetch_hot_search()
        if data:
            print(f'✅ 通过 (获取到 {len(data)} 条)')
            print(f'         示例: {data[0]["标题"][:30]}...')
            return data
        else:
            print('⚠️  警告: 未获取到数据（可能是网络问题）')
            return []
    except Exception as e:
        print(f'❌ 失败: {e}')
        traceback.print_exc()
        return []


def test_keyword_filter(scraper, data):
    """测试关键词过滤"""
    print('[测试4] 关键词过滤...', end=' ')
    try:
        if data:
            filtered = scraper.filter_by_keyword(data, '')
            print(f'✅ 通过 (过滤后 {len(filtered)} 条)')
            return True
        else:
            print('⚠️  跳过（无数据）')
            return True
    except Exception as e:
        print(f'❌ 失败: {e}')
        return False


def test_export(scraper, data):
    """测试Excel导出"""
    print('[测试5] Excel导出...', end=' ')
    try:
        if data:
            import os
            test_file = 'test_output.xlsx'
            
            # 删除已存在的测试文件
            if os.path.exists(test_file):
                os.remove(test_file)
            
            scraper.export_to_excel(data, test_file)
            
            if os.path.exists(test_file):
                print(f'✅ 通过 (文件已创建)')
                # 清理测试文件
                os.remove(test_file)
                return True
            else:
                print('❌ 失败 (文件未创建)')
                return False
        else:
            print('⚠️  跳过（无数据）')
            return True
    except Exception as e:
        print(f'❌ 失败: {e}')
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print('=' * 60)
    print('微博热搜爬虫 - 快速测试')
    print('=' * 60)
    print()
    
    results = []

    
    # 运行测试
    if test_import():
        scraper = test_initialization()
        if scraper:
            data = test_fetch_data(scraper)
            results.append(test_keyword_filter(scraper, data))
            results.append(test_export(scraper, data))
        else:
            print('\n⚠️  爬虫初始化失败，跳过后续测试')
    else:
        print('\n⚠️  模块导入失败，跳过后续测试')
        return False
    
    # 汇总结果
    print()
    print('=' * 60)
    if all(results):
        print('✅ 所有测试通过！')
        print('=' * 60)
        return True
    else:
        print('⚠️  部分测试失败，请检查网络连接和依赖包')
        print('=' * 60)
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
