"""
新浪微博爬虫主入口
提供命令行接口
"""

import sys
import os
import argparse
from datetime import datetime

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api import WeiboAPI
from src.exporter import DataExporter
from src.analyzer import DataAnalyzer
from src.user import WeiboUser
from src.weibo import WeiboPost
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def cmd_user(args):
    """获取用户信息"""
    print(f"正在获取用户信息: {args.user_id}")

    api = WeiboAPI(cookie=args.cookie)

    user = api.get_user_info(args.user_id)
    if user:
        print("\n" + "="*60)
        print("用户信息")
        print("="*60)
        print(f"用户ID: {user.user_id}")
        print(f"用户名: {user.username}")
        print(f"昵称: {user.nickname}")
        print(f"粉丝数: {user.fans_count:,}")
        print(f"关注数: {user.follow_count:,}")
        print(f"微博数: {user.weibo_count:,}")
        print(f"简介: {user.bio}")
        print(f"认证: {'是' if user.verified else '否'} ({user.verified_type})")
        print(f"位置: {user.location}")
        print(f"性别: {user.gender}")
        print(f"主页: {user.url}")
        print("="*60)

        # 导出数据
        if args.export:
            exporter = DataExporter('data')
            filepath = exporter.export_users([user], format=args.format)
            print(f"\n数据已导出: {filepath}")

    else:
        print(f"获取用户信息失败: {args.user_id}")

    api.close()


def cmd_search(args):
    """搜索微博搜索: {args.keyword}")

    api = WeiboAPI(cookie=args.cookie)

    posts = api.search_posts(args.keyword, page=args.page, max_results=args.max_results)

    print(f"\n找到 {len(posts)} 条相关微博:\n")
    print("="*80)

    for i, post in enumerate(posts, 1):
        print(f"\n{i}. {post.username}")
        print(f"   时间: {post.created_at}")
        print(f"   内容: {post.content[:100]}{'...' if len(post.content) > 100 else ''}")
        print(f"   互动: {post.likes} 赞 | {post.comments} 评 | {post.reposts} 转")
        if post.topics:
            print(f"   话题: {', '.join(f'#{t}' for t in post.topics)}")

    print("="*80)

    # 导出数据
    if args.export and posts:
        exporter = DataExporter('data')
        filename = f'search_{args.keyword}_{datetime.now().strftime("%Y%m%d")}'
        filepath = exporter.export_posts(posts, filename, format=args.format)
        print(f"\n数据已导出: {filepath}")

    api.close()


def cmd_hot(args):
    """获取热搜话题")
    print("正在获取微博热搜...")

    api = WeiboAPI(cookie=args.cookie)

    topics = api.get_hot_topics()

    print(f"\n获取到 {len(topics)} 条热搜:\n")
    print("="*60)
    print(f"{'排名':<6}{'话题':<30}{'热度':<12}{'分类'}")
    print("-"*60)

    for topic in topics[:args.count]:
        print(f"{topic['rank']:<6}{topic['word']:<30}{str(topic['hot']):<12}{topic['category']}")

    print("="*60)

    api.close()


def cmd_analyze(args):
    """分析数据"""
    print("正在分析数据...")

    # 这里简单演示，实际应该从文件加载
    analyzer = DataAnalyzer('data')

    print("\n数据分析功能:")
    print("- 用户排行（粉丝数、微博数)")
    print("- 微博热度分析（点赞、评论、转发）")
    print("- 话题统计和热门话题")
    print("- 可视化图表生成")

    print("\n提示: 运行 examples/demo.py 查看完整演示")


def cmd_demo(args):
    """运行演示演示"""
print("运行演示脚本...")

import subprocess
demo_path = os.path.join(os.path.dirname(__file__), 'examples', 'demo.py')
subprocess.run([sys.executable, demo_path])


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='新浪微博爬虫 - 数据爬取和分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 获取用户信息
  python main.py user 123456789

  # 搜索微博
  python main.py search 人工智能 --max-results 20

  # 获取热搜话题
  python main.py hot --count 20

  # 运行演示
  python main.py demo

注意: 大部分功能需要登录Cookie，使用 --cookie 参数提供。
        """
    )

    # 全局参数
    parser.add_argument('--cookie', help='微博登录Cookie')
    parser.add_argument('--export', action='store_true', help='导出数据')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='导出格式 (默认: json)')

    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # user 命令
    user_parser = subparsers.add_parser('user', help='获取用户信息')
    user_parser.add_argument('user_id', help='用户ID或昵称')
    user_parser.set_defaults(func=cmd_user)

    # search 命令
    search_parser = subparsers.add_parser('search', help='搜索微博')
    search_parser.add_argument('keyword', help='搜索关键词')
    search_parser.add_argument('--page', type=int, default=1, help='页码 (默认: 1)')
    search_parser.add_argument('--max-results', type=int, default=20, help='最大结果数 (默认: 20)')
    search_parser.set_defaults(func=cmd_search)

    # hot 命令
    hot_parser = subparsers.add_parser('hot', help='获取热搜话题')
    hot_parser.add_argument('--count', type=int, default=20, help='显示数量 (默认: 20)')
    hot_parser.set_defaults(func=cmd_hot)

    # analyze 命令
    analyze_parser = subparsers.add_parser('analyze', help='分析数据')
    analyze_parser.set_defaults(func=cmd_analyze)

    # demo 命令
    demo_parser = subparsers.add_parser('demo', help='运行演示')
    demo_parser.set_defaults(func=cmd_demo)

    # 解析参数
    args = parser.parse_args()

    # 如果没有指定命令，显示帮助
    if not args.command:
        parser.print_help()
        return

    # 执行命令
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
    except Exception as e:
        logger.error(f"执行命令时出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
