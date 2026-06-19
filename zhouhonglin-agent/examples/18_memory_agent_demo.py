"""
Memory Management Agent 演示

这个示例展示了如何使用 Memory Management Agent 进行智能记忆管理。

运行方式:
    python examples/18_memory_agent_demo.py
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.zhouhonglin_agent.gitee_ai_client import GiteeAIClient
from src.zhouhonglin_agent.agents.memory_agent import (
    MemoryAgent,
    MemoryType,
    MemoryImportance,
    MemoryStrategy
)


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_basic_memory_operations():
    """演示基本的记忆操作"""
    print_section("1. 基本记忆操作")
    
    # 创建Memory Agent
    llm_client = GiteeAIClient()
    agent = MemoryAgent(
        llm_client=llm_client,
        max_memories=100,
        strategy=MemoryStrategy.HYBRID,
        storage_path="data/memories/demo_memory.json"
    )
    
    print("✓ Memory Agent 已创建\n")
    
    # 存储不同类型的记忆
    print("📝 存储记忆...\n")
    
    # 语义记忆：事实性知识
    agent.store_memory(
        content="Python是一种高级编程语言，以简洁和可读性著称",
        memory_type=MemoryType.SEMANTIC,
        importance=MemoryImportance.HIGH,
        tags=["编程", "Python", "知识"]
    )
    print("✓ 已存储语义记忆")
    
    # 情景记忆：具体事件
    agent.store_memory(
        content="用户在2025年10月15日询问了Python的特性",
        memory_type=MemoryType.EPISODIC,
        importance=MemoryImportance.MEDIUM,
        tags=["对话历史", "Python"]
    )
    print("✓ 已存储情景记忆")
    
    # 长期记忆：用户偏好
    agent.store_memory(
        content="用户喜欢使用面向对象编程方式",
        memory_type=MemoryType.LONG_TERM,
        importance=MemoryImportance.HIGH,
        tags=["用户偏好", "编程风格"]
    )
    print("✓ 已存储长期记忆")
    
    # 程序性记忆：操作步骤
    agent.store_memory(
        content="创建Python虚拟环境的步骤：1. python -m venv env 2. source env/bin/activate",
        memory_type=MemoryType.PROCEDURAL,
        importance=MemoryImportance.MEDIUM,
        tags=["Python", "环境配置", "步骤"]
    )
    print("✓ 已存储程序性记忆\n")
    
    # 获取统计信息
    stats = agent.get_statistics()
    print(f"📊 当前统计:")
    print(f"  - 总记忆数: {stats.total_memories}")
    print(f"  - 按类型分布: {stats.by_type}")
    print(f"  - 按重要性分布: {stats.by_importance}")
    print(f"  - 存储大小: {stats.storage_size_kb} KB")


def demo_memory_retrieval():
    """演示记忆检索"""
    print_section("2. 记忆检索")
    
    llm_client = GiteeAIClient()
    agent = MemoryAgent(
        llm_client=llm_client,
        storage_path="data/memories/demo_memory.json"
    )
    
    # 检索相关记忆
    print("🔍 检索关于Python的记忆...\n")
    results = agent.retrieve_memories(
        query="告诉我关于Python的信息",
        top_k=5
    )
    
    for i, result in enumerate(results, 1):
        print(f"{i}. [{result.memory.memory_type.value}] {result.memory.content}")
        print(f"   相关性: {result.relevance_score:.2f}")
        print(f"   原因: {result.reason}")
        print(f"   标签: {', '.join(result.memory.tags)}\n")
    
    # 按类型检索
    print("🔍 检索所有语义记忆...\n")
    semantic_memories = agent.get_memories_by_type(MemoryType.SEMANTIC)
    for memory in semantic_memories:
        print(f"  - {memory.content}")
    
    # 按标签检索
    print("\n🔍 检索标签为'Python'的记忆...\n")
    python_memories = agent.get_memories_by_tag("Python")
    for memory in python_memories:
        print(f"  - [{memory.memory_type.value}] {memory.content}")


def demo_memory_chat():
    """演示基于记忆的对话"""
    print_section("3. 基于记忆的对话")
    
    llm_client = GiteeAIClient()
    agent = MemoryAgent(
        llm_client=llm_client,
        storage_path="data/memories/demo_memory.json"
    )
    
    # 存储一些用户偏好
    print("📝 存储用户偏好...\n")
    agent.store_memory(
        content="用户喜欢简洁的代码风格，偏好函数式编程",
        memory_type=MemoryType.LONG_TERM,
        importance=MemoryImportance.CRITICAL,
        tags=["用户偏好", "代码风格"]
    )
    
    agent.store_memory(
        content="用户正在学习Python数据分析，目前在学习Pandas",
        memory_type=MemoryType.SEMANTIC,
        importance=MemoryImportance.HIGH,
        tags=["学习进度", "Python", "数据分析"]
    )
    
    # 基于记忆的对话
    print("💬 开始对话...\n")
    
    questions = [
        "你知道我喜欢什么样的编程风格吗？",
        "我现在在学习什么？",
        "给我推荐一些Python学习资源"
    ]
    
    for question in questions:
        print(f"👤 用户: {question}")
        response = agent.chat_with_memory(question)
        print(f"🤖 助手: {response}\n")
        print("-" * 60 + "\n")


def demo_working_memory():
    """演示工作记忆管理"""
    print_section("4. 工作记忆管理")
    
    llm_client = GiteeAIClient()
    agent = MemoryAgent(
        llm_client=llm_client,
        storage_path="data/memories/demo_memory.json"
    )
    
    print("🔧 管理工作记忆...\n")
    
    # 设置工作记忆
    agent.update_working_memory("current_task", "开发记忆管理Agent")
    agent.update_working_memory("progress", "70%")
    agent.update_working_memory("next_step", "添加前端界面")
    agent.update_working_memory("deadline", "2025-10-20")
    
    print("✓ 工作记忆已更新:")
    for key, value in agent.working_memory.items():
        print(f"  - {key}: {value}")
    
    # 基于工作记忆的对话
    print("\n💬 基于工作记忆的对话...\n")
    question = "我现在的任务进度怎么样？"
    print(f"👤 用户: {question}")
    response = agent.chat_with_memory(question)
    print(f"🤖 助手: {response}\n")
    
    # 清空工作记忆
    print("🗑️  清空工作记忆...")
    agent.clear_working_memory()
    print("✓ 工作记忆已清空")


def demo_memory_management_strategies():
    """演示不同的记忆管理策略"""
    print_section("5. 记忆管理策略")
    
    strategies = [
        (MemoryStrategy.FIFO, "先进先出"),
        (MemoryStrategy.LRU, "最近最少使用"),
        (MemoryStrategy.IMPORTANCE, "基于重要性"),
        (MemoryStrategy.HYBRID, "混合策略")
    ]
    
    for strategy, name in strategies:
        print(f"📋 策略: {name} ({strategy.value})")
        print(f"   描述: ", end="")
        
        if strategy == MemoryStrategy.FIFO:
            print("删除最早创建的记忆，简单高效")
        elif strategy == MemoryStrategy.LRU:
            print("删除最少访问的记忆，考虑使用频率")
        elif strategy == MemoryStrategy.IMPORTANCE:
            print("优先删除不重要的记忆，保护关键信息")
        elif strategy == MemoryStrategy.HYBRID:
            print("综合考虑时间、重要性和访问频率（推荐）")
        
        print()
    
    # 演示混合策略
    print("\n✨ 使用混合策略创建Agent...\n")
    llm_client = GiteeAIClient()
    agent = MemoryAgent(
        llm_client=llm_client,
        max_memories=10,  # 设置较小的容量以便演示清理
        strategy=MemoryStrategy.HYBRID,
        storage_path="data/memories/demo_strategy.json"
    )
    
    # 添加不同重要性的记忆
    print("📝 添加不同重要性的记忆...\n")
    for i in range(12):
        importance = MemoryImportance.CRITICAL if i % 4 == 0 else \
                     MemoryImportance.HIGH if i % 4 == 1 else \
                     MemoryImportance.MEDIUM if i % 4 == 2 else \
                     MemoryImportance.LOW
        
        agent.store_memory(
            content=f"记忆 {i+1}",
            memory_type=MemoryType.SEMANTIC,
            importance=importance,
            tags=[f"test_{i}"]
        )
        print(f"  ✓ 记忆 {i+1} (重要性: {importance.name})")
    
    print(f"\n📊 最终记忆数: {len(agent.memories)}")
    print("   (由于容量限制，低重要性的记忆被自动清理)")


def demo_memory_export_import():
    """演示记忆导出和导入"""
    print_section("6. 记忆导出和导入")
    
    llm_client = GiteeAIClient()
    agent1 = MemoryAgent(
        llm_client=llm_client,
        storage_path="data/memories/demo_export.json"
    )
    
    # 添加一些记忆
    print("📝 创建测试记忆...\n")
    for i in range(5):
        agent1.store_memory(
            content=f"测试记忆 {i+1}",
            memory_type=MemoryType.SEMANTIC,
            importance=MemoryImportance.MEDIUM,
            tags=["导出测试"]
        )
    
    print(f"✓ 已创建 {len(agent1.memories)} 条记忆\n")
    
    # 导出记忆
    export_path = "data/memories/exported_memories.json"
    print(f"📤 导出记忆到: {export_path}")
    agent1.export_memories(export_path)
    print("✓ 导出完成\n")
    
    # 创建新的Agent并导入
    agent2 = MemoryAgent(
        llm_client=llm_client,
        storage_path="data/memories/demo_import.json"
    )
    
    print(f"📥 导入记忆从: {export_path}")
    agent2.import_memories(export_path)
    print("✓ 导入完成\n")
    
    print(f"📊 导入后的记忆数: {len(agent2.memories)}")


def demo_memory_statistics():
    """演示记忆统计和分析"""
    print_section("7. 记忆统计和分析")
    
    llm_client = GiteeAIClient()
    agent = MemoryAgent(
        llm_client=llm_client,
        storage_path="data/memories/demo_memory.json"
    )
    
    stats = agent.get_statistics()
    
    print("📊 记忆系统统计:\n")
    print(f"📝 总记忆数: {stats.total_memories}")
    print(f"\n📦 按类型分布:")
    for mem_type, count in stats.by_type.items():
        print(f"  - {mem_type}: {count}")
    
    print(f"\n⭐ 按重要性分布:")
    for importance, count in stats.by_importance.items():
        print(f"  - {importance}: {count}")
    
    print(f"\n⏰ 时间信息:")
    print(f"  - 最早记忆: {stats.oldest_memory}")
    print(f"  - 最新记忆: {stats.newest_memory}")
    
    if stats.most_accessed:
        print(f"\n🔥 最常访问的记忆:")
        print(f"  - 内容: {stats.most_accessed.content}")
        print(f"  - 访问次数: {stats.most_accessed.access_count}")
    
    print(f"\n💾 存储信息:")
    print(f"  - 总大小: {stats.storage_size_kb} KB")
    print(f"  - 平均每条: {stats.storage_size_bytes / max(stats.total_memories, 1):.0f} bytes")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("  🧠 Memory Management Agent 演示")
    print("="*60)
    print("\n这个演示将展示记忆管理Agent的各种功能...")
    
    demos = [
        ("基本记忆操作", demo_basic_memory_operations),
        ("记忆检索", demo_memory_retrieval),
        ("基于记忆的对话", demo_memory_chat),
        ("工作记忆管理", demo_working_memory),
        ("记忆管理策略", demo_memory_management_strategies),
        ("记忆导出和导入", demo_memory_export_import),
        ("记忆统计和分析", demo_memory_statistics),
    ]
    
    while True:
        print("\n" + "="*60)
        print("  请选择要运行的演示:")
        print("="*60)
        
        for i, (name, _) in enumerate(demos, 1):
            print(f"  [{i}] {name}")
        print(f"  [A] 运行所有演示")
        print(f"  [Q] 退出")
        
        choice = input("\n请输入选择: ").strip().upper()
        
        if choice == 'Q':
            print("\n👋 再见！")
            break
        elif choice == 'A':
            for name, demo_func in demos:
                try:
                    demo_func()
                except Exception as e:
                    print(f"\n⚠️  演示出错: {e}")
                    import traceback
                    traceback.print_exc()
            
            input("\n按回车键继续...")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            try:
                demos[int(choice) - 1][1]()
            except Exception as e:
                print(f"\n⚠️  演示出错: {e}")
                import traceback
                traceback.print_exc()
            
            input("\n按回车键继续...")
        else:
            print("\n⚠️  无效的选择，请重试")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已中断，再见！")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

