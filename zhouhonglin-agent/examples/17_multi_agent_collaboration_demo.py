"""
多智能体协作演示 (Multi-Agent Collaboration Demo)

这个示例展示如何使用多智能体协作系统，让多个专业化的 Agent 组成团队协同工作。

功能演示：
1. 软件开发团队协作
2. 研究团队协作
3. 内容创作团队协作
4. 商业咨询团队协作
5. 不同的协作模式
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.zhouhonglin_agent.gitee_ai_client import GiteeAIClient
from src.zhouhonglin_agent.agents.multi_agent_collaboration import (
    MultiAgentCollaboration,
    CollaborationMode,
    AgentRole,
    AgentProfile,
    SoftwareDevelopmentTeam,
    ResearchTeam,
    ContentCreationTeam,
    BusinessConsultingTeam
)


def print_separator(title=""):
    """打印分隔线"""
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)


def print_result(result):
    """打印协作结果"""
    print(f"\n{'='*80}")
    print("📊 协作结果")
    print(f"{'='*80}")
    
    print(f"\n✅ 成功: {result.success}")
    print(f"⏱️  执行时间: {result.execution_time:.2f} 秒")
    print(f"👥 参与 Agents: {len(result.agent_contributions)}")
    print(f"💬 消息数量: {len(result.messages)}")
    
    print(f"\n{'-'*80}")
    print("🎯 最终输出")
    print(f"{'-'*80}")
    print(result.final_output)
    
    print(f"\n{'-'*80}")
    print("🤖 Agent 贡献")
    print(f"{'-'*80}")
    for agent_name, contribution in result.agent_contributions.items():
        print(f"\n【{agent_name}】({contribution['role']})")
        print(contribution['response'][:200] + "..." if len(contribution['response']) > 200 else contribution['response'])
    
    if result.error_message:
        print(f"\n❌ 错误: {result.error_message}")


def demo_software_development():
    """演示：软件开发团队协作"""
    print_separator("演示1: 软件开发团队协作")
    
    print("""
场景：开发一个在线代码编辑器
团队：产品经理、系统架构师、后端工程师、前端工程师、QA 工程师
模式：层级协作（有明确的管理层级）
    """)
    
    # 初始化
    llm_client = GiteeAIClient()
    collaboration = MultiAgentCollaboration(
        llm_client=llm_client,
        mode=CollaborationMode.HIERARCHICAL,
        verbose=True
    )
    
    # 注册软件开发团队
    agents = SoftwareDevelopmentTeam.get_agents()
    collaboration.register_agents(agents)
    
    print(f"\n✓ 已注册 {len(agents)} 个 Agents")
    for agent in agents:
        print(f"  - {agent.name} ({agent.role.value}): {agent.description}")
    
    # 执行协作
    task = "设计并实现一个支持多人协作的在线代码编辑器，需要考虑实时同步、语法高亮、代码补全等功能"
    
    print(f"\n🎯 任务: {task}")
    print("\n开始协作...")
    
    result = collaboration.collaborate(task)
    print_result(result)
    
    return result


def demo_research_team():
    """演示：研究团队协作"""
    print_separator("演示2: 研究团队协作")
    
    print("""
场景：研究深度学习在自然语言处理中的应用
团队：研究负责人、理论研究者、数据科学家、实验研究者、同行评审专家
模式：层级协作
    """)
    
    # 初始化
    llm_client = GiteeAIClient()
    collaboration = MultiAgentCollaboration(
        llm_client=llm_client,
        mode=CollaborationMode.HIERARCHICAL,
        verbose=True
    )
    
    # 注册研究团队
    agents = ResearchTeam.get_agents()
    collaboration.register_agents(agents)
    
    print(f"\n✓ 已注册 {len(agents)} 个 Agents")
    
    # 执行协作
    task = "研究如何使用 Transformer 模型改进机器翻译的质量，设计实验方案并分析预期结果"
    
    print(f"\n🎯 任务: {task}")
    print("\n开始协作...")
    
    result = collaboration.collaborate(task)
    print_result(result)
    
    return result


def demo_content_creation():
    """演示：内容创作团队协作"""
    print_separator("演示3: 内容创作团队协作")
    
    print("""
场景：撰写一篇关于人工智能未来发展的文章
团队：内容策略师、撰写者、编辑、SEO 专家
模式：并行协作（同时工作然后整合）
    """)
    
    # 初始化
    llm_client = GiteeAIClient()
    collaboration = MultiAgentCollaboration(
        llm_client=llm_client,
        mode=CollaborationMode.PARALLEL,  # 使用并行模式
        verbose=True
    )
    
    # 注册内容创作团队
    agents = ContentCreationTeam.get_agents()
    collaboration.register_agents(agents)
    
    print(f"\n✓ 已注册 {len(agents)} 个 Agents")
    
    # 执行协作
    task = "撰写一篇面向技术人员的文章：《人工智能的下一个十年：机遇与挑战》"
    
    print(f"\n🎯 任务: {task}")
    print("\n开始协作...")
    
    result = collaboration.collaborate(task)
    print_result(result)
    
    return result


def demo_business_consulting():
    """演示：商业咨询团队协作"""
    print_separator("演示4: 商业咨询团队协作")
    
    print("""
