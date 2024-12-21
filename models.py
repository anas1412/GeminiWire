from pydantic import BaseModel
from typing import Any, Dict, Optional, Union, List

class GeminiRequest(BaseModel):
    function_name: str
    inputs: Dict[str, Any]

class GeminiResponse(BaseModel):
    function_name: str
    status: str
    data: Optional[Any]
    message: Optional[str] = None

class WireFunctionRequest(BaseModel):
    function_name: str
    inputs: List[str]  # List of input parameter names
    description: str   # Description for the wire function

class WireFunctionResponse(BaseModel):
    message: str