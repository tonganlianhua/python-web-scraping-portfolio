# -*- coding: utf-8 -*-
"""
知乎爬虫演示脚本
展示主要功能的使用方法
"""

import sys
import io

# 设置输出编码为UTF-8（针对Windows）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from zhihu_scraper import ZhihuScraper, TOPIC_IDS
from data_exporter import DataExporter
from analyzer import DataAnalyzer


def demo_search_questions():
    """演示：搜索问题"""
    print("\n" + "=" * 60)
    print("演示 1: 搜索问题")
    print("=" * 60)

    scraper = ZhihuScraper()

    # 搜索关键词
    keyword = "人工智能"
    print(f"\n🔍 搜索关键词: {keyword}")

    questions = scraper.search_questions(keyword, limit=5)
    print(f"✓ 找到 {len(questions)} 个相关问题")

    for i, q in enumerate(questions, 1):
        print(f"\n{i}. {q['title']}")
        print(f"   ID: {q['question_id']}")
        print(f"   链接: {q['url']}")

    scraper.close()
    return questions


def demo_get_topic_questions():
    """演示：获取话题
问题"""
    print("\n" + "=" * 60)
    print("演示 2: 获取话题问题")
    print("=" * 60)

    scraper = ZhihuScraper()

    # 选择话题
    topic_name = "技术"
    topic_id = TOPIC_IDS.get(topic_name)
    print(f"\n📁 话题: {topic_name} (ID: {topic_id})")

    questions = scraper.get_topic_questions(topic_id, limit=5)
    print(f"✓ 找到 {len(questions)} 个热门问题")

    for i, q in enumerate(questions, 1):
        print(f"\n{i}. {q.get('title', 'N/A')}")
        print(f"   话题: {q.get('topic', 'N/A')}")
        print(f"   链接: {q.get('url', 'N/A')}")

    scraper.close()
    return questions


def demo_get_question_detail():
    """演示：获取问题详情"""
    print("\n" + "=" * 60)
    print("演示 3: 获取问题详情")
    print("=" * 60)

    scraper = ZhihuScraper()

    # 使用一个示例问题ID
    question_id = "27446676"  # 一个已知的问题ID
    print(f"\n📄 问题ID: {question_id}")

    detail = scraper.get_question_detail(question_id)
    if detail:
        print("\n✓ 问题详情:")
        print(f"标题: {detail['title']}")
        print(f"作者: {detail['author']}")
        print(f"描述: {detail['description'][:100]}...")
        print(f"回答数: {detail['answer_count']}")
        print(f"关注数: {detail['follower_count']}")
        print(f"浏览量: {detail['visited_count']}")
        print(f"创建时间: {detail['created_time']}")
        print(f"链接: {detail['url']}")
    else:
        print("✗ 无法获取问题详情")

    scraper.close()
    return detail


def demo_get_answers():
    """演示：获取问题回答"""
    print("\n" + "=" * 60)
    print("演示 4: 获取问题回答")
    print("=" * 60)

    scraper = ZhihuScraper()

    # 使用一个示例问题ID
    question_id = "27446676"
    print(f"\n💬 问题ID: {question_id}")

    # 获取前5个回答
    answers = scraper.get_question_answers(question_id, limit=5)
    print(f"✓ 获取到 {len(answers)} 个回答")

    for i, answer in enumerate(answers, 1):
        print(f"\n{i}. 作者: {answer['author']}")
        print(f"   点赞数: {answer['voteup_count']} | 评论数: {answer['comment_count']}")
        print(f"   内容预览: {answer['content'][:100]}...")
        print(f"   创建时间: {answer['created_time']}")

    scraper.close()
    return answers


def demo_get_all_answers_pagination():
    """演示：分页获取所有回答"""
    print("\n" + "=" * 60)
    print("演示 5: 分页获取所有回答")
    print("=" * 60)

    scraper = ZhihuScraper()

    question_id = "27446676"
    max_answers = 50  # 最多获取50个回答
    print(f"\n📄 问题ID: {question_id}")
    print(f"📋 最大获取数量: {max_answers}")

    # 分页获取所有回答
    all_answers = scraper.get_all_answers(question_id, max_answers=max_answers)
    print(f"✓ 实际获取到 {len(all_answers)} 个回答")

    # 按点赞排序
    sorted_answers = sorted(all_answers, key=lambda x: x['voteup_count'], reverse=True)
    print("\n🏆 最受欢迎的回答:")
    for i, answer in enumerate(sorted_answers[:5], 1):
        print(f"{i}. {answer['author']} - {answer['voteup_count']} 赞")

    scraper.close()
    return all_answers


