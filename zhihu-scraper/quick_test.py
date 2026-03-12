# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证项目基本功能
"""

import sys
import os
from pathlib import Path

# 设置输出编码为UTF-8（针对Windows）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("🧪 知乎爬虫快速测试")
print("=" * 60)

# 检查文件是否存在
required_files = [
    'config.py',
    'zhihu_scraper.py',
    'data_exporter.py',
    'analyzer.py',
    'demo.py',
    'test.py',
    'main.py',
    'requirements.txt',
    'README.md',
]

print("\n📁 检查项目文件...")
all_exist = True
for filename in required_files:
    filepath = Path(filename)
    if filepath.exists():
        print(f"  ✓ {filename}")
    else:
        print(f"  ✗ {filename} (缺失)")
        all
_exist = False

if not all_exist:
    print("\n❌ 部分文件缺失，请检查项目完整性")
    sys.exit(1)

print("\n✅ 所有必需文件存在")

# 测试导入模块
print("\n🔧 测试模块导入...")
try:
    from config import USER_AGENTS, DEFAULT_HEADERS
    print(f"  ✓ config.py (包含 {len(USER_AGENTS)} 个User-Agent)")
except Exception as e:
    print(f"  ✗ config.py 导入失败: {e}")
    sys.exit(1)

try:
    from zhihu_scraper import ZhihuScraper, TOPIC_IDS
    print(f"  ✓ zhihu_scraper.py (支持 {len(TOPIC_IDS)} 个话题)")
except Exception as e:
    print(f"  ✗ zhihu_scraper.py 导入失败: {e}")
    sys.exit(1)

try:
    from data_exporter import DataExporter
    print(f"  ✓ data_exporter.py")
except Exception as e:
    print(f"  ✗ data_exporter.py 导入失败: {e}")
    sys.exit(1)

try:
    from analyzer import DataAnalyzer
    print(f"  ✓ analyzer.py")
except Exception as e:
    print(f"  ✗ analyzer.py 导入失败: {e}")
    sys.exit(1)

print("\n✅ 所有模块导入成功")

# 测试基本功能
print("\n⚡ 测试基本功能...")
try:
    scraper = ZhihuScraper()
    print("  ✓ 创建爬虫实例")

    print("  • 测试搜索功能（可能需要几秒钟）...")
    questions = scraper.search_questions("测试", limit=2)
    if isinstance(questions, list):
        print(f"  ✓ 搜索功能正常，返回 {len(questions)} 个结果")
    else:
        print(f"  ✗ 搜索功能返回类型错误")
        sys.exit(1)

    scraper.close()
    print("  ✓ 关闭爬虫实例")

except Exception as e:
    print(f"  ✗ 功能测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ 基本功能测试通过")

# 测试数据导出
print("\n💾 测试数据导出...")
try:
    exporter = DataExporter('output/test')
    print("  ✓ 创建导出器实例")

    test_data = [{'id': 1, 'name': '测试'}]
    json_path = exporter.export_to_json(test_data, 'test_quick')
    if Path(json_path).exists():
        print(f"  ✓ JSON导出功能正常")
    else:
        print(f"  ✗ JSON文件未创建")
        sys.exit(1)

    csv_path = exporter.export_to_csv(test_data, 'test_quick')
    if Path(csv_path).exists():
        print(f"  ✓ CSV导出功能正常")
    else:
        print(f"  ✗ CSV文件未创建")
        sys.exit(1)

except Exception as e:
    print(f"  ✗ 数据导出测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ 数据导出测试通过")

# 总结
print("\n" + "=" * 60)
print("🎉 所有测试通过！")
print("=" * 60)
print("\n📝 下一步:")
print("  1. 运行完整测试: python test.py")
print("  2. 运行演示: python demo.py")
print("  3. 查看帮助: python main.py --help")
print("  4. 阅读文档: README.md")
print("\n✨ 项目已就绪，可以开始使用！")
