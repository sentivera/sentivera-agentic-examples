from fastapi import APIRouter, HTTPException, Depends, Query
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from agents.ast_parser_agent import ASTParserAgent
from typing import Dict, Any

class ASTParserController:
    def __init__(self, agent: ASTParserAgent):
        self.agent = agent

    async def parse_ast(self, root_path: str) -> Dict[str, Any]:
        try:
            # Get AST analysis results
            result = self.agent.run(root_path)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

def get_controller() -> ASTParserController:
    return ASTParserController(ASTParserAgent())

router = APIRouter(
    prefix="/api/v1/agents/ast-parser",
    tags=["ast-parser"],
    responses={404: {"description": "Not found"}},
)

@router.get("/parse")
async def parse_ast(
    root_path: str = Query(..., description="Root directory path to analyze for Python files"),
    controller: ASTParserController = Depends(get_controller)
) -> Dict[str, Any]:
    """
    Parse Python files in the specified directory using AST Parser Agent.
    
    Args:
        root_path (str): Path to the root directory to analyze
        controller (ASTParserController): Controller instance for handling the parsing
        
    Returns:
        dict: AST parsing results including symbols and analysis details
    """
    return await controller.parse_ast(root_path) 