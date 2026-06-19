"""
单元测试: 计算器工具

测试计算器工具的基本功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.zhouhonglin_agent.agents.tools.calculator_tool import (
    add,
    subtract,
    multiply,
    divide,
    calculator_add,
    calculator_subtract,
    calculator_multiply,
    calculator_divide,
    get_calculator_tools
)


def test_basic_operations():
    """测试基本运算"""
    print("测试基本运算...")
    
    # 测试加法
    assert add(1, 2) == 3
    assert add(1.5, 2.5) == 4.0
    print("  [OK] 加法测试通过")
    
    # 测试减法
    assert subtract(5, 3) == 2
    assert subtract(5.5, 2.5) == 3.0
    print("  [OK] 减法测试通过")
    
    # 测试乘法
    assert multiply(3, 4) == 12
    assert multiply(2.5, 4) == 10.0
    print("  [OK] 乘法测试通过")
    
    # 测试除法
    assert divide(10, 2) == 5.0
    assert divide(10.0, 4.0) == 2.5
    print("  [OK] 除法测试通过")
    
    # 测试除零错误
    try:
        divide(10, 0)
        assert False, "应该抛出 ZeroDivisionError"
    except ZeroDivisionError:
        print("  [OK] 除零错误测试通过")


def test_calculator_wrappers():
    """测试计算器包装函数"""
    print("\n测试计算器包装函数...")
    
    # 测试加法包装
    result = calculator_add(1, 2)
    assert result["operation"] == "addition"
    assert result["operands"] == [1, 2]
    assert result["result"] == 3
    print("  [OK] 加法包装测试通过")
    
    # 测试减法包装
    result = calculator_subtract(5, 3)
    assert result["operation"] == "subtraction"
    assert result["operands"] == [5, 3]
    assert result["result"] == 2
    print("  [OK] 减法包装测试通过")
    
    # 测试乘法包装
    result = calculator_multiply(3, 4)
    assert result["operation"] == "multiplication"
    assert result["operands"] == [3, 4]
    assert result["result"] == 12
    print("  [OK] 乘法包装测试通过")
    
    # 测试除法包装
    result = calculator_divide(10, 2)
    assert result["operation"] == "division"
    assert result["operands"] == [10, 2]
    assert result["result"] == 5.0
    print("  [OK] 除法包装测试通过")


def test_tool_definitions():
    """测试工具定义"""
    print("\n测试工具定义...")
    
    tools = get_calculator_tools()
    assert len(tools) == 4, f"应该有 4 个工具，实际有 {len(tools)} 个"
    print(f"  [OK] 工具数量正确: {len(tools)}")
    
    # 检查每个工具的结构
    for tool in tools:
        assert "name" in tool
        assert "func" in tool
        assert "description" in tool
        assert "parameters" in tool
        assert tool["parameters"]["type"] == "object"
        assert "properties" in tool["parameters"]
        assert "required" in tool["parameters"]
        print(f"  [OK] 工具 '{tool['name']}' 结构正确")
    
    # 检查具体工具
    tool_names = [tool["name"] for tool in tools]
    assert "calculator_add" in tool_names
    assert "calculator_subtract" in tool_names
    assert "calculator_multiply" in tool_names
    assert "calculator_divide" in tool_names
    print("  [OK] 所有必需的工具都存在")


def test_tool_execution():
    """测试工具执行"""
    print("\n测试工具执行...")
    
    tools = get_calculator_tools()
    
    # 测试加法工具执行
    add_tool = next(t for t in tools if t["name"] == "calculator_add")
    result = add_tool["func"](a=10, b=20)
    assert result["result"] == 30
    print("  [OK] 加法工具执行测试通过")
    
    # 测试减法工具执行
    subtract_tool = next(t for t in tools if t["name"] == "calculator_subtract")
    result = subtract_tool["func"](a=100, b=30)
    assert result["result"] == 70
    print("  [OK] 减法工具执行测试通过")
    
    # 测试乘法工具执行
    multiply_tool = next(t for t in tools if t["name"] == "calculator_multiply")
    result = multiply_tool["func"](a=7, b=8)
    assert result["result"] == 56
    print("  [OK] 乘法工具执行测试通过")
    
    # 测试除法工具执行
    divide_tool = next(t for t in tools if t["name"] == "calculator_divide")
    result = divide_tool["func"](a=100, b=4)
    assert result["result"] == 25.0
    print("  [OK] 除法工具执行测试通过")


def main():
    """主函数"""
    print("=" * 60)
    print("单元测试: 计算器工具")
    print("=" * 60)
    print()
    
    try:
        test_basic_operations()
        test_calculator_wrappers()
        test_tool_definitions()
        test_tool_execution()
        
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