场景：企业数字化转型战略咨询
团队：首席顾问、商业分析师、财务顾问、实施专家、质量保证专家
模式：层级协作
    """)
    
    # 初始化
    llm_client = GiteeAIClient()
    collaboration = MultiAgentCollaboration(
        llm_client=llm_client,
        mode=CollaborationMode.HIERARCHICAL,
        verbose=True
    )
    
    # 注册商业咨询团队
    agents = BusinessConsultingTeam.get_agents()
    collaboration.register_agents(agents)
    
    print(f"\n✓ 已注册 {len(agents)} 个 Agents")
    
    # 执行协作
    task = "为一家传统制造企业制定数字化转型战略，包括技术选型、实施路线图和成本效益分析"
    
    print(f"\n🎯 任务: {task}")
    print("\n开始协作...")
    
    result = collaboration.collaborate(task)
    print_result(result)
    
    return result


def demo_different_modes():
    """演示：不同的协作模式"""
    print_separator("演示5: 不同协作模式对比")
    
    print("""
任务：设计一个智能问答系统
使用不同的协作模式看看效果有何不同
    """)
    
    task = "设计一个基于 RAG 的智能问答系统，包括知识库构建、检索优化和答案生成"
    
    llm_client = GiteeAIClient()
    agents = SoftwareDevelopmentTeam.get_agents()
    
    modes = [
        (CollaborationMode.SEQUENTIAL, "顺序协作"),
        (CollaborationMode.PARALLEL, "并行协作"),
        (CollaborationMode.HIERARCHICAL, "层级协作")
    ]
    
    results = []
    
    for mode, mode_name in modes:
        print(f"\n{'-'*80}")
        print(f"🔄 模式: {mode_name}")
        print(f"{'-'*80}")
        
        collaboration = MultiAgentCollaboration(
            llm_client=llm_client,
            mode=mode,
            verbose=False  # 关闭详细输出
        )
        
        collaboration.register_agents(agents)
        result = collaboration.collaborate(task)
        results.append((mode_name, result))
        
        print(f"\n✓ 完成 ({result.execution_time:.2f}s)")
        print(f"  - Agents 数: {len(result.agent_contributions)}")
        print(f"  - 消息数: {len(result.messages)}")
    
    # 对比结果
    print(f"\n{'-'*80}")
    print("📊 模式对比")
    print(f"{'-'*80}")
    print(f"{'模式':<15} {'时间(s)':<10} {'Agents':<10} {'消息数':<10}")
    print(f"{'-'*80}")
    for mode_name, result in results:
        print(f"{mode_name:<15} {result.execution_time:<10.2f} {len(result.agent_contributions):<10} {len(result.messages):<10}")
    
    return results


def demo_custom_team():
    """演示：自定义团队"""
    print_separator("演示6: 自定义团队协作")
    
    print("""
场景：创建一个专门的教育产品开发团队
自定义 Agents 组合
    """)
    
    llm_client = GiteeAIClient()
    collaboration = MultiAgentCollaboration(
        llm_client=llm_client,
        mode=CollaborationMode.HIERARCHICAL,
        verbose=True
    )
    
    # 自定义教育产品团队
    custom_agents = [
        AgentProfile(
            name="教育专家",
            role=AgentRole.COORDINATOR,
            description="教育领域专家，负责教学设计",
            expertise=["教学设计", "课程开发", "学习理论"],
            system_prompt="你是一位经验丰富的教育专家，擅长设计有效的学习体验。",
            priority=10
        ),
        AgentProfile(
            name="产品设计师",
            role=AgentRole.SPECIALIST,
            description="负责产品交互和用户体验设计",
            expertise=["用户体验", "交互设计", "产品设计"],
            system_prompt="你是一位产品设计师，专注于创建直观易用的学习产品。",
            priority=9
        ),
        AgentProfile(
            name="技术开发者",
            role=AgentRole.EXECUTOR,
            description="负责技术实现",
            expertise=["前端开发", "后端开发", "移动开发"],
            system_prompt="你是一位全栈开发者，能够实现各种技术方案。",
            priority=8
        ),
        AgentProfile(
            name="教育评估师",
            role=AgentRole.REVIEWER,
            description="评估教学效果和产品质量",
            expertise=["教学评估", "数据分析", "效果测量"],
            system_prompt="你是教育评估专家，关注学习效果和产品质量。",
            priority=7
        )
    ]
    
    collaboration.register_agents(custom_agents)
    
    print(f"\n✓ 已注册自定义团队 {len(custom_agents)} 个 Agents")
    for agent in custom_agents:
        print(f"  - {agent.name} ({agent.role.value})")
    
    # 执行协作
    task = "设计一个在线编程学习平台，帮助初学者学习 Python，包括互动式课程、在线编辑器和即时反馈"
    
    print(f"\n🎯 任务: {task}")
    print("\n开始协作...")
    
    result = collaboration.collaborate(task)
    print_result(result)
    
    return result


def interactive_mode():
    """交互模式"""
    print_separator("交互模式：多智能体协作")
    
    print("""
