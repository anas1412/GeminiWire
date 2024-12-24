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
    function_name: Optional[str] = None
    inputs: Optional[Dict[str, str]] = None
    description: Optional[str] = None
    prompt: Optional[str] = None

class WireFunctionResponse(BaseModel):
    message: str

class WireFunctionDetails(BaseModel):
    function_name: str
    inputs: Dict[str, str]
    description: str
    prompt: str
