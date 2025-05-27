from pydantic import BaseModel

class ASTInput(BaseModel):
    root_path: str

class CodeAnalysisInput(BaseModel):
    root_path: str