在交互模式中，您可以：
1. 选择团队类型
2. 选择协作模式
3. 输入任务描述
4. 查看协作结果
    """)
    
    # 选择团队
    print("\n可用的团队：")
    teams = {
        "1": ("软件开发团队", SoftwareDevelopmentTeam),
        "2": ("研究团队", ResearchTeam),
        "3": ("内容创作团队", ContentCreationTeam),
        "4": ("商业咨询团队", BusinessConsultingTeam)
    }
    
    for key, (name, _) in teams.items():
        print(f"  {key}. {name}")
    
    team_choice = input("\n请选择团队 (1-4): ").strip()
    if team_choice not in teams:
        print("❌ 无效选择")
        return
    
    team_name, team_class = teams[team_choice]
    
    # 选择模式
    print("\n可用的协作模式：")
    modes = {
        "1": (CollaborationMode.SEQUENTIAL, "顺序协作"),
        "2": (CollaborationMode.PARALLEL, "并行协作"),
        "3": (CollaborationMode.HIERARCHICAL, "层级协作（推荐）"),
        "4": (CollaborationMode.PEER_TO_PEER, "对等协作"),
        "5": (CollaborationMode.HYBRID, "混合模式")
    }
    
    for key, (_, name) in modes.items():
        print(f"  {key}. {name}")
    
    mode_choice = input("\n请选择协作模式 (1-5，默认3): ").strip() or "3"
    if mode_choice not in modes:
        print("❌ 无效选择")
        return
    
    mode, mode_name = modes[mode_choice]
    
    # 输入任务
    print("\n请输入任务描述（输入多行，空行结束）：")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    
    task = "\n".join(lines)
    if not task:
        print("❌ 任务描述不能为空")
        return
    
    # 确认并执行
    print(f"\n{'='*80}")
    print("📋 协作配置")
    print(f"{'='*80}")
    print(f"团队: {team_name}")
    print(f"模式: {mode_name}")
    print(f"任务: {task[:100]}...")
    
    confirm = input("\n确认开始协作？(y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ 已取消")
        return
    
    # 初始化并执行
    llm_client = GiteeAIClient()
    collaboration = MultiAgentCollaboration(
        llm_client=llm_client,
        mode=mode,
        verbose=True
    )
    
    agents = team_class.get_agents()
    collaboration.register_agents(agents)
    
    print(f"\n✓ 已注册 {len(agents)} 个 Agents")
    print("\n开始协作...\n")
    
    result = collaboration.collaborate(task)
    print_result(result)
    
    # 保存结果
    save = input("\n是否保存结果到文件？(y/n): ").strip().lower()
    if save == 'y':
        import json
        from datetime import datetime
        
        filename = f"collaboration_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "team": team_name,
                "mode": mode_name,
                "task": task,
                "success": result.success,
                "execution_time": result.execution_time,
                "final_output": result.final_output,
                "agent_contributions": result.agent_contributions,
                "messages": [
                    {
                        "sender": msg.sender,
                        "receiver": msg.receiver,
                        "content": msg.content,
                        "type": msg.message_type,
                        "timestamp": msg.timestamp
                    }
                    for msg in result.messages
                ]
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 结果已保存到: {filename}")


def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              🤝 多智能体协作演示 (Multi-Agent Collaboration)                  ║
║                                                                              ║
║  让多个专业化的 AI Agent 组成团队，通过协作共同完成复杂任务                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("\n请选择演示：")
    print("  1. 软件开发团队协作")
    print("  2. 研究团队协作")
    print("  3. 内容创作团队协作")
    print("  4. 商业咨询团队协作")
    print("  5. 不同协作模式对比")
    print("  6. 自定义团队协作")
    print("  7. 交互模式")
    print("  0. 运行所有演示")
    
    choice = input("\n请选择 (0-7): ").strip()
    
    demos = {
        "1": demo_software_development,
        "2": demo_research_team,
        "3": demo_content_creation,
        "4": demo_business_consulting,
        "5": demo_different_modes,
        "6": demo_custom_team,
        "7": interactive_mode
    }
    
    if choice == "0":
        # 运行所有演示
        for i in range(1, 7):
            try:
                demos[str(i)]()
                input("\n按 Enter 继续下一个演示...")
            except KeyboardInterrupt:
                print("\n\n⚠️ 用户中断")
                break
            except Exception as e:
                print(f"\n❌ 演示失败: {e}")
                import traceback
                traceback.print_exc()
    elif choice in demos:
        try:
            demos[choice]()
        except KeyboardInterrupt:
            print("\n\n⚠️ 用户中断")
        except Exception as e:
            print(f"\n❌ 演示失败: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ 无效选择")
    
    print("\n" + "="*80)
    print("演示结束！")
    print("="*80)


if __name__ == "__main__":
    main()

