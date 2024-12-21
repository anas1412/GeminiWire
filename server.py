from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gemini_service import execute
from crud_service import add_function, update_function, delete_function, list_functions
from typing import Dict, Any, List
import function_definitions 
import inspect
import os

app = FastAPI()

##################################################################################################

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
        response = execute(request.function_name, request.inputs)
        
        if response.status == "success":
            print(f"Function Output: {response.data}")
        else:
            print(f"Error: {response.message}")
        
        return GeminiResponse(function_name=request.function_name, outputs=str(response.data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


##################################################################################################

class FunctionCRUDRequest(BaseModel):
    name: str
    code: str

@app.post("/execute", response_model=GeminiResponse)
async def wire_function(request: GeminiRequest):
    try:
        response = execute(request.function_name, request.inputs)
        if response.status != "success":
            raise HTTPException(status_code=400, detail=response.message)
        return GeminiResponse(function_name=request.function_name, outputs=str(response.data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/function")
async def create_function(request: FunctionCRUDRequest):
    try:
        add_function(request.name, request.code)
        return {"message": f"Function '{request.name}' added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/function")
async def update_existing_function(request: FunctionCRUDRequest):
    try:
        update_function(request.name, request.code)
        return {"message": f"Function '{request.name}' updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/function/{name}")
async def delete_existing_function(name: str):
    try:
        delete_function(name)
        return {"message": f"Function '{name}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/functions")
async def get_all_functions():
    try:
        return {"functions": list_functions()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

##################################################################################################