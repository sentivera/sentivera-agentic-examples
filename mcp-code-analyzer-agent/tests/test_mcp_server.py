import pytest
from fastapi.testclient import TestClient
from server.mcp_server import app
from mcp import MCPRequest, ModelType
import json

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data

def test_list_models():
    """Test the model listing endpoint"""
    response = client.get("/mcp/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) > 0
    for model in data["models"]:
        assert "id" in model
        assert "name" in model
        assert "description" in model
        assert "capabilities" in model

def test_analyze_code_ast_parser():
    """Test AST parser analysis endpoint"""
    request_data = {
        "model": "ast_parser",
        "content": {
            "code": """
def hello_world():
    print("Hello, World!")
            """,
            "options": {}
        },
        "parameters": {}
    }
    
    response = client.post("/mcp/analyze", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "content" in data
    assert "metadata" in data
    assert data["metadata"]["model"] == "ast_parser"

def test_analyze_code_dependency_graph():
    """Test dependency graph analysis endpoint"""
    request_data = {
        "model": "dependency_graph",
        "content": {
            "code": """
from typing import List
import os

def process_files(files: List[str]) -> None:
    for file in files:
        if os.path.exists(file):
            print(f"Processing {file}")
            """,
            "options": {}
        },
        "parameters": {}
    }
    
    response = client.post("/mcp/analyze", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "content" in data
    assert "metadata" in data
    assert data["metadata"]["model"] == "dependency_graph"

def test_invalid_model():
    """Test analysis with invalid model type"""
    request_data = {
        "model": "invalid_model",
        "content": {
            "code": "print('test')",
            "options": {}
        },
        "parameters": {}
    }
    
    response = client.post("/mcp/analyze", json=request_data)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data

def test_missing_content():
    """Test analysis with missing content"""
    request_data = {
        "model": "ast_parser",
        "parameters": {}
    }
    
    response = client.post("/mcp/analyze", json=request_data)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data

def test_invalid_request_format():
    """Test analysis with invalid request format"""
    request_data = {
        "invalid_field": "value"
    }
    
    response = client.post("/mcp/analyze", json=request_data)
    assert response.status_code == 422  # FastAPI validation error 