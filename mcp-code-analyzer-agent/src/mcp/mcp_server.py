from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from mcp import MCPRequest, MCPResponse, MCPHandler
from mcp.models import ModelType
from typing import Dict, Any, List, Optional
import uvicorn
import logging
from datetime import datetime
from .config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Model Content Protocol Server",
    description="Server implementing the Model Content Protocol for code analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP handler
mcp_handler = MCPHandler()

# Request handlers
@app.post("/mcp/analyze", response_model=MCPResponse)
async def analyze_code(request: MCPRequest) -> MCPResponse:
    """
    Analyze code using the specified model.
    
    Args:
        request (MCPRequest): The analysis request containing model and content
        
    Returns:
        MCPResponse: Analysis results
    """
    try:
        logger.info(f"Received analysis request for model: {request.model}")
        
        # Validate request
        if not request.model or not request.content:
            raise HTTPException(status_code=400, detail="Invalid request: model and content are required")
        
        # Process request using MCP handler
        result = await mcp_handler.process_request(request)
        
        return MCPResponse(
            status="success",
            content=result,
            metadata={
                "timestamp": datetime.utcnow().isoformat(),
                "model": request.model
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# Model info endpoint
@app.get("/mcp/models")
async def list_models() -> Dict[str, Any]:
    """List available models and their capabilities"""
    return {
        "models": [
            {
                "id": model.value,
                "name": model.name,
                "description": model.description,
                "capabilities": model.capabilities
            }
            for model in ModelType
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "mcp_server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    ) 