"""
Prompt Chaining Agent 演示 - 体验提示链设计模式

这个演示展示了如何使用 Prompt Chaining 模式来处理复杂任务。
提供了多个实用场景供您体验。
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.zhouhonglin_agent.gitee_ai_client import GiteeAIClient
from src.zhouhonglin_agent.agents.prompt_chaining_agent import (
    PromptChainingAgent,
    DocumentGenerationChain,
    CodeReviewChain,
    ResearchPlanningChain,
    StoryCreationChain,
    ProductAnalysisChain
)


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       🔗 Prompt Chaining Agent - 提示链代理演示 🔗          ║
║                                                              ║
║   体验 Agentic Design Pattern 中的 Prompt Chaining 模式    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

提示链（Prompt Chaining）核心理念：
• 将复杂任务分解为一系列简单子任务
• 每个子任务专注于特定目标
• 前一步的输出成为下一步的输入
• 提高输出质量和可控性
"""
    print(banner)


def print_menu():
    """打印功能菜单"""
    menu = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                         场景选择
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] 📄 文档生成链
    功能：根据主题自动生成结构化技术文档
    步骤：生成大纲 → 撰写内容 → 添加示例 → 优化润色

[2] 🔍 代码审查链
    功能：系统化的代码审查和改进建议
    步骤：理解代码 → 检查问题 → 提出建议 → 生成报告

[3] 🔬 研究规划链
    功能：将研究问题转化为系统化的研究计划
    步骤：问题分析 → 文献综述 → 研究方法 → 时间规划

[4] 📖 故事创作链
    功能：创意写作工作流，生成完整故事
    步骤：构思情节 → 角色塑造 → 撰写初稿 → 润色完善

[5] 💡 产品分析链
    功能：系统化的产品需求分析和规划
    步骤：需求理解 → 功能设计 → 技术方案 → 实施计划

[0] 👋 退出程序

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(menu)


def scenario_document_generation(agent: PromptChainingAgent):
    """场景1：文档生成"""
    print("\n" + "="*60)
    print("📄 文档生成链 - Document Generation Chain")
    print("="*60)
    
    # 获取用户输入
    print("\n请输入文档主题（例如：Python 异步编程入门、Docker 容器化实践等）")
    topic = input("主题: ").strip()
    
    if not topic:
        print("❌ 主题不能为空")
        return
    
    # 创建并执行链
    agent.create_chain("doc_gen", DocumentGenerationChain.get_steps())
    result = agent.run_chain("doc_gen", topic)
    
    if result.success:
        # 保存结果
        output_file = f"document_{topic[:20].replace(' ', '_')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.final_output)
        
        print(f"\n✅ 文档生成成功！已保存到: {output_file}")
        print(f"⏱️  总耗时: {result.execution_time:.2f}秒")
        
        # 询问是否查看
        view = input("\n是否查看生成的文档? (y/n): ").strip().lower()
        if view == 'y':
            print("\n" + "="*60)
            print("生成的文档内容：")
            print("="*60)
            print(result.final_output)
    else:
        print(f"\n❌ 执行失败: {result.error_message}")


def scenario_code_review(agent: PromptChainingAgent):
    """场景2：代码审查"""
    print("\n" + "="*60)
    print("🔍 代码审查链 - Code Review Chain")
    print("="*60)
    
    print("\n请输入要审查的代码（输入 'END' 单独一行表示结束）:")
    print("提示：可以粘贴一个函数、类或代码片段")
    print("-"*60)
    
    code_lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        code_lines.append(line)
    
    code = '\n'.join(code_lines)
    
    if not code.strip():
        print("❌ 代码不能为空")
        return
    
    # 创建并执行链
    agent.create_chain("code_review", CodeReviewChain.get_steps())
    result = agent.run_chain("code_review", code)
    
    if result.success:
        # 保存结果
        output_file = "code_review_report.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.final_output)
        
        print(f"\n✅ 代码审查完成！报告已保存到: {output_file}")
        print(f"⏱️  总耗时: {result.execution_time:.2f}秒")
    else:
        print(f"\n❌ 执行失败: {result.error_message}")


