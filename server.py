from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gemini_service import execute
from typing import Dict, Any, List
import function_definitions 
import inspect

app = FastAPI()

# Define the request model for Gemini input (no need for "prompt")
class GeminiRequest(BaseModel):
    function_name: str  # Used for logging or categorizing the request
    inputs: Dict[str, Any]  # Used for other input parameters if necessary

# Define the response model for Gemini output
class GeminiResponse(BaseModel):
    function_name: str  # Function name included in the response for logging
    outputs: str  # Expect a string output, not a dictionary

@app.post("/execute", response_model=GeminiResponse)
async def wire_function(request: GeminiRequest):
    try:
        # Call the gemini_service to execute the request and get the response
        response = execute(request.function_name, request.inputs)
        
        # Handle the response status and print result or error
        if response.status == "success":
            print(f"Function Output: {response.data}")
        else:
            print(f"Error: {response.message}")
        
        # Return the output in the format GeminiResponse expects
        return GeminiResponse(function_name=request.function_name, outputs=str(response.data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
