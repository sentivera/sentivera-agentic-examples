from typing import Any, Dict
from .models import ModelType
from .schemas import MCPRequest
import logging
from ..tools.ast_parser_tool import parse_code
import requests

logger = logging.getLogger(__name__)

class MCPHandler:
    """Handler for processing MCP requests"""
    
    def __init__(self):
        pass
    
    async def process_request(self, request: MCPRequest) -> Dict[str, Any]:
        """
        Process an MCP request using the specified model.
        
        Args:
            request (MCPRequest): The analysis request
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        try:
            # Validate model type
            model_type = ModelType(request.model)
            
            # Process based on model type
            if model_type == ModelType.AST_PARSER:
                return await self._process_ast_parser(request)
            elif model_type == ModelType.DEPENDENCY_GRAPH:
                return await self._process_dependency_graph(request)
            else:
                raise ValueError(f"Unsupported model type: {request.model}")
                
        except ValueError as e:
            logger.error(f"Invalid model type: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            raise
    
    async def _process_ast_parser(self, request: MCPRequest) -> Dict[str, Any]:
        """Process request using AST parser"""
        try:
            # Get code from request content
            code = request.content.get("code", "")
            if not code:
                raise ValueError("No code provided in request content")
            
            # Parse code using AST parser
            result = parse_code(code)
            
            # Add request metadata
            result["request_metadata"] = {
                "model": request.model,
                "parameters": request.parameters or {}
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in AST parsing: {str(e)}")
            raise
    
    async def _process_dependency_graph(self, request: MCPRequest) -> Dict[str, Any]:
        """Process request using dependency graph analyzer"""
        # TODO: Implement dependency graph processing
        return {
            "dependencies": "Dependency graph results will be implemented here",
            "code": request.content.get("code", "")
        } 