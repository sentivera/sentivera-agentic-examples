import ast
from typing import Dict, Any, List, Optional
import json
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ASTNode:
    """Represents a node in the Abstract Syntax Tree"""
    type: str
    lineno: int
    col_offset: int
    end_lineno: Optional[int] = None
    end_col_offset: Optional[int] = None
    children: List['ASTNode'] = None
    value: Any = None

    def __post_init__(self):
        if self.children is None:
            self.children = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation"""
        result = asdict(self)
        result['children'] = [child.to_dict() for child in self.children]
        return result

class ASTParser:
    """Tool for parsing Python code into an Abstract Syntax Tree"""
    
    def __init__(self):
        self.current_node = None
        self.node_stack = []

    def parse(self, code: str) -> Dict[str, Any]:
        """
        Parse Python code into an AST representation.
        
        Args:
            code (str): Python source code to parse
            
        Returns:
            Dict[str, Any]: AST representation of the code
        """
        try:
            # Parse the code into an AST
            tree = ast.parse(code)
            
            # Convert AST to our custom representation
            root = self._convert_node(tree)
            
            # Add metadata
            result = {
                "ast": root.to_dict(),
                "metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "node_count": self._count_nodes(root),
                    "max_depth": self._calculate_max_depth(root)
                }
            }
            
            return result
            
        except SyntaxError as e:
            return {
                "error": f"Syntax error: {str(e)}",
                "line": e.lineno,
                "offset": e.offset
            }
        except Exception as e:
            return {
                "error": f"Error parsing code: {str(e)}"
            }

    def _convert_node(self, node: ast.AST) -> ASTNode:
        """Convert an ast.AST node to our custom ASTNode representation"""
        # Create base node
        ast_node = ASTNode(
            type=type(node).__name__,
            lineno=getattr(node, 'lineno', 0),
            col_offset=getattr(node, 'col_offset', 0),
            end_lineno=getattr(node, 'end_lineno', None),
            end_col_offset=getattr(node, 'end_col_offset', None)
        )
        
        # Handle different node types
        if isinstance(node, ast.Name):
            ast_node.value = node.id
        elif isinstance(node, ast.Constant):
            ast_node.value = node.value
        elif isinstance(node, ast.Num):
            ast_node.value = node.n
        elif isinstance(node, ast.Str):
            ast_node.value = node.s
        elif isinstance(node, ast.NameConstant):
            ast_node.value = node.value
            
        # Process child nodes
        for child in ast.iter_child_nodes(node):
            ast_node.children.append(self._convert_node(child))
            
        return ast_node

    def _count_nodes(self, node: ASTNode) -> int:
        """Count total number of nodes in the AST"""
        return 1 + sum(self._count_nodes(child) for child in node.children)

    def _calculate_max_depth(self, node: ASTNode, current_depth: int = 0) -> int:
        """Calculate maximum depth of the AST"""
        if not node.children:
            return current_depth
        return max(self._calculate_max_depth(child, current_depth + 1) 
                  for child in node.children)

def parse_code(code: str) -> Dict[str, Any]:
    """
    Parse Python code into an AST representation.
    
    Args:
        code (str): Python source code to parse
        
    Returns:
        Dict[str, Any]: AST representation of the code
    """
    parser = ASTParser()
    return parser.parse(code)
