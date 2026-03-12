"""
新浪微博爬虫演示脚本
展示各个功能的使用方法
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api import WeiboAPI
from src.exporter import DataExporter
from src.analyzer import DataAnalyzer
from src.user import WeiboUser
from src.weibo import WeiboPost
import logging

# 设置日志级别
logging.basicConfig(level=logging.INFO)


def demo_user_info():
    """演示：获取用户信息"""
    print("\n" + "="*80)
    print("演示1：获取用户信息")
    print("="*80)

    api = WeiboAPI()

    # 注意：这里使用示例用户ID，实际使用时需要替换为真实用户ID
    # 由于微博需要登录才能访问，这里演示数据结构
    user = WeiboUser(
        user_id='123456789',
        username='示例用户',
        fans_count=10000,
        follow_count=500,
        weibo_count=1000,
        bio='这是一个示例用户简介',
        verified=True,
        verified_type='个人认证',
        location='北京',
        gender='女'
    )

    print(f"用户名: {user.username}")
    print(f"粉丝数: {user.fans_count:,}")
    print(f"关注数: {user.follow_count:,}")
    print(f"微博数: {user.weibo_count:,}")
    print(f"简介: {user.bio}")
    print(f"认证: {user.verified} ({user.verified_type})")
    print(f"位置: {user.location}")
    print(f"性别: {user.gender}")

    api.close()
    return [user]


def demo_posts():
    """演示：微博帖子"""
    print("\n" + "="*80)
    print("演示2：微博帖子数据")
    print("="*80)

    # 创建示例帖子数据
    posts = [
        WeiboPost(
            post_id='001',
            user_id='123456789',
            username='示例用户',
            content='今天天气真好！#生活 #心情',
            created_at='2024-01-15 10:00:00',
            likes=100,
            comments=20,
            reposts=5,
            images=['https://example.com/image1.jpg'],
            topics=['生活', '心情']
        ),
        WeiboPost(
            post_id='002',
            user_id='123456789',
            username='示例用户',
            content='转发了一条有趣的内容',
            created_at='2024-01-15 11:00:00',
            likes=50,
            comments=10,
            reposts=2,
            is_repost=True,
            original_post_id='999'
        ),
        WeiboPost(
            post_id='003',
            user_id='987654321',
            username='另一个用户',
            content='推荐一部好电影 #电影 推荐',
            created_at='2024-01-15 12:00:00',
            likes=200,
            comments=40,
            reposts=15,
            topics=['电影']
        ),
        WeiboPost(
            post_id='004',
            user_id='987654321',
            username='另一个用户',
            content='科技新闻：人工智能发展迅速 #科技 #AI',
            created_at='2024-01-15 13:00:00',
            likes=500,
            comments=100,
            reposts=50,
            topics=['科技', 'AI']
        ),
        WeiboPost(
            post_id='005',
            user_id='111222333',
            username='娱乐博主',
            content='最新明星动态 #娱乐',
            created_at='2024-01-15 14:00:00',
            likes=1000,
            comments=200,
            reposts=100,
            topics=['娱乐']
        )
    ]

    print(f"创建 {len(posts)} 条示例微博：\n")

    for i, post in enumerate(posts, 1):
        print(f"{i}. {post.username}: {post.content[:50]}{'...' if len(post.content) > 50 else ''}")
        print(f"   点赞: {post.likes} | 评论: {post.comments} | 转发: {post.reposts}")
        if post.topics:
            print(f"   话题: {', '.join(f'#{t}' for t in post.topics)}")
        print()

    return posts


def demo_export(users, posts):
    """演示：数据导出"""
    print("\n" + "="*80)
    print("演示3：数据导出（CSV和JSON）")
    print("="*80)

    exporter = DataExporter('data')

    # 导出用户数据
    print("导出用户数据...")
    csv_path = exporter.export_users(users, format='csv')
    json_path = exporter.export_users(users, format='json')
    print(f"  CSV: {csv_path}")
    print(f"  JSON: {json_path}")

    # 导出帖子数据
    print("\n导出帖子数据...")
    csv_path = exporter.export_posts(posts, format='csv')
    json_path = exporter.export_posts(posts, format='json')
    print(f"  CSV: {csv_path}")
    print(f"  JSON: {json_path}")


def demo_analysis(users, posts):
    """演示：数据分析"""
    print("\n" + "="*80)
    print("演示4：数据分析与可视化")
    print("="*80)

    analyzer = DataAnalyzer('data')

    # 用户分析
    print("\n用户数据分析...")
    user_analysis = analyzer.analyze_users(users)
    print(f"  总用户数: {user_analysis.get('total_users', 0)}")
    print(f"  认证用户: {user_analysis.get('verified_users', 0)}")
    print(f"  平均粉丝数: {user_analysis.get('fans_count_avg', 0):.2f}")

    # 帖子分析
    print("\n帖子数据分析...")
    post_analysis = analyzer.analyze_posts(posts)
    print(f"  总帖子数: {post_analysis.get('total_posts', 0)}")
    print(f"  原创帖子: {post_analysis.get('original_posts', 0)}")
    print(f"  转发帖子: {post_analysis.get('repost_posts', 0)}")
    print(f"  总点赞数: {post_analysis.get('likes_total', 0):,}")
    print(f"  总评论数: {post_analysis.get('comments_total', 0):,}")

    # 生成报告
    print("\n生成分析报告...")
    report_path = analyzer.generate_report(users, posts)
    print(f"  报告: {report_path}")

    # 生成图表
    print("\n生成可视化图表...")
    fans_plot = analyzer.plot_user_fans(users)
    if fans_plot:
        print(f"  粉丝排行图: {fans_plot}")

    interaction_plot = analyzer.plot_post_interaction(posts)
    if interaction_plot:
        print(f"  互动分布图: {interaction_plot}")


def demo_search():
    """演示：搜索功能"""
    print("\n" + "="*80)
    print("演示5：搜索微博（需要Cookie）")
    print("="*80)

    print("\n注意：实际搜索功能需要微博登录Cookie")
    print("以下是使用示例代码：")
    print("""
    api = WeiboAPI(cookie='your_cookie_here')

    # 搜索关键词
    posts = api.search_posts('人工智能', page=1, max_results=20)

    # 搜索话题标签
    hot_topics = api.get_hot_topics()

    # 获取用户帖子
    user_posts = api.get_user_posts('user_id', page=1, max_posts=20)

    api.close()
    """)


def demo_comment():
    """演示：评论获取"""
    print("\n" + "="*80)
    print("演示6：获取微博评论（需要Cookie）")
    print("="*80)

    print("\n注意：获取评论功能需要微博登录Cookie")
    print("以下是使用示例代码：")
    print("""
    api = WeiboAPI(cookie='your_cookie_here')

    # 获取帖子详情
    post = api.get_post_detail('post_id')

    # 获取评论
    comments = api.get_post_comments('post_id', max_comments=50)

    print(f"帖子: {post.content}")
    print(f"评论数: {len(comments)}")
    for comment in comments:
        print(f"  {comment['username']}: {comment['content']}")

    api.close()
    """)


def main():
    """主函数"""
    print("\n" + "="*80)
    print("新浪微博爬虫功能演示")
    print("="*80)

    try:
        # 演示1：用户信息
        users = demo_user_info()

        # 演示2：帖子数据
        posts = demo_posts()

        # 演示3：数据导出
        demo_export(users, posts)

        # 演示4：数据分析
        demo_analysis(users, posts)

        # 演示5：搜索功能（代码示例）
        demo_search()

        # 演示6：评论获取（代码示例）
        demo_comment()

        print("\n" + "="*80)
        print("演示完成！数据已保存到 data/ 目录")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\n演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
