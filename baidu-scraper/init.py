#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目初始化脚本
检查依赖并创建必要的目录
"""

import os
import sys
import subprocess


def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python版本过低，需要Python 3.8或更高版本")
        return False
    print("✅ Python版本符合要求")
    return True


def check_dependencies():
    """检查依赖包"""
    print("\n检查依赖包...")
    
    required = {
        'requests': '>=2.31.0',
        'bs4': '>=4.12.0',
        'lxml': '>=4.9.0'
    }
    
    missing = []
    for package, version in required.items():
        try:
            __import__(package)
            print(f"✅ {package} {version}")
        except ImportError:
            print(f"❌ {package} {version} 未安装")
            missing.append(package)
    
    return missing


def install_dependencies(missing):
    """安装缺失的依赖"""
    if not missing:
        return True
    
    print(f"\n需要安装以下包: {', '.join(missing)}")
    print("正在安装...")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖包安装失败")
        print("请手动运行: pip install -r requirements.txt")
        return False


def create_directories():
    """创建必要的目录"""
    print("\n创建必要的目录...")
    
    directories = ['output', 'examples', 'test_output']
    
    for dir_name in directories:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✅ 创建目录: {dir_name}")
        else:
            print(f"📁 目录已存在: {dir_name}")


def check_files():
    """检查项目文件"""
    print("\n检查项目文件...")
    
    required_files = [
        'baidu_scraper.py',
        'exporter.py',
        'analyzer.py',
        'demo.py',
        'test.py',
        'example.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_exist = True
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} 缺失")
            all_exist = False
    
    return all_exist


def main():
    """主函数"""
    print("\n" + "="*80)
    print("🚀 百度百科爬虫 - 项目初始化")
    print("="*80)
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 检查项目文件
    if not check_files():
        print("\n❌ 项目文件不完整，请重新下载")
        return False
    
    # 检查依赖
    missing = check_dependencies()
    if missing:
        if not install_dependencies(missing):
            return False
    
    # 创建目录
    create_directories()
    
    # 完成
    print("\n" + "="*80)
    print("✅ 初始化完成!")
    print("="*80)
    print("\n可以开始使用项目了:")
    print("  运行演示: python demo.py")
    print("  运行测试: python test.py")
    print("  查看示例: python example.py")
    print("\n详细文档请查看 README.md")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
