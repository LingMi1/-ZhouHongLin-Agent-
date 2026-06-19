"""
Reflection Agent 示例 - 演示反思代理的各种功能

这个示例展示了如何使用 Reflection Agent 通过自我批判和迭代改进来提升输出质量。
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.zhouhonglin_agent.gitee_ai_client import GiteeAIClient
from src.zhouhonglin_agent.agents.reflection_agent import (
    ReflectionAgent,
    ReflectionStrategy,
    ContentReflection,
    CodeReflection,
    AnalysisReflection,
    TranslationReflection
)


def print_separator(title=""):
    """打印分隔线"""
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)
    print()


def demo_simple_reflection():
    """演示简单反思"""
    print_separator("示例 1: 简单反思 - 改进一篇短文")
    
    llm_client = GiteeAIClient()
    agent = ReflectionAgent(
        llm_client=llm_client,
        max_iterations=3,
        score_threshold=0.85,
        verbose=True
    )
    
    task = """写一篇关于"AI与人类协作"的短文，200字左右。"""
    
    result = agent.reflect_and_improve(
        task=task,
        strategy=ReflectionStrategy.SIMPLE
    )
    
    if result.success:
        print("\n✨ 最终优化后的内容：")
        print("-" * 60)
        print(result.final_content)
        print("-" * 60)
        print(f"\n📊 统计信息：")
        print(f"  - 总迭代次数: {result.total_iterations}")
        print(f"  - 最终评分: {result.final_score:.2f}")
        print(f"  - 总耗时: {result.total_time:.2f}秒")
    else:
        print(f"\n❌ 反思失败: {result.error_message}")


def demo_multi_aspect_reflection():
    """演示多维度反思"""
    print_separator("示例 2: 多维度反思 - 优化代码")
    
    llm_client = GiteeAIClient()
    agent = ReflectionAgent(
        llm_client=llm_client,
        max_iterations=3,
        score_threshold=0.9,  # 更高的质量要求
        verbose=True
    )
    
    # 提供初始代码
    initial_code = """
def find_max(numbers):
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

result = find_max([3, 1, 4, 1, 5, 9, 2, 6])
print(result)
"""
    
    result = agent.reflect_and_improve(
        task="优化这个查找最大值的Python函数",
        initial_content=initial_code,
        strategy=ReflectionStrategy.MULTI_ASPECT,
        criteria=CodeReflection.get_criteria()
    )
    
    if result.success:
        print("\n✨ 优化后的代码：")
        print("-" * 60)
        print(result.final_content)
        print("-" * 60)
        print(f"\n💡 改进总结：")
        print(result.improvement_summary)
    else:
        print(f"\n❌ 反思失败: {result.error_message}")


def demo_debate_reflection():
    """演示辩论式反思"""
    print_separator("示例 3: 辩论式反思 - 分析技术方案")
    
    llm_client = GiteeAIClient()
    agent = ReflectionAgent(
        llm_client=llm_client,
        max_iterations=2,
        score_threshold=0.8,
        verbose=True
    )
    
    task = """分析微服务架构相比单体架构的优缺点，并给出选择建议。"""
    
    result = agent.reflect_and_improve(
        task=task,
        strategy=ReflectionStrategy.DEBATE,  # 使用辩论式策略
        criteria=AnalysisReflection.get_criteria()
    )
    
    if result.success:
        print("\n✨ 最终分析结果：")
        print("-" * 60)
        print(result.final_content)
        print("-" * 60)
        
        print("\n📜 反思历史：")
        for i, reflection in enumerate(result.reflection_history, 1):
            print(f"\n第 {i} 轮反思:")
            print(f"  评分: {reflection.score:.2f}")
            print(f"  批评: {reflection.critique[:100]}...")
            print(f"  改进建议数: {len(reflection.improvements)}")
    else:
        print(f"\n❌ 反思失败: {result.error_message}")


def demo_expert_reflection():
    """演示专家反思"""
    print_separator("示例 4: 专家反思 - 专业领域评估")
    
    llm_client = GiteeAIClient()
    agent = ReflectionAgent(
        llm_client=llm_client,
        max_iterations=3,
        score_threshold=0.85,
        verbose=True
    )
    
    task = """设计一个高并发的分布式缓存系统架构方案。"""
    
    context = {
        'expert_role': '资深系统架构师',
        'expert_expertise': '15年大规模分布式系统设计经验，擅长高并发架构'
    }
    
    result = agent.reflect_and_improve(
        task=task,
        strategy=ReflectionStrategy.EXPERT,
        context=context
    )
    
    if result.success:
        print("\n✨ 专家优化后的方案：")
        print("-" * 60)
        print(result.final_content)
        print("-" * 60)
        print(f"\n质量提升: {result.final_score - result.reflection_history[0].score:+.2f}")
    else:
        print(f"\n❌ 反思失败: {result.error_message}")


def demo_translation_reflection():
    """演示翻译反思"""
    print_separator("示例 5: 翻译优化 - 改进翻译质量")
    
    llm_client = GiteeAIClient()
    agent = ReflectionAgent(
        llm_client=llm_client,
        max_iterations=3,
        score_threshold=0.9,
        verbose=True
    )
    
    # 一段需要翻译的英文
    task = """将以下英文翻译成中文：
    
