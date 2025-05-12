"""
This module provides functionality for creating MCP (Multi-Component Processing) steps
for the chatbot system. It defines the structure for processing steps that can be
executed by various tools in the system.
"""

def create_mcp_step(user_input: str) -> dict:
    """
    Creates a standardized MCP step configuration for processing user input.

    Args:
        user_input (str): The input text from the user that needs to be processed

    Returns:
        dict: A dictionary containing the step configuration with the following keys:
            - id: Unique identifier for the step
            - name: Name of the bot/component handling the step
            - input: The user's input text
            - tool_name: Name of the tool that will process this step
            - type: Type of the step (e.g., "tool")
    """
    return {
        "id": "step_001",
        "name": "SimpleMathBot",
        "input": user_input,
        "tool_name": "math_tool",
        "type": "tool"
    }
