#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证爬虫基本功能（简化版，避免控制台编码问题）
"""

import sys
import os

def main():
    """主测试函数"""
    print('=' * 60)
    print('微博热搜爬虫 - 快速测试')
    print('=' * 60)
    print()
    
    try:
        print('[1/4] 测试模块导入...')
        from weibo_hot_search import WeiboHotSearchScraper
        print('OK')
        
        print('[2/4] 测试爬虫初始化...')
        scraper = WeiboHotSearchScraper(delay_range=(1, 2))
        print('OK')
        
        print('[3/4] 测试数据获取...')
        data = scraper.fetch_hot_search()
        if data:
            print(f'OK - 获取到 {len(data)} 条热搜')
            print(f'示例: {data[0]["标题"][:30]}...')
        else:
            print('WARNING - 未获取到数据（可能是网络问题）')
            return False
        
        print('[4/4] 测试Excel导出...')
        test_file = 'test_output.xlsx'
        if os.path.exists(test_file):
            os.remove(test_file)
        scraper.export_to_excel(data, test_file)
        if os.path.exists(test_file):
            print('OK - 文件已创建')
            os.remove(test_file)
        else:
            print('FAIL - 文件未创建')
            return False
        
        print()
        print('=' * 60)
        print('所有测试通过!')
        print('=' * 60)
        return True
        
    except Exception as e:
        print(f'ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
