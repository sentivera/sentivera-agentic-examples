import os
import sys
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.append(str(src_path))

# Import and run the server
from src.mcp.mcp_server import app
import uvicorn
from src.mcp.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.mcp.mcp_server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    ) 