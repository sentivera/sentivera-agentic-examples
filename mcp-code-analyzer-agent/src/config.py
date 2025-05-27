from pydantic import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

class ServerSettings(BaseSettings):
    """Server configuration settings"""
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    RELOAD: bool = True
    
    # Security settings
    CORS_ORIGINS: List[str] = ["*"]
    API_KEY_HEADER: str = "X-API-Key"
    API_KEY: Optional[str] = None
    
    # Model settings
    SUPPORTED_MODELS: List[str] = ["ast_parser", "dependency_graph"]
    DEFAULT_MODEL: str = "ast_parser"
    
    # File paths
    BASE_DIR: Path = Path(__file__).parent.parent
    LOG_DIR: Path = BASE_DIR / "logs"
    OUTPUT_DIR: Path = BASE_DIR / "output"
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = ServerSettings()

# Ensure directories exist
settings.LOG_DIR.mkdir(exist_ok=True)
settings.OUTPUT_DIR.mkdir(exist_ok=True) 