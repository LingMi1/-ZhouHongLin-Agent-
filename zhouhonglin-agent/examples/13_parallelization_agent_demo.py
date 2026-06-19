"""
并行化 Agent 演示

这个示例展示如何使用并行化 Agent 来同时执行多个任务，
提高效率并获得多角度的分析结果。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.zhouhonglin_agent.gitee_ai_client import GiteeAIClient
from src.zhouhonglin_agent.agents.parallelization_agent import (
    ParallelizationAgent,
    ParallelStrategy,
    AggregationMethod,
    ParallelTask,
    MultiPerspectiveAnalysis,
    ParallelTranslation,
    ParallelContentGeneration,
    ParallelCodeReview,
    ParallelResearch,
    ConsensusGenerator
)


def print_separator(title=""):
    """打印分隔线"""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    else:
        print(f"\n{'-'*70}\n")


def demo_multi_perspective_analysis():
    """演示：多角度分析"""
    print_separator("📊 演示1：多角度分析")
    
    llm_client = GiteeAIClient()
    agent = ParallelizationAgent(llm_client=llm_client, max_workers=5, verbose=True)
    
    # 分析主题
    topic = "开发一个基于AI的智能代码审查工具"
    
    print(f"分析主题: {topic}\n")
    
    # 创建多角度分析任务
    tasks = MultiPerspectiveAnalysis.create_tasks(
        topic,
        perspectives=[
            "技术可行性分析",
            "市场需求分析",
            "商业价值评估",
            "用户体验设计",
            "风险和挑战"
        ]
    )
    
    # 执行并行分析
    result = agent.execute_parallel(
        tasks,
        strategy=ParallelStrategy.FULL_PARALLEL,
        aggregation=AggregationMethod.SUMMARIZE
    )
    
    # 显示结果
    if result.success_count > 0:
        print(f"\n✅ 并行分析完成！")
        print(f"   - 成功任务: {result.success_count}/{len(tasks)}")
        print(f"   - 并行耗时: {result.parallel_time:.2f}秒")
        print(f"   - 总耗时: {result.total_time:.2f}秒")
        print(f"\n📝 综合分析结果:\n")
        print(result.aggregated_result)
        
        # 显示各个角度的独立结果
        print(f"\n📋 各角度详细分析:")
        for task_result in result.task_results:
            if task_result.success:
                print(f"\n【{task_result.task_name}】")
                print(f"{task_result.output[:200]}...")  # 只显示前200字符
    else:
        print(f"❌ 所有任务都失败了")


def demo_parallel_translation():
    """演示：并行翻译"""
    print_separator("🌍 演示2：并行翻译")
    
    llm_client = GiteeAIClient()
    agent = ParallelizationAgent(llm_client=llm_client, max_workers=5, verbose=True)
    
    # 要翻译的文本
    text = "我们的新产品采用了最先进的人工智能技术，能够实时分析用户行为并提供个性化建议。"
    
    print(f"原文: {text}\n")
    
    # 创建并行翻译任务
    tasks = ParallelTranslation.create_tasks(
        text,
        target_languages=["英语", "日语", "法语", "德语"]
    )
    
    # 执行并行翻译
    result = agent.execute_parallel(
        tasks,
        strategy=ParallelStrategy.FULL_PARALLEL,
        aggregation=AggregationMethod.MERGE
    )
    
    # 显示结果
    if result.success_count > 0:
        print(f"\n✅ 翻译完成！")
        print(f"   - 成功翻译: {result.success_count}/{len(tasks)} 种语言")
        print(f"   - 耗时: {result.parallel_time:.2f}秒\n")
        
        print(f"📝 翻译结果:")
        for task_result in result.task_results:
            if task_result.success:
                lang = task_result.task_name.replace("翻译_", "")
                print(f"\n【{lang}】")
                print(task_result.output)


def demo_parallel_content_generation():
    """演示：并行内容生成"""
    print_separator("📝 演示3：并行内容生成")
    
    llm_client = GiteeAIClient()
    agent = ParallelizationAgent(llm_client=llm_client, max_workers=5, verbose=True)
    
    # 文档主题
    topic = "Python 异步编程入门"
    
    print(f"文档主题: {topic}\n")
    
    # 创建并行内容生成任务
    tasks = ParallelContentGeneration.create_tasks(
        topic,
        sections=[
            "简介和背景",
            "核心概念",
            "实践示例",
            "最佳实践"
        ]
    )
    
    # 执行并行生成
    result = agent.execute_parallel(
        tasks,
        strategy=ParallelStrategy.FULL_PARALLEL,
        aggregation=AggregationMethod.CONCAT
    )
    
    # 显示结果
    if result.success_count > 0:
        print(f"\n✅ 文档生成完成！")
        print(f"   - 成功章节: {result.success_count}/{len(tasks)}")
        print(f"   - 耗时: {result.parallel_time:.2f}秒\n")
        
        print(f"📄 完整文档:\n")
        print(result.aggregated_result)


def demo_parallel_code_review():
    """演示：并行代码审查"""
    print_separator("👨‍💻 演示4：并行代码审查")
    
    llm_client = GiteeAIClient()
    agent = ParallelizationAgent(llm_client=llm_client, max_workers=5, verbose=True)
    
    # 要审查的代码
    code = """
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

