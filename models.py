from pydantic import BaseModel
from typing import Any, Dict, Optional, Union

class GeminiRequest(BaseModel):
    function_name: str
    inputs: Dict[str, Any]

class GeminiResponse(BaseModel):
    function_name: str
    status: str
    data: Optional[Any]
    message: Optional[str] = None