# -*- coding: utf-8 -*-
"""
知乎爬虫主入口
提供简单的命令行接口
"""

import argparse
import sys
from pathlib import Path

from zhihu_scraper import ZhihuScraper, TOPIC_IDS
from data_exporter import DataExporter
from analyzer import DataAnalyzer


def cmd_search(args):
    """搜索问题命令"""
    print(f"🔍 搜索关键词: {args.keyword}")

    scraper = ZhihuScraper()
    questions = scraper.search_questions(args.keyword, limit=args.limit)

    print(f"✓ 找到 {len(questions)} 个相关问题\n")

    for i, q in enumerate(questions, 1):
        print(f"{i}. {q['title']}")
        print(f"   ID: {q['question_id']}")
        print(f"   链接: {q['url']}")
        print()

    # 导出到文件
    if args.export:
        exporter = DataExporter()
        exporter.export_questions(questions, f"search_{args.keyword}")
        print(f"✓ 数据已导出")

    scraper.close()


def cmd_detail(args):
    """获取问题详情命令"""
    print(f"📄 获取问题详情 (ID: {args.question_id})")

    scraper = ZhihuScraper()
    detail = scraper.get_question_detail(args.question_id)

    if detail:
        print("\n✓ 问题详情:")
        print(f"标题: {detail['title']}")
        print(f"作者: {detail['author']}")
        print(f"描述: {detail['description'][:200]}...")
        print(f"回答数: {detail['answer_count']}")
        print(f"关注数: {detail['follower_count']}")
        print(f"浏览量: {detail['visited_count']}")
        print(f"创建时间: {detail['created_time']}")
        print(f"链接: {detail['url']}")

        # 导出
        if args.export:
            exporter = DataExporter()
            exporter.export_questions([detail], f"detail_{args.question_id}")
            print(f"\n✓ 数据已导出")
    else:
        print("✗ 无法获取问题详情")
        sys.exit(1)

    scraper.close()


def cmd_answers(args):
    """获取回答命令"""
    print(f"💬 获取问题回答 (ID: {args.question_id})")

    scraper = ZhihuScraper()

    if args.all:
        print(f"📋 获取所有回答（最多 {args.limit} 个）")
        answers = scraper.get_all_answers(args.question_id, max_answers=args.limit)
    else:
        print(f"📋 获取前 {args.limit} 个回答")
        answers = scraper.get_question_answers(args.question_id, limit=args.limit)

    print(f"✓ 获取到 {len(answers)} 个回答\n")

    # 排序显示
    if args.sort == 'votes':
        answers_sorted = sorted(answers, key=lambda x: x['voteup_count'], reverse=True)
        print("📊 按点赞数排序:")
    else:
        answers_sorted = answers
        print("📊 按默认顺序:")

    for i, answer in enumerate(answers_sorted[:args.display], 1):
        print(f"{i}. 作者: {answer['author']}")
        print(f"   点赞: {answer['voteup_count']} | 评论: {answer['comment_count']}")
        print(f"   内容: {answer['content'][:80]}...")
        print()

    # 导出
    if args.export:
        exporter = DataExporter()
        exporter.export_answers(answers, args.question_id)
        print(f"✓ 回答数据已导出")

    # 分析
    if args.analyze and answers:
        analyzer = DataAnalyzer()
        report = analyzer.analyze_answers(answers)
        text_report = analyzer.generate_text_report(report, 'answers')
        print("\n📊 分析报告:")
        print(text_report)

    scraper.close()


def cmd_topic(args):
    """按话题获取问题命令"""
    topic_name = args.topic
    topic_id = TOPIC_IDS.get(topic_name)

    if not topic_id:
        print(f"✗ 未知话题: {topic_name}")
        print(f"可用话题: {', '.join(TOPIC_IDS.keys())}")
        sys.exit(1)

    print(f"📁 话题: {topic_name} (ID: {topic_id})")

    scraper = ZhihuScraper()
    questions = scraper.get_topic_questions(topic_id, limit=args.limit)

    print(f"✓ 找到 {len(questions)} 个热门问题\n")

    for i, q in enumerate(questions, 1):
        print(f"{i}. {q.get('title', 'N/A')}")
        print(f"   链接: {q.get('url', 'N/A')}")
        print()

    # 导出
    if args.export:
        exporter = DataExporter()
        exporter.export_questions(questions, f"topic_{topic_name}")
        print(f"✓ 数据已导出")

    scraper.close()


def cmd_list_topics(args):
    """列出所有可用话题"""
    print("📋 可用话题列表:")
    print("=" * 40)

    for name, topic_id in TOPIC_IDS.items():
        print(f"  {name}: {topic_id}")

    print(f"\n共 {len(TOPIC_IDS)} 个话题")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='知乎爬虫 - 搜索问题、获取详情、抓取回答',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py search "人工智能" --limit 5 --export
  python main.py detail 27446676 --export
  python main.py answers 27446676 --all --limit 50 --export --analyze
  python main.py topic 技术 --limit 10 --export
  python main.py list-topics
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 搜索命令
    search_parser = subparsers.add_parser('search', help='搜索问题')
    search_parser.add_argument('keyword', help='搜索关键词')
    search_parser.add_argument('--limit', type=int, default=10, help='返回结果数量（默认: 10）')
    search_parser.add_argument('--export', action='store_true', help='导出数据')
    search_parser.set_defaults(func=cmd_search)

    # 问题详情命令
    detail_parser = subparsers.add_parser('detail', help='获取问题详情')
    detail_parser.add_argument('question_id', help='问题ID')
    detail_parser.add_argument('--export', action='store_true', help='导出数据')
    detail_parser.set_defaults(func=cmd_detail)

    # 回答命令
    answers_parser = subparsers.add_parser('answers', help='获取问题回答')
    answers_parser.add_argument('question_id', help='问题ID')
    answers_parser.add_argument('--limit', type=int, default=20, help='最大回答数量（默认: 20）')
    answers_parser.add_argument('--all', action='store_true', help='获取所有回答（分页）')
    answers_parser.add_argument('--sort', choices=['default', 'votes'], default='default',
                               help='排序方式: default（默认）| votes（按点赞）')
    answers_parser.add_argument('--display', type=int, default=10, help='显示数量（默认: 10）')
    answers_parser.add_argument('--export', action='store_true', help='导出数据')
    answers_parser.add_argument('--analyze', action='store_true', help='生成分析报告')
    answers_parser.set_defaults(func=cmd_answers)

    # 话题命令
    topic_parser = subparsers.add_parser('topic', help='按话题获取问题')
    topic_parser.add_argument('topic', help='话题名称（技术/生活/娱乐等）')
    topic_parser.add_argument('--limit', type=int, default=10, help='返回结果数量（默认: 10）')
    topic_parser.add_argument('--export', action='store_true', help='导出数据')
    topic_parser.set_defaults(func=cmd_topic)

    # 列出话题命令
    topics_parser = subparsers.add_parser('list-topics', help='列出所有可用话题')
    topics_parser.set_defaults(func=cmd_list_topics)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n\n⚠️  操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
