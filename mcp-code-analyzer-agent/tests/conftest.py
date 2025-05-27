import pytest
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

@pytest.fixture
def test_code():
    """Sample Python code for testing"""
    return """
def hello_world():
    print("Hello, World!")
    return True

class TestClass:
    def __init__(self):
        self.value = 42
    
    def get_value(self):
        return self.value
    """

@pytest.fixture
def test_dependency_code():
    """Sample Python code with dependencies for testing"""
    return """
from typing import List, Dict
import os
import json

def process_files(files: List[str]) -> Dict[str, str]:
    results = {}
    for file in files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                results[file] = f.read()
    return results
    """

@pytest.fixture
def valid_request_data(test_code):
    """Valid MCP request data"""
    return {
        "model": "ast_parser",
        "content": {
            "code": test_code,
            "options": {}
        },
        "parameters": {}
    }

@pytest.fixture
def test_output_dir():
    """Test output directory"""
    output_dir = project_root / "tests" / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir 