"""
计算器工具

为 SimpleAgent 提供基础的数值计算功能
支持加、减、乘、除四则运算
"""

from typing import Union


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    加法运算
    
    Args:
        a: 第一个数
        b: 第二个数
        
    Returns:
        两个数的和
        
    Examples:
        >>> add(1, 2)
        3
        >>> add(1.5, 2.5)
        4.0
    """
    return a + b


def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    减法运算
    
    Args:
        a: 被减数
        b: 减数
        
    Returns:
        两个数的差
        
    Examples:
        >>> subtract(5, 3)
        2
        >>> subtract(5.5, 2.5)
        3.0
    """
    return a - b


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    乘法运算
    
    Args:
        a: 第一个数
        b: 第二个数
        
    Returns:
        两个数的积
        
    Examples:
        >>> multiply(3, 4)
        12
        >>> multiply(2.5, 4)
        10.0
    """
    return a * b


def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    除法运算
    
    Args:
        a: 被除数
        b: 除数
        
    Returns:
        两个数的商
        
    Raises:
        ZeroDivisionError: 当除数为 0 时抛出
        
    Examples:
        >>> divide(10, 2)
        5
        >>> divide(10.0, 4.0)
        2.5
    """
    if b == 0:
        raise ZeroDivisionError("除数不能为零")
    return a / b


# 为了更好的工具调用体验，提供带描述的包装函数
def calculator_add(a: Union[int, float], b: Union[int, float]) -> dict:
    """
    计算两个数的和
    
    Args:
        a: 第一个加数
        b: 第二个加数
        
    Returns:
        包含计算结果的字典
    """
    result = add(a, b)
    return {
        "operation": "addition",
        "operands": [a, b],
        "result": result
    }


def calculator_subtract(a: Union[int, float], b: Union[int, float]) -> dict:
    """
    计算两个数的差
    
    Args:
        a: 被减数
        b: 减数
        
    Returns:
        包含计算结果的字典
    """
    result = subtract(a, b)
    return {
        "operation": "subtraction",
        "operands": [a, b],
        "result": result
    }


def calculator_multiply(a: Union[int, float], b: Union[int, float]) -> dict:
    """
    计算两个数的积
    
    Args:
        a: 第一个乘数
        b: 第二个乘数
        
    Returns:
        包含计算结果的字典
    """
    result = multiply(a, b)
    return {
        "operation": "multiplication",
        "operands": [a, b],
        "result": result
    }


def calculator_divide(a: Union[int, float], b: Union[int, float]) -> dict:
    """
    计算两个数的商
    
    Args:
        a: 被除数
        b: 除数
        
    Returns:
        包含计算结果的字典
        
    Raises:
        ZeroDivisionError: 当除数为 0 时抛出
    """
    result = divide(a, b)
    return {
        "operation": "division",
        "operands": [a, b],
        "result": result
    }


def get_calculator_tools() -> list:
    """
    获取计算器工具列表
    
    返回符合 LangGraph 工具定义格式的工具列表
    
    Returns:
        工具定义列表
    """
    return [
        {
            "name": "calculator_add",
            "func": calculator_add,
            "description": "计算两个数的和。当用户需要做加法运算时使用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "第一个加数"
                    },
                    "b": {
                        "type": "number",
                        "description": "第二个加数"
                    }
                },
                "required": ["a", "b"]
            }
        },
        {
            "name": "calculator_subtract",
            "func": calculator_subtract,
            "description": "计算两个数的差。当用户需要做减法运算时使用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "被减数"
                    },
                    "b": {
                        "type": "number",
                        "description": "减数"
                    }
                },
                "required": ["a", "b"]
            }
        },
        {
            "name": "calculator_multiply",
            "func": calculator_multiply,
            "description": "计算两个数的积。当用户需要做乘法运算时使用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "第一个乘数"
                    },
                    "b": {
                        "type": "number",
                        "description": "第二个乘数"
                    }
                },
                "required": ["a", "b"]
            }
        },
        {
            "name": "calculator_divide",
            "func": calculator_divide,
            "description": "计算两个数的商。当用户需要做除法运算时使用此工具。注意：除数不能为零。",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "被除数"
                    },
                    "b": {
                        "type": "number",
                        "description": "除数（不能为零）"
                    }
                },
                "required": ["a", "b"]
            }
        }
    ]