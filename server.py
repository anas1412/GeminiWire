from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gemini_service import execute
from crud_service import add_wire, update_wire, delete_wire, list_wires
from typing import Dict, Any, List
import wire_definitions 
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
    output: str  # Expect a string output, not a dictionary



@app.post("/execute", response_model=GeminiResponse)
async def wire_function(request: GeminiRequest):
    try:
        response = execute(request.function_name, request.inputs)
        
        if response.status == "success":
            print(f"Function Output: {response.data}")
        else:
            print(f"Error: {response.message}")
        
        return GeminiResponse(function_name=request.function_name, output=str(response.data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


##################################################################################################

# Model for input data for functions like add_wire, update_wire, etc.
class WireFunctionRequest(BaseModel):
    function_name: str
    inputs: List[str]  # List of input parameter names
    description: str   # Description for the wire function

# Model for output data
class WireFunctionResponse(BaseModel):
    message: str

@app.post("/wire/add", response_model=WireFunctionResponse)
async def create_wire(request: WireFunctionRequest):
    try:
        add_wire(request.function_name, request.inputs, request.description)
        return WireFunctionResponse(message=f"Wire '{request.function_name}' added successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/wire/update", response_model=WireFunctionResponse)
async def update_existing_wire(request: WireFunctionRequest):
    try:
        update_wire(request.function_name, request.inputs, request.description)
        return WireFunctionResponse(message=f"Wire '{request.function_name}' updated successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/wire/delete/{function_name}", response_model=WireFunctionResponse)
async def delete_existing_wire(function_name: str):
    try:
        delete_wire(function_name)
        return WireFunctionResponse(message=f"Wire '{function_name}' deleted successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/wires", response_model=List[str])
async def get_all_wires():
    try:
        wires = list_wires()
        return wires
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))