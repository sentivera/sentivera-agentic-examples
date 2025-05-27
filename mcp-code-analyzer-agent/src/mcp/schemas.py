from pydantic import BaseModel
from typing import Dict, Any, Optional

class MCPRequest(BaseModel):
    """Model Content Protocol request model"""
    model: str
    content: Dict[str, Any]
    parameters: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    """Model Content Protocol response model"""
    status: str
    content: Any
    metadata: Dict[str, Any] 