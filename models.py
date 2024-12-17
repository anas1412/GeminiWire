from pydantic import BaseModel
from typing import Any, Dict, Optional, Union

class GeminiRequest(BaseModel):
    function_name: str
    inputs: Dict[str, Any]

class GeminiResponse(BaseModel):
    function_name: str
    status: str  # "success" or "error"
    data: Optional[Any]  # The actual output of the function, can be of any type
    message: Optional[str] = None  # Optional message for errors or additional info