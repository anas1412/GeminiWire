from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_service import execute
from crud_service import add_wire, update_wire, delete_wire, list_wires, fetch_wire
from models import WireFunctionRequest, WireFunctionResponse
from typing import Dict, Any, List
import wire_definitions 
import inspect
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # For local development
        "https://gemini-wire-ui.vercel.app",  # Vercel frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/wire/{function_name}", response_model=WireFunctionRequest)
async def get_wire(function_name: str):
    try:
        wire_details = fetch_wire(function_name)
        if wire_details:
            return WireFunctionRequest(
                function_name=wire_details["function_name"],
                inputs=wire_details["inputs"],
                description=wire_details["description"],
            )
        else:
            raise HTTPException(status_code=404, detail=f"Function '{function_name}' not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))