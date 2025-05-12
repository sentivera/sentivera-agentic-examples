"""
Tool Registry Module

This module maintains a central registry of available tools that can be used by the chatbot.
The registry maps tool names to their corresponding tool implementations, making it easy
to look up and access tools by name.

Each tool in the registry should be a callable object that implements the tool's functionality.
"""

from tools.math_tool import math_tool

# Dictionary mapping tool names to their implementations
# Add new tools to this registry to make them available to the chatbot
TOOL_REGISTRY = {
    "math_tool": math_tool  # Mathematical operations tool
}
