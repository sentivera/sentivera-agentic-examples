"""
Tool Registry Module

This module maintains a central registry of available tools that can be used through the MCP protocol.
The registry maps tool names to their corresponding tool implementations, making it easy
to look up and access tools by name.

Each tool in the registry should be a callable object that implements the tool's functionality.
Tools can be registered using the @mcp_tool decorator.
"""

from typing import Callable, Dict, Any, Optional
from functools import wraps
from .schemas import MCPRequest, MCPResponse
import asyncio
import logging

logger = logging.getLogger(__name__)

# Dictionary mapping tool names to their implementations
# Add new tools to this registry to make them available to the chatbot
TOOL_REGISTRY: Dict[str, Callable] = {}

def mcp_tool(name: Optional[str] = None, description: Optional[str] = None):
    """
    Decorator to register a tool in the MCP system.
    
    Args:
        name (str, optional): The name to register the tool under. If not provided,
                            the function's __name__ will be used.
        description (str, optional): A description of what the tool does.
    
    Returns:
        Callable: The decorator function
    """
    def decorator(func: Callable) -> Callable:
        tool_name = name or func.__name__
        logger.info(f"Registering tool: {tool_name}")
        
        @wraps(func)
        async def wrapper(request: MCPRequest) -> MCPResponse:
            try:
                # Extract parameters from the MCP request
                params = request.parameters or {}
                
                # Call the original function with the parameters
                result = await func(**params) if asyncio.iscoroutinefunction(func) else func(**params)
                
                # Create MCP response
                return MCPResponse(
                    status="success",
                    content=result,
                    metadata={
                        "tool": tool_name,
                        "description": description or func.__doc__ or ""
                    }
                )
            except Exception as e:
                return MCPResponse(
                    status="error",
                    content=str(e),
                    metadata={
                        "tool": tool_name,
                        "error": True
                    }
                )
            
        # Register the wrapped function
        TOOL_REGISTRY[tool_name] = wrapper
        logger.info(f"Successfully registered tool: {tool_name}")
        return wrapper
    return decorator

# Example usage:
# @mcp_tool(description="Evaluates mathematical expressions")
# async def math_tool(expression: str) -> str:
#     # Tool implementation
#     pass

def mcp_tool_copy(name: Optional[str] = None, description: Optional[str] = None):
    """
    Decorator to register a tool in the MCP system.
    
    Args:
        name (str, optional): The name to register the tool under. If not provided,
                            the function's __name__ will be used.
        description (str, optional): A description of what the tool does.
    
    Returns:
        Callable: The decorator function
    """
    def decorator(func: Callable) -> Callable:
        tool_name = name or func.__name__
        logger.info(f"Registering tool (copy): {tool_name}")
        
        @wraps(func)
        async def wrapper(request: MCPRequest) -> MCPResponse:
            try:
                # Extract parameters from the MCP request
                params = request.parameters or {}
                
                # Call the original function with the parameters
                result = await func(**params) if asyncio.iscoroutinefunction(func) else func(**params)
                
                # Create MCP response
                return MCPResponse(
                    status="success",
                    content=result,
                    metadata={
                        "tool": tool_name,
                        "description": description or func.__doc__ or ""
                    }
                )
            except Exception as e:
                return MCPResponse(
                    status="error",
                    content=str(e),
                    metadata={
                        "tool": tool_name,
                        "error": True
                    }
                )
            
        # Register the wrapped function
        TOOL_REGISTRY[tool_name] = wrapper
        logger.info(f"Successfully registered tool (copy): {tool_name}")
        return wrapper
    return decorator
