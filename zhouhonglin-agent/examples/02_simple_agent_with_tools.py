"""
示例: SimpleAgent 工具调用测试

演示如何使用 SimpleAgent 的工具调用功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.zhouhonglin_agent import SimpleAgent
from src.zhouhonglin_agent.agents.tools import get_calculator_tools
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def main():
    """主函数"""
    print("=" * 60)
    print("示例: SimpleAgent 工具调用测试")
    print("=" * 60)
    print()
    
    # 创建启用了工具调用的 Agent
    print("正在初始化 Agent（启用工具调用）...")
    agent = SimpleAgent(
        system_message="你是一个有帮助的AI助手。当用户需要进行数学计算时，请使用提供的计算器工具。",
        enable_tools=True,
        max_iterations=5
    )
    print("[OK] Agent 初始化完成")
    print()
    
    # 注册计算器工具
    print("正在注册计算器工具...")
    calculator_tools = get_calculator_tools()
    for tool in calculator_tools:
        agent.register_tool(
            name=tool["name"],
            func=tool["func"],
            description=tool["description"],
            parameters=tool["parameters"]
        )
    print(f"[OK] 已注册 {len(calculator_tools)} 个计算器工具")
    print()
    
    # 测试工具调用
    test_questions = [
        "请帮我计算 123 加 456 等于多少？",
        "计算 1000 减去 234 的结果",
        "25 乘以 8 是多少？",
        "100 除以 4 等于多少？",
        "先计算 10 加 20，然后结果再乘以 3",
    ]
    
    print("=" * 60)
    print("开始测试工具调用")
    print("=" * 60)
    print()
    
    for i, question in enumerate(test_questions, 1):
        print(f"问题 {i}: {question}")
        print("-" * 60)
        
        try:
            response = agent.chat(question)
            print(f"回答: {response}")
        except Exception as e:
            print(f"错误: {str(e)}")
        
        print()
    
    # 测试向后兼容性（不启用工具）
    print("=" * 60)
    print("测试向后兼容性（不启用工具）")
    print("=" * 60)
    print()
    
    print("正在初始化 Agent（不启用工具）...")
    agent_no_tools = SimpleAgent(
        system_message="你是一个有帮助的AI助手。"
    )
    print("[OK] Agent 初始化完成")
    print()
    
    test_question = "你好！"
    print(f"问题: {test_question}")
    print("-" * 60)
    
    try:
        response = agent_no_tools.chat(test_question)
        print(f"回答: {response}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()