"""
A simple mathematical expression evaluator tool.

This module provides a function that safely evaluates mathematical expressions
provided as strings. It can handle basic arithmetic operations and returns either
the calculated result or an error message if the expression is invalid.
"""

def math_tool(input_text: str) -> str:
    """
    Evaluates a mathematical expression provided as a string.

    Args:
        input_text (str): A string containing a mathematical expression to evaluate.
                         Examples: "2 + 2", "10 * 5", "100 / 4"

    Returns:
        str: A string containing either:
            - The result of the calculation in the format "The result is {result}"
            - An error message if the expression is invalid or cannot be evaluated

    Note:
        This function uses Python's built-in eval() function, which can be dangerous
        if used with untrusted input. It should only be used with controlled,
        mathematical expressions.
    """
    try:
        # Evaluate the mathematical expression
        result = eval(input_text)
        return f"The result is {result}"
    except Exception as e:
        # Return error message if evaluation fails
        return f"Error: {str(e)}"