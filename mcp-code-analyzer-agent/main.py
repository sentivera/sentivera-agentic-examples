# Import required FastAPI components and custom modules
import logging
from fastapi import FastAPI
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.agents.ast_parser import router as ast_parser_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('code_analyzer.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application with metadata and documentation settings
app = FastAPI(
    title="Code Analyzer Agent API",
    description="API for analyzing code using the Code Analyzer Agent",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc"  # ReDoc endpoint
)

# Include routers
app.include_router(ast_parser_router)

