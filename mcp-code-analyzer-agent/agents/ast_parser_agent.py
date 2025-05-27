import ast
import os
import logging
from typing import Dict, Any, List
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class ASTParserAgent:
    """
    Agent responsible for parsing Python files and extracting AST (Abstract Syntax Tree) information.
    Analyzes Python files in a given directory and its subdirectories to find functions and classes.
    """
    
    def run(self, root_path: str) -> Dict[str, Any]:
        """
        Process Python files in the given root path and extract AST information.
        
        Args:
            root_path (str): Path to the root directory to analyze
            
        Returns:
            dict: Dictionary containing:
                - status: Success or error status
                - summary: Summary statistics of the analysis
                - files_processed: List of all Python files found and their processing status
                - details: Detailed analysis results including symbols
        """
        result = {}
        files_processed = []
        logger.info(f"Starting AST analysis for path: {root_path}")

        try:
            # Walk through all directories and files in the root path
            for dirpath, _, filenames in os.walk(root_path):
                for file in filenames:
                    # Only process Python files
                    if file.endswith(".py"):
                        full_path = os.path.join(dirpath, file)
                        logger.debug(f"Processing file: {full_path}")
                        try:
                            # Read and parse the Python file
                            with open(full_path, "r", encoding="utf-8") as f:
                                # Parse the file content into an AST
                                tree = ast.parse(f.read())
                                # Extract function and class definitions
                                symbols = [
                                    {
                                        "name": node.name,  # Name of the function/class
                                        "type": type(node).__name__,  # Type (FunctionDef/ClassDef)
                                        "lineno": node.lineno  # Line number in the file
                                    }
                                    for node in ast.walk(tree)
                                    if isinstance(node, (ast.FunctionDef, ast.ClassDef))
                                ]
                                # Store the symbols for this file
                                result[full_path] = symbols
                                logger.debug(f"Found {len(symbols)} symbols in {full_path}")
                                files_processed.append({
                                    "path": full_path,
                                    "status": "success",
                                    "symbols_count": len(symbols)
                                })
                        except Exception as e:
                            # Skip files that can't be parsed
                            logger.warning(f"Failed to parse {full_path}: {str(e)}")
                            files_processed.append({
                                "path": full_path,
                                "status": "error",
                                "error": str(e)
                            })
                            continue

            # Calculate summary statistics
            successful_files = len([f for f in files_processed if f["status"] == "success"])
            failed_files = len([f for f in files_processed if f["status"] == "error"])

            # Format the response
            response = {
                "status": "success",
                "summary": {
                    "total_files": len(files_processed),
                    "successful_files": successful_files,
                    "failed_files": failed_files
                },
                "files_processed": files_processed,
                "details": {
                    "symbols": result
                }
            }

            logger.info(f"Completed AST analysis. Processed {len(result)} files")
            return response

        except Exception as e:
            logger.error(f"Error during AST analysis: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": str(e),
                "path": root_path
            } 