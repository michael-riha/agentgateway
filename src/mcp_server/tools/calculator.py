from mcp.server.fastmcp import FastMCP
import math

def setup_calculator_tools(mcp: FastMCP):
    """Setup calculator tools as shown in the article"""
    
    @mcp.tool()
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        print(f'called add-calculator-MCPTool with {a}+ {b}')
        return a + b

    @mcp.tool()
    def subtract(a: int, b: int) -> int:
        """Subtract two numbers"""
        return a - b

    @mcp.tool()
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b

    @mcp.tool()
    def divide(a: int, b: int) -> float:
        """Divide two numbers"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    @mcp.tool()
    def power(a: int, b: int) -> int:
        """Power of two numbers"""
        return a ** b

    @mcp.tool()
    def sqrt(a: int) -> float:
        """Square root of a number"""
        return math.sqrt(a)

    @mcp.tool()
    def factorial(a: int) -> int:
        """Factorial of a number"""
        return math.factorial(a)

    @mcp.tool()
    def log(a: int) -> float:
        """Natural logarithm of a number"""
        return math.log(a)

    @mcp.tool()
    def sin(a: int) -> float:
        """Sine of a number (in radians)"""
        return math.sin(a)

    @mcp.tool()
    def cos(a: int) -> float:
        """Cosine of a number (in radians)"""
        return math.cos(a)

    @mcp.tool()
    def tan(a: int) -> float:
        """Tangent of a number (in radians)"""
        return math.tan(a)