"Artificial Intelligence is not just about automation, it's about augmenting human capabilities 
and enabling us to solve problems that were previously intractable. The future lies in the 
seamless collaboration between humans and AI systems."
"""
    
    result = agent.reflect_and_improve(
        task=task,
        strategy=ReflectionStrategy.MULTI_ASPECT,
        criteria=TranslationReflection.get_criteria()
    )
    
    if result.success:
        print("\n✨ 优化后的译文：")
        print("-" * 60)
        print(result.final_content)
        print("-" * 60)
    else:
        print(f"\n❌ 反思失败: {result.error_message}")


def demo_iterative_improvement():
    """演示迭代改进过程"""
    print_separator("示例 6: 迭代改进 - 观察质量提升过程")
    
    llm_client = GiteeAIClient()
    agent = ReflectionAgent(
        llm_client=llm_client,
        max_iterations=5,  # 更多迭代次数
        score_threshold=0.95,  # 很高的质量要求
        verbose=False  # 关闭详细输出，我们自己处理
    )
    
    task = """写一篇关于"量子计算的未来"的科普文章，300字左右。"""
    
    result = agent.reflect_and_improve(
        task=task,
        strategy=ReflectionStrategy.MULTI_ASPECT,
        criteria=ContentReflection.get_criteria()
    )
    
    if result.success:
        print("📈 质量改进轨迹：")
        print()
        for reflection in result.reflection_history:
            bar_length = int(reflection.score * 50)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"第{reflection.iteration}轮: [{bar}] {reflection.score:.2f}")
        
        print(f"\n总提升: {result.final_score - result.reflection_history[0].score:+.3f}")
        print(f"达到阈值: {'是' if result.final_score >= 0.95 else '否'}")
        
        print("\n✨ 最终文章：")
        print("-" * 60)
        print(result.final_content)
        print("-" * 60)
    else:
        print(f"\n❌ 反思失败: {result.error_message}")


def interactive_demo():
    """交互式演示"""
    print_separator("交互式 Reflection Agent 演示")
    
    print("欢迎使用 Reflection Agent！")
    print("\n请选择一个场景：")
    print("1. 内容创作优化")
    print("2. 代码质量提升")
    print("3. 分析报告改进")
    print("4. 翻译质量优化")
    print("5. 自定义任务")
    print("0. 退出")
    
    choice = input("\n请输入选项 (0-5): ").strip()
    
    if choice == "0":
        print("\n再见！")
        return
    
    llm_client = GiteeAIClient()
    agent = ReflectionAgent(
        llm_client=llm_client,
        max_iterations=3,
        score_threshold=0.85,
        verbose=True
    )
    
    criteria = None
    strategy = ReflectionStrategy.MULTI_ASPECT
    
    if choice == "1":
        criteria = ContentReflection.get_criteria()
        task = input("\n请输入内容创作任务: ").strip()
    elif choice == "2":
        criteria = CodeReflection.get_criteria()
        task = input("\n请输入代码或代码任务: ").strip()
    elif choice == "3":
        criteria = AnalysisReflection.get_criteria()
        task = input("\n请输入分析任务: ").strip()
    elif choice == "4":
        criteria = TranslationReflection.get_criteria()
        task = input("\n请输入翻译任务: ").strip()
    elif choice == "5":
        task = input("\n请输入任务描述: ").strip()
        print("\n选择反思策略：")
        print("1. 简单反思")
        print("2. 多维度反思（推荐）")
        print("3. 辩论式反思")
        print("4. 专家反思")
        strategy_choice = input("请选择 (1-4): ").strip()
        
        strategy_map = {
            "1": ReflectionStrategy.SIMPLE,
            "2": ReflectionStrategy.MULTI_ASPECT,
            "3": ReflectionStrategy.DEBATE,
            "4": ReflectionStrategy.EXPERT
        }
        strategy = strategy_map.get(strategy_choice, ReflectionStrategy.MULTI_ASPECT)
        
        if strategy == ReflectionStrategy.EXPERT:
            expert_role = input("请输入专家角色 (例如: 资深架构师): ").strip()
            expert_expertise = input("请输入专业领域 (例如: 10年分布式系统经验): ").strip()
            context = {
                'expert_role': expert_role or '领域专家',
                'expert_expertise': expert_expertise or '相关领域专业知识'
            }
        else:
            context = {}
    else:
        print("无效的选项！")
        return
    
    if not task:
        print("任务不能为空！")
        return
    
    print("\n开始反思和改进...")
    
    result = agent.reflect_and_improve(
        task=task,
        strategy=strategy,
        criteria=criteria,
        context=context if choice == "5" and strategy == ReflectionStrategy.EXPERT else {}
    )
    
    if result.success:
        print("\n" + "=" * 60)
        print("✨ 反思完成！")
        print("=" * 60)
        print(f"\n📊 统计信息：")
        print(f"  - 迭代次数: {result.total_iterations}")
        print(f"  - 最终评分: {result.final_score:.2f}")
        print(f"  - 质量提升: {result.final_score - result.reflection_history[0].score:+.2f}")
        print(f"  - 总耗时: {result.total_time:.2f}秒")
        
        print(f"\n✨ 最终结果：")
        print("-" * 60)
        print(result.final_content)
        print("-" * 60)
        
        print(f"\n💡 改进总结：")
        print(result.improvement_summary)
    else:
        print(f"\n❌ 反思失败: {result.error_message}")


def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           Reflection Agent 演示程序                          ║
║                                                               ║
║  通过自我批判和迭代改进提升输出质量                          ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("\n请选择演示模式：")
    print("1. 运行所有预定义示例")
    print("2. 简单反思示例")
    print("3. 多维度反思示例")
    print("4. 辩论式反思示例")
    print("5. 专家反思示例")
    print("6. 翻译优化示例")
    print("7. 迭代改进过程示例")
    print("8. 交互式演示")
    print("0. 退出")
    
    choice = input("\n请输入选项 (0-8): ").strip()
    
    if choice == "0":
        print("\n再见！")
        return
    elif choice == "1":
        # 运行所有示例
        demo_simple_reflection()
        demo_multi_aspect_reflection()
        demo_debate_reflection()
        demo_expert_reflection()
        demo_translation_reflection()
        demo_iterative_improvement()
    elif choice == "2":
        demo_simple_reflection()
    elif choice == "3":
        demo_multi_aspect_reflection()
    elif choice == "4":
        demo_debate_reflection()
    elif choice == "5":
        demo_expert_reflection()
    elif choice == "6":
        demo_translation_reflection()
    elif choice == "7":
        demo_iterative_improvement()
    elif choice == "8":
        interactive_demo()
    else:
        print("无效的选项！")
        return
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("=" * 60)
    print("\n💡 提示：")
    print("  - Reflection 通过多轮反思和改进显著提升输出质量")
    print("  - 不同策略适用于不同场景")
    print("  - 可以通过调整迭代次数和质量阈值控制优化程度")
    print("  - 查看 🎯 Reflection Agent 功能完成！.md 了解更多信息")


if __name__ == "__main__":
    main()

