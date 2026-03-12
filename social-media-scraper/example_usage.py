#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：如何使用导出的Excel数据
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os


def analyze_hot_search_excel(excel_file: str):
    """
    分析微博热搜Excel数据
    
    Args:
        excel_file: Excel文件路径
    """
    
    # 读取Excel文件
    df = pd.read_excel(excel_file)
    
    print('=' * 60)
    print('微博热搜数据分析')
    print('=' * 60)
    
    # 1. 显示基本信息
    print(f'\n【数据概览】')
    print(f'总热搜数: {len(df)} 条')
    print(f'文件名: {excel_file}')
    
    # 2. 显示前10条热搜
    print(f'\n【Top 10 热搜】')
    print(df.head(10)[['排名', '标题', '热度值']].to_string(index=False))
    
    # 3. 热度值统计
    print(f'\n【热度值统计】')
    # 转换热度值为数值（处理"万"等单位）
    def parse_hot_value(val):
        if pd.isna(val):
            return 0
        if isinstance(val, (int, float)):
            return val
        if '万' in str(val):
            return float(str(val).replace('万', '')) * 10000
        try:
            return float(str(val).replace(',', ''))
        except:
            return 0
    
    df['热度值_数值'] = df['热度值'].apply(parse_hot_value)
    
    print(f'平均热度: {df["热度值_数值"].mean():,.0f}')
    print(f'最高热度: {df["热度值_数值"].max():,.0f}')
    print(f'最低热度: {df["["热度值_数值"].min():,.0f}')
    
    # 4. 关键词分析示例
    keywords = ['经济', '科技', '娱乐', '体育', '国际']
    print(f'\n【关键词出现次数】')
    for keyword in keywords:
        count = df['标题'].str.contains(keyword, na=False).sum()
        print(f'{keyword}: {count} 次')
    
    # 5. 筛选特定热搜
    print(f'\n【筛选示例：包含"经济"的热搜】')
    economy_data = df[df['标题'].str.contains('经济', na=False)]
    if len(economy_data) > 0:
        print(economy_data[['排名', '标题', '热度值']].to_string(index=False))
    else:
        print('未找到包含"经济"的热搜')
    
    # 6. 按热度排序
    print(f'\n【按热度值排序（前5名）】')
    top5_by_hot = df.nlargest(5, '热度值_数值')
    print(top5_by_hot[['排名', '标题', '热度值']].to_string(index=False))
    
    print('\n' + '=' * 60)
    print('分析完成！')
    print('=' * 60)
    
    return df


def create_visualization(df: pd.DataFrame, output_file: str = 'hot_search_chart.png'):
    """
    创建数据可视化图表
    
    Args:
        df: 数据框
        output_file: 输出图片文件名
    """
    try:
        # 设置中文字体（Windows）
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 取前15条热搜
        top15 = df.head(15)
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 水平条形图
        y_pos = range(len(top15))
        ax.barh(y_pos, top15['热度值_数值'], color='skyblue')
        
        # 设置标签
        ax.set_yticks(y_pos)
        ax.set_yticklabels([f"{row['排名']}. {row['标题'][:20]}..." if len(row['标题']) > 20 
                            else f"{row['排名']}. {row['标题']}" 
                            for _, row in top15.iterrows()])
        
        ax.set_xlabel('热度值', fontsize=12)
        ax.set_title('微博热搜Top15热度值对比', fontsize=16, fontweight='bold')
        
        # 反转y轴，让排名1在顶部
        ax.invert_yaxis()
        
        # 添加数值标签
        for i, v in enumerate(top15['热度值_数值']):
            ax.text(v + max(top15['热度值_数值'])*0.01, i, f'{v:,.0f}', 
                   va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
")
        print(f'\n✅ 可视化图表已保存: {output_file}')
        
    except Exception as e:
        print(f'\n⚠️  生成图表失败: {e}')
        print('提示：确保已安装matplotlib: pip install matplotlib')


def main():
    """主函数"""
    print('\n微博热搜数据分析示例\n')
    
    # 查找最新的Excel文件
    import glob
    excel_files = glob.glob('weibo_hot_search_*.xlsx')
    
    if not excel_files:
        print('❌ 未找到Excel文件，请先运行 weibo_hot_search.py')
        print('\n运行命令: python weibo_hot_search.py')
        return
    
    # 使用最新的文件
    latest_file = max(excel_files, key=os.path.getctime)
    print(f'✅ 找到最新文件: {latest_file}')
    
    # 分析数据
    df = analyze_hot_search_excel(latest_file)
    
    # 创建可视化图表（可选）
    create_plot = input('\n是否生成可视化图表？(y/n): ').strip().lower()
    if create_plot == 'y':
        try:
            import matplotlib.pyplot as plt
            create_visualization(df)
        except ImportError:
            print('\n⚠️  未安装matplotlib，跳过图表生成')
            print('安装命令: pip install matplotlib')


if __name__ == '__main__':
    main()
