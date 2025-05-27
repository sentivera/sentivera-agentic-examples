import os
import sys
from typing import Dict, Any, List, Set
import ast
from pathlib import Path
import json

class ASTFileDependencyGraph:
    """
    Tool to create file-level dependency graphs from AST parser results.
    Analyzes import statements to build a JSON representation of file dependencies.
    """
    
    def _extract_imports(self, file_path: str) -> Set[str]:
        """
        Extract import statements from a Python file.
        
        Args:
            file_path (str): Path to the Python file
            
        Returns:
            Set[str]: Set of imported module names
        """
        imports = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.add(name.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
                        
        except Exception as e:
            print(f"Error parsing imports from {file_path}: {str(e)}")
            
        return imports
    
    def _extract_symbols(self, file_path: str) -> Dict[str, List[str]]:
        """
        Extract classes and functions from a Python file.
        
        Args:
            file_path (str): Path to the Python file
            
        Returns:
            Dict[str, List[str]]: Dictionary containing lists of classes and functions
        """
        symbols = {"classes": [], "functions": []}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    symbols["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    symbols["functions"].append(node.name)
                    
        except Exception as e:
            print(f"Error parsing symbols from {file_path}: {str(e)}")
            
        return symbols
    
    def _normalize_path(self, file_path: str, root_path: str) -> str:
        """
        Normalize file path to be relative to root path.
        
        Args:
            file_path (str): Full path to the file
            root_path (str): Root directory path
            
        Returns:
            str: Normalized relative path
        """
        try:
            rel_path = os.path.relpath(file_path, root_path)
            return rel_path.replace(os.sep, '.')
        except:
            return file_path
    
    def _determine_layer(self, file_path: str) -> str:
        """
        Determine the architectural layer of a file based on its path.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: Layer name (e.g., 'data', 'api', 'core', etc.)
        """
        path_parts = file_path.split(os.sep)
        if 'api' in path_parts:
            return 'api'
        elif 'models' in path_parts or 'data' in path_parts:
            return 'data'
        elif 'core' in path_parts or 'utils' in path_parts:
            return 'core'
        else:
            return 'other'
    
    def build_graph(self, ast_results: Dict[str, Any], root_path: str) -> Dict[str, Any]:
        """
        Build a JSON representation of file dependencies from AST parser results.
        
        Args:
            ast_results (Dict[str, Any]): Results from AST parser
            root_path (str): Root directory path
            
        Returns:
            Dict[str, Any]: Dictionary containing nodes and edges
        """
        nodes = []
        edges = []
        
        # Process each file
        for file_info in ast_results.get('files_processed', []):
            if file_info['status'] == 'success':
                file_path = file_info['path']
                normalized_path = self._normalize_path(file_path, root_path)
                
                # Extract symbols
                symbols = self._extract_symbols(file_path)
                
                # Create node
                node = {
                    "id": normalized_path,
                    "type": "file",
                    "symbol_count": len(symbols["classes"]) + len(symbols["functions"]),
                    "classes": symbols["classes"],
                    "functions": symbols["functions"],
                    "layer": self._determine_layer(file_path)
                }
                nodes.append(node)
                
                # Extract and process imports
                imports = self._extract_imports(file_path)
                for imp in imports:
                    # Find matching target file
                    for target_node in nodes:
                        if imp in target_node["id"] or target_node["id"] in imp:
                            edge = {
                                "source": normalized_path,
                                "target": target_node["id"],
                                "type": "imports",
                                "weight": 1  # Could be enhanced to count number of imports
                            }
                            edges.append(edge)
        
        return {
            "nodes": nodes,
            "edges": edges
        }

def create_dependency_graph(ast_results: Dict[str, Any], root_path: str, output_path: str = None) -> Dict[str, Any]:
    """
    Create a file-level dependency graph from AST parser results.
    
    Args:
        ast_results (Dict[str, Any]): Results from AST parser
        root_path (str): Root directory path
        output_path (str, optional): Path to save the JSON output
        
    Returns:
        Dict[str, Any]: Graph data in JSON format
    """
    graph_tool = ASTFileDependencyGraph()
    graph_data = graph_tool.build_graph(ast_results, root_path)
    
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(graph_data, f, indent=2)
    
    return graph_data 