def demo_data_export():
    """演示：数据导出"""
    print("\n" + "=" * 60)
    print("演示 6: 数据导出")
    print("=" * 60)

    scraper = ZhihuScraper()
    exporter = DataExporter()

()

    # 获取一些问题数据
    question_id = "27446676"
    detail = scraper.get_question_detail(question_id)
    answers = scraper.get_question_answers(question_id, limit=10)

    print(f"\n📄 问题: {detail['title']}")
    print(f"📊 回答数量: {len(answers)}")

    # 导出问题详情
    if detail:
        print("\n💾 导出问题详情...")
        exporter.export_to_json([detail], f"question_detail_{question_id}")
        exporter.export_to_csv([detail], f"question_detail_{question_id}")

    # 导出回答
    if answers:
        print("💾 导出回答...")
        exporter.export_answers(answers, question_id)

    scraper.close()


def demo_data_analysis():
    """演示：数据分析"""
    print("\n" + "=" * 60)
    print("演示 7: 数据分析")
    print("=" * 60)

    scraper = ZhihuScraper()
    analyzer = DataAnalyzer()
    exporter = DataExporter()

    # 获取数据
    question_id = "27446676"
    detail = scraper.get_question_detail(question_id)
    answers = scraper.get_all_answers(question_id, max_answers=30)

    print(f"\n📄 问题: {detail['title']}")
    print(f"📊 分析 {len(answers)} 个回答...")

    # 生成分析报告
    report = analyzer.generate_comparison_report(detail, answers)

    # 生成文本报告
    text_report = analyzer.generate_text_report(report['answers_analysis'], 'answers')
    print("\n📋 分析报告:")
    print(text_report)

    # 保存报告
    print("\n💾 保存分析报告...")
    exporter.export_analysis_report(report, question_id)
    analyzer.save_text_report(text_report, f"output/question_{question_id}/report_{question_id}.txt")

    scraper.close()


def demo_full_workflow():
    """完整工作流演示"""
    print("\n" + "=" * 60)
    print("完整工作流演示")
    print("=" * 60)

    scraper = ZhihuScraper()
    analyzer = DataAnalyzer()
    exporter = DataExporter()

    # 1. 搜索问题
    print("\n1️⃣ 搜索问题...")
    questions = scraper.search_questions("Python编程", limit=3)

    if questions:
        # 2. 获取第一个问题的详情
        question_id = questions[0]['question_id']
        print(f"\n2️⃣ 获取问题详情 (ID: {question_id})...")
        detail = scraper.get_question_detail(question_id)

        if detail:
            print(f"   标题: {detail['title']}")
            print(f"   回答数: {detail['answer_count']}")

            # 3. 获取回答
            print(f"\n3️⃣ 获取回答 (最多20个)...")
            answers = scraper.get_all_answers(question_id, max_answers=20)

            # 4. 数据分析
            print(f"\n4️⃣ 分析数据...")
            report = analyzer.generate_comparison_report(detail, answers)

            # 5. 导出数据
            print(f"\n5️⃣ 导出数据...")
            exporter.export_questions([detail])
            exporter.export_answers(answers, question_id)
            exporter.export_analysis_report(report, question_id)

            # 6. 生成文本报告
            text_report = analyzer.generate_text_report(report['answers_analysis'], 'answers')
            analyzer.save_text_report(text_report, f"output/question_{question_id}/full_report.txt")

            print(f"\n✓ 完整工作流完成！")
            print(f"✓ 问题ID: {question_id}")
            print(f"✓ 获取回答数: {len(answers)}")

    scraper.close()


def main():
    """主函数 - 运行所有演示"""
    print("🚀 知乎爬虫演示开始")
    print("=" * 60)

    try:
        # 运行各个演示
        demo_search_questions()
        demo_get_topic_questions()
        demo_get_question_detail()
        demo_get_answers()
        demo_get_all_answers_pagination()
        demo_data_export()
        demo_data_analysis()
        demo_full_workflow()

        print("\n" + "=" * 60)
        print("✅ 所有演示完成！")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n⚠️  演示被用户中断")
    except Exception as e:
        print(f"\n\n❌ 演示过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
