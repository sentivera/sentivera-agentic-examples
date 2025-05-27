from enum import Enum
from typing import List, Dict, Any

class ModelType(str, Enum):
    """Enum representing available model types for code analysis"""
    
    AST_PARSER = "ast_parser"
    DEPENDENCY_GRAPH = "dependency_graph"
    
    @property
    def description(self) -> str:
        """Get the description of the model type"""
        descriptions = {
            self.AST_PARSER: "Abstract Syntax Tree parser for code analysis",
            self.DEPENDENCY_GRAPH: "Dependency graph analyzer for code relationships"
        }
        return descriptions[self]
    
    @property
    def capabilities(self) -> List[str]:
        """Get the capabilities of the model type"""
        capabilities = {
            self.AST_PARSER: [
                "syntax_analysis",
                "code_structure",
                "ast_traversal"
            ],
            self.DEPENDENCY_GRAPH: [
                "import_analysis",
                "dependency_tracking",
                "relationship_mapping"
            ]
        }
        return capabilities[self] 