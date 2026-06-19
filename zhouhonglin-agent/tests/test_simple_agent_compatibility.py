"""
单元测试: SimpleAgent 向后兼容性

测试 SimpleAgent 在不启用工具时的向后兼容性
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.zhouhonglin_agent import SimpleAgent


def test_simple_agent_without_tools():
    """测试不启用工具的 SimpleAgent"""
    print("测试不启用工具的 SimpleAgent...")
    
    # 创建不启用工具的 Agent
    agent = SimpleAgent(
        system_message="你是一个测试助手。"
    )
    
    # 检查初始状态
    assert agent.enable_tools == False, "默认应该不启用工具"
    assert agent.max_iterations == 10, "默认最大迭代次数应该是 10"
    assert len(agent.tools) == 0, "默认应该没有工具"
    assert len(agent.tool_functions) == 0, "默认应该没有工具函数"
    print("  [OK] 初始状态正确")
    
    # 检查图结构
    assert agent.graph is not None, "图应该被创建"
    print("  [OK] 图结构正确")


def test_simple_agent_with_tools_enabled():
    """测试启用工具的 SimpleAgent"""
    print("\n测试启用工具的 SimpleAgent...")
    
    # 创建启用工具的 Agent
    agent = SimpleAgent(
        system_message="你是一个测试助手。",
        enable_tools=True,
        max_iterations=5
    )
    
    # 检查初始状态
    assert agent.enable_tools == True, "应该启用工具"
    assert agent.max_iterations == 5, "最大迭代次数应该是 5"
    assert len(agent.tools) == 0, "初始应该没有工具"
    assert len(agent.tool_functions) == 0, "初始应该没有工具函数"
    print("  [OK] 初始状态正确")
    
    # 检查图结构
    assert agent.graph is not None, "图应该被创建"
    print("  [OK] 图结构正确")


def test_register_tool():
    """测试工具注册"""
    print("\n测试工具注册...")
    
    # 创建启用工具的 Agent
    agent = SimpleAgent(enable_tools=True)
    
    # 定义一个测试工具
    def test_tool(x: int, y: int) -> int:
        return x + y
    
    # 注册工具
    agent.register_tool(
        name="test_tool",
        func=test_tool,
        description="测试工具",
        parameters={
            "type": "object",
            "properties": {
                "x": {"type": "integer"},
                "y": {"type": "integer"}
            },
            "required": ["x", "y"]
        }
    )
    
    # 检查工具是否注册成功
    assert len(agent.tools) == 1, "应该有 1 个工具"
    assert len(agent.tool_functions) == 1, "应该有 1 个工具函数"
    assert "test_tool" in agent.tool_functions, "工具函数应该存在"
    assert agent.tool_functions["test_tool"] == test_tool, "工具函数应该正确"
    print("  [OK] 工具注册成功")


def test_max_iterations_limit():
    """测试最大迭代次数限制"""
    print("\n测试最大迭代次数限制...")
    
    # 测试不同的最大迭代次数
    for max_iter in [1, 5, 10, 20]:
        agent = SimpleAgent(enable_tools=True, max_iterations=max_iter)
        assert agent.max_iterations == max_iter, f"最大迭代次数应该是 {max_iter}"
    
    print("  [OK] 最大迭代次数限制正确")


def test_state_structure():
    """测试状态结构"""
    print("\n测试状态结构...")
    
    from src.zhouhonglin_agent.agents.simple_agent import AgentState
    from langchain_core.messages import HumanMessage
    
    # 创建测试状态
    state = {
        "messages": [HumanMessage(content="测试")],
        "next_action": "",
        "iterations": 0
    }
    
    # 验证状态结构
    assert "messages" in state, "状态应该包含 messages"
    assert "next_action" in state, "状态应该包含 next_action"
    assert "iterations" in state, "状态应该包含 iterations"
    
    print("  [OK] 状态结构正确")


def main():
    """主函数"""
    print("=" * 60)
    print("单元测试: SimpleAgent 向后兼容性")
    print("=" * 60)
    print()
    
    try:
        test_simple_agent_without_tools()
        test_simple_agent_with_tools_enabled()
        test_register_tool()
        test_max_iterations_limit()
        test_state_structure()
        
        print()
        print("=" * 60)
        print("[OK] 所有测试通过!")
        print("=" * 60)
        
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"[ERROR] 测试失败: {str(e)}")
        print("=" * 60)
        sys.exit(1)
    except Exception as e:
        print()
        print("=" * 60)
        print(f"[ERROR] 发生错误: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()