# 使用示例
numbers = [1, -2, 3, 4, -5]
processed = process_data(numbers)
print(processed)
"""
    
    print(f"待审查代码:\n{code}\n")
    
    # 创建并行代码审查任务
    tasks = ParallelCodeReview.create_tasks(code)
    
    # 执行并行审查
    result = agent.execute_parallel(
        tasks,
        strategy=ParallelStrategy.FULL_PARALLEL,
        aggregation=AggregationMethod.SUMMARIZE
    )
    
    # 显示结果
    if result.success_count > 0:
        print(f"\n✅ 代码审查完成！")
        print(f"   - 审查维度: {result.success_count}/{len(tasks)}")
        print(f"   - 耗时: {result.parallel_time:.2f}秒\n")
        
        print(f"📊 综合审查报告:\n")
        print(result.aggregated_result)


def demo_parallel_research():
    """演示：并行研究"""
    print_separator("🔬 演示5：并行研究")
    
    llm_client = GiteeAIClient()
    agent = ParallelizationAgent(llm_client=llm_client, max_workers=5, verbose=True)
    
    # 研究问题
    question = "区块链技术在供应链管理中的应用"
    
    print(f"研究问题: {question}\n")
    
    # 创建并行研究任务
    tasks = ParallelResearch.create_tasks(
        question,
        aspects=[
            "技术原理",
            "应用场景",
            "成功案例",
            "面临挑战"
        ]
    )
    
    # 执行并行研究
    result = agent.execute_parallel(
        tasks,
        strategy=ParallelStrategy.FULL_PARALLEL,
        aggregation=AggregationMethod.SUMMARIZE
    )
    
    # 显示结果
    if result.success_count > 0:
        print(f"\n✅ 研究完成！")
        print(f"   - 研究方面: {result.success_count}/{len(tasks)}")
        print(f"   - 耗时: {result.parallel_time:.2f}秒\n")
        
        print(f"📚 研究综述:\n")
        print(result.aggregated_result)


def demo_consensus_generation():
    """演示：共识生成"""
    print_separator("🤝 演示6：共识生成")
    
    llm_client = GiteeAIClient()
    agent = ParallelizationAgent(llm_client=llm_client, max_workers=5, verbose=True)
    
    # 问题
    prompt = "如何设计一个高性能的分布式缓存系统？"
    
    print(f"问题: {prompt}\n")
    print("通过多次生成寻找最佳答案...\n")
    
    # 创建共识生成任务
    tasks = ConsensusGenerator.create_tasks(
        prompt,
        num_generations=5
    )
    
    # 执行并寻找共识
    result = agent.execute_parallel(
        tasks,
        strategy=ParallelStrategy.FULL_PARALLEL,
        aggregation=AggregationMethod.CONSENSUS
    )
    
    # 显示结果
    if result.success_count > 0:
        print(f"\n✅ 共识生成完成！")
        print(f"   - 生成次数: {result.success_count}/{len(tasks)}")
        print(f"   - 耗时: {result.parallel_time:.2f}秒\n")
        
        print(f"💡 共识答案:\n")
        print(result.aggregated_result)


def demo_custom_parallel_tasks():
    """演示：自定义并行任务"""
    print_separator("⚙️ 演示7：自定义并行任务")
    
    llm_client = GiteeAIClient()
    agent = ParallelizationAgent(llm_client=llm_client, max_workers=3, verbose=True)
    
    # 自定义处理器
    def analyze_pros(input_data, llm_client):
        prompt = f"请列出'{input_data}'的主要优点（3-5点）："
        return llm_client.chat(prompt)
    
    def analyze_cons(input_data, llm_client):
        prompt = f"请列出'{input_data}'的主要缺点（3-5点）："
        return llm_client.chat(prompt)
    
    def analyze_alternatives(input_data, llm_client):
        prompt = f"请推荐'{input_data}'的3个替代方案："
        return llm_client.chat(prompt)
    
    # 创建自定义任务
    topic = "使用微服务架构"
    
    tasks = [
        ParallelTask(
            name="优点分析",
            handler=analyze_pros,
            input_data=topic,
            description="分析优点"
        ),
        ParallelTask(
            name="缺点分析",
            handler=analyze_cons,
            input_data=topic,
            description="分析缺点"
        ),
        ParallelTask(
            name="替代方案",
            handler=analyze_alternatives,
            input_data=topic,
            description="推荐替代方案"
        )
    ]
    
    print(f"分析主题: {topic}\n")
    
    # 执行并行任务
    result = agent.execute_parallel(
        tasks,
        strategy=ParallelStrategy.FULL_PARALLEL,
        aggregation=AggregationMethod.MERGE
    )
    
    # 显示结果
    if result.success_count > 0:
        print(f"\n✅ 分析完成！")
        print(f"   - 完成任务: {result.success_count}/{len(tasks)}")
        print(f"   - 耗时: {result.parallel_time:.2f}秒\n")
        
        print(f"📊 分析结果:")
        for task_name, output in result.aggregated_result.items():
            print(f"\n【{task_name}】")
            print(output)


def demo_strategy_comparison():
    """演示：不同策略的对比"""
    print_separator("⚡ 演示8：并行策略对比")
    
    llm_client = GiteeAIClient()
    
    # 创建一组简单任务
    def simple_task(data, llm):
        import time
        time.sleep(2)  # 模拟耗时操作
        return f"处理完成: {data}"
    
    tasks = [
        ParallelTask(f"任务{i}", simple_task, f"数据{i}", f"处理数据{i}")
        for i in range(1, 7)
    ]
    
    print("创建了6个任务，每个任务耗时2秒\n")
    
    # 测试不同策略
    strategies = [
        (ParallelStrategy.FULL_PARALLEL, "全并行"),
        (ParallelStrategy.BATCH_PARALLEL, "批量并行（每批3个）")
    ]
    
    for strategy, name in strategies:
        print(f"\n🔄 测试策略: {name}")
        agent = ParallelizationAgent(llm_client=llm_client, max_workers=3, verbose=False)
        
        result = agent.execute_parallel(
            tasks,
            strategy=strategy,
            aggregation=AggregationMethod.MERGE,
            batch_size=3
        )
        
        print(f"   ✅ 完成！耗时: {result.parallel_time:.2f}秒")
        print(f"   📊 成功: {result.success_count}, 失败: {result.failed_count}")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("  🚀 并行化 Agent 演示")
    print("="*70)
    
    demos = [
        ("1", "多角度分析", demo_multi_perspective_analysis),
        ("2", "并行翻译", demo_parallel_translation),
        ("3", "并行内容生成", demo_parallel_content_generation),
        ("4", "并行代码审查", demo_parallel_code_review),
        ("5", "并行研究", demo_parallel_research),
        ("6", "共识生成", demo_consensus_generation),
        ("7", "自定义任务", demo_custom_parallel_tasks),
        ("8", "策略对比", demo_strategy_comparison),
        ("0", "运行所有演示", None)
    ]
    
    print("\n请选择要运行的演示：")
    for num, name, _ in demos:
        print(f"  [{num}] {name}")
    
    choice = input("\n请输入选项（默认1）: ").strip() or "1"
    
    if choice == "0":
        # 运行所有演示
        for num, name, demo_func in demos:
            if num != "0" and demo_func:
                try:
                    demo_func()
                    input("\n按回车键继续下一个演示...")
                except KeyboardInterrupt:
                    print("\n\n用户中断")
                    break
                except Exception as e:
                    print(f"\n❌ 演示出错: {e}")
                    import traceback
                    traceback.print_exc()
    else:
        # 运行选定的演示
        for num, name, demo_func in demos:
            if num == choice and demo_func:
                try:
                    demo_func()
                except Exception as e:
                    print(f"\n❌ 演示出错: {e}")
                    import traceback
                    traceback.print_exc()
                break
        else:
            print(f"❌ 无效的选项: {choice}")
    
    print("\n" + "="*70)
    print("  ✅ 演示结束")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

