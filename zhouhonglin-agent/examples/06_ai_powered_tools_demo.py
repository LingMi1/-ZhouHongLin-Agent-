"""
AI驱动工具演示

展示真正需要大模型参与的智能工具，而不是简单的硬编码逻辑
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.zhouhonglin_agent.agents.tool_agent import ToolAgent
from src.zhouhonglin_agent.tools import get_ai_powered_tools


def print_section(title: str):
    """打印章节标题"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()
    
    print_section("🤖 AI驱动的智能工具演示")
    print("这些工具真正需要大模型的理解、推理和生成能力")
    print("而不是简单的硬编码逻辑！\n")
    
    # 创建工具 Agent
    agent = ToolAgent(
        system_message="""你是一个智能AI助手，拥有多种需要AI能力的高级工具。
当工具返回 needs_ai_processing=True 时，说明工具已经为你准备好了分析指令，
请按照指令中的要求，使用你的AI能力进行深度分析和处理。"""
    )
    
    # 注册所有AI驱动的工具
    print("📦 正在注册AI驱动的工具...")
    tools = get_ai_powered_tools()
    for tool in tools:
        agent.register_tool(
            name=tool["name"],
            func=tool["func"],
            description=tool["description"],
            parameters=tool["parameters"]
        )
    print(f"✅ 已注册 {len(tools)} 个AI智能工具\n")
    
    # 展示工具列表
    print("📋 可用的AI智能工具：")
    tool_names = [
        "1. web_content_analyzer - 智能网页内容分析",
        "2. text_quality_analyzer - 文本质量分析",
        "3. creative_idea_generator - 创意想法生成",
        "4. code_review_assistant - 代码审查助手",
        "5. decision_analyzer - 决策分析",
        "6. data_insight_generator - 数据洞察生成",
        "7. content_improver - 内容优化器",
        "8. problem_solver - 问题解决器",
        "9. meeting_summarizer - 会议总结器",
        "10. learning_path_designer - 学习路径设计"
    ]
    for name in tool_names:
        print(f"   {name}")
    
    # 精选演示案例
    demo_cases = [
        {
            "title": "💡 创意生成",
            "query": "我想开一家咖啡店，帮我生成3个有创意的商业模式想法"
        },
        {
            "title": "📝 文本质量分析",
            "query": """帮我分析这段文本的质量：
"我们公司是做软件的公司，我们的产品很好用，很多人都在用，你也来用吧，
真的很好用的，不信你试试，用了就知道了。"

请指出问题并给出改进建议。"""
        },
        {
            "title": "🔍 代码审查",
            "query": """请审查这段Python代码：

def get_user(id):
    users = []
    for i in range(1000):
        users.append({'id': i, 'name': f'user{i}'})
    for u in users:
        if u['id'] == id:
            return u
    return None

result = get_user(500)
print(result)"""
        },
        {
            "title": "🤔 决策分析",
            "query": """帮我分析这个决策场景：
场景：我正在考虑职业发展方向
选项：
1. 留在大公司做技术专家
2. 跳槽到创业公司当技术负责人
3. 自己创业

请帮我分析各个选项的优劣。"""
        },
        {
            "title": "✨ 内容优化",
            "query": """请将这段内容改写为更专业的商务风格：

"嘿，咱们下周开个会呗，聊聊那个项目的事儿，看看能不能搞定，
要是搞不定就算了，反正也不是啥大事。"
"""
        }
    ]
    
    # 运行演示案例
    for i, case in enumerate(demo_cases, 1):
        print_section(f"{case['title']} (案例 {i}/{len(demo_cases)})")
        print(f"❓ 用户请求:\n{case['query']}\n")
        print("💭 AI正在调用智能工具并进行分析...\n")
        
        try:
            response = agent.run(case['query'])
            print(f"✅ AI回复:\n{response}\n")
        except Exception as e:
            print(f"❌ 错误: {str(e)}\n")
        
        # 添加分隔，避免输出太快
        input("\n按Enter继续下一个演示...")
    
    print_section("🎯 演示完成")
    print("""
这些工具展示了AI Agent的真正价值：

✅ 需要深度理解和分析
✅ 需要创造性思维
✅ 需要专业知识和经验
✅ 需要多维度推理
✅ 需要语言生成能力

而不是简单的：
❌ 日期时间处理
❌ 数学计算
❌ 字符串操作
❌ 编码解码
❌ 简单的算法逻辑

这才是AI Agent应该做的事情！🚀
""")


if __name__ == "__main__":
    main()