def scenario_research_planning(agent: PromptChainingAgent):
    """场景3：研究规划"""
    print("\n" + "="*60)
    print("🔬 研究规划链 - Research Planning Chain")
    print("="*60)
    
    print("\n请输入研究问题（例如：如何优化深度学习模型的训练效率？）")
    question = input("问题: ").strip()
    
    if not question:
        print("❌ 问题不能为空")
        return
    
    # 创建并执行链
    agent.create_chain("research", ResearchPlanningChain.get_steps())
    result = agent.run_chain("research", question)
    
    if result.success:
        # 保存结果
        output_file = f"research_plan_{question[:20].replace(' ', '_')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.final_output)
        
        print(f"\n✅ 研究计划生成成功！已保存到: {output_file}")
        print(f"⏱️  总耗时: {result.execution_time:.2f}秒")
    else:
        print(f"\n❌ 执行失败: {result.error_message}")


def scenario_story_creation(agent: PromptChainingAgent):
    """场景4：故事创作"""
    print("\n" + "="*60)
    print("📖 故事创作链 - Story Creation Chain")
    print("="*60)
    
    print("\n请输入故事主题（例如：时间旅行者的困境、AI觉醒的一天等）")
    theme = input("主题: ").strip()
    
    if not theme:
        print("❌ 主题不能为空")
        return
    
    # 创建并执行链
    agent.create_chain("story", StoryCreationChain.get_steps())
    result = agent.run_chain("story", theme)
    
    if result.success:
        # 保存结果
        output_file = f"story_{theme[:20].replace(' ', '_')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.final_output)
        
        print(f"\n✅ 故事创作完成！已保存到: {output_file}")
        print(f"⏱️  总耗时: {result.execution_time:.2f}秒")
        
        # 询问是否查看
        view = input("\n是否查看创作的故事? (y/n): ").strip().lower()
        if view == 'y':
            print("\n" + "="*60)
            print("创作的故事：")
            print("="*60)
            print(result.final_output)
    else:
        print(f"\n❌ 执行失败: {result.error_message}")


def scenario_product_analysis(agent: PromptChainingAgent):
    """场景5：产品分析"""
    print("\n" + "="*60)
    print("💡 产品分析链 - Product Analysis Chain")
    print("="*60)
    
    print("\n请描述产品需求（例如：一个帮助开发者快速搭建API的工具）")
    requirement = input("需求: ").strip()
    
    if not requirement:
        print("❌ 需求不能为空")
        return
    
    # 创建并执行链
    agent.create_chain("product", ProductAnalysisChain.get_steps())
    result = agent.run_chain("product", requirement)
    
    if result.success:
        # 保存结果
        output_file = f"product_analysis_{requirement[:20].replace(' ', '_')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.final_output)
        
        print(f"\n✅ 产品分析完成！已保存到: {output_file}")
        print(f"⏱️  总耗时: {result.execution_time:.2f}秒")
    else:
        print(f"\n❌ 执行失败: {result.error_message}")


def main():
    """主程序"""
    print_banner()
    
    # 初始化 LLM 客户端
    print("正在初始化 AI 客户端...")
    try:
        llm_client = GiteeAIClient()
        print("✓ AI 客户端初始化成功\n")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("请确保已配置好 API Key (在 .env 文件中)")
        return
    
    # 创建提示链代理
    agent = PromptChainingAgent(llm_client, verbose=True)
    
    # 场景映射
    scenarios = {
        '1': scenario_document_generation,
        '2': scenario_code_review,
        '3': scenario_research_planning,
        '4': scenario_story_creation,
        '5': scenario_product_analysis
    }
    
    # 主循环
    while True:
        print_menu()
        choice = input("请选择场景 (0-5): ").strip()
        
        if choice == '0':
            print("\n👋 感谢使用 Prompt Chaining Agent！再见！\n")
            break
        elif choice in scenarios:
            try:
                scenarios[choice](agent)
            except KeyboardInterrupt:
                print("\n\n⚠️  操作已取消")
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")
                import traceback
                traceback.print_exc()
            
            input("\n按 Enter 键继续...")
        else:
            print("\n❌ 无效选择，请重新输入")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出")

