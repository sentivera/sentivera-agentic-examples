from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.mcp.schemas import MCPRequest, MCPResponse
from src.mcp.handler import MCPHandler
from typing import Dict, Any, List, Optional
import uvicorn
import logging
from datetime import datetime
from src.mcp.config import settings
import requests

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

# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.mcp.mcp_server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    ) 