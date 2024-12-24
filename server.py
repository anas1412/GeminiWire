from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from gemini_request import execute
from crud_service import add_wire, update_wire, delete_wire, list_wires, fetch_wire, fetch_wires
from models import WireFunctionRequest, WireFunctionResponse, GeminiRequest, GeminiResponse, WireFunctionDetails
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

# Get allowed origins from environment variables
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GeminiRequest(BaseModel):
    function_name: str = Field(..., example="multiply")
    inputs: Dict[str, Any] = Field(..., example={"num1": 5, "num2": 10})

class GeminiResponse(BaseModel):
    function_name: str
    status: str
    data: Optional[Any]
    message: Optional[str] = None

@app.post("/execute", response_model=GeminiResponse)
async def wire_function(request: GeminiRequest):
    """Execute a wire function with the given inputs."""
    try:
        response = execute(request.function_name, request.inputs)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/wire/add", response_model=WireFunctionResponse)
async def create_wire(request: WireFunctionRequest):
    """Add a new wire function."""
    try:
        add_wire(request.function_name, request.inputs, request.description, request.prompt)
        return WireFunctionResponse(message=f"Wire '{request.function_name}' added successfully.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/wire/update", response_model=WireFunctionResponse)
async def update_existing_wire(request: WireFunctionRequest):
    """Update an existing wire function."""
    try:
        update_wire(request.function_name, request.inputs, request.description, request.prompt)
        return WireFunctionResponse(message=f"Wire '{request.function_name}' updated successfully.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/wire/delete/{function_name}", response_model=WireFunctionResponse)
async def delete_existing_wire(function_name: str):
    """Delete a wire function."""
    try:
        delete_wire(function_name)
        return WireFunctionResponse(message=f"Wire '{function_name}' deleted successfully.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/wires", response_model=List[str])
async def get_all_wires():
    """List all wire function names."""
    try:
        wires = list_wires()
        return wires
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/wires/details", response_model=Dict[str, Any])
async def get_all_wire_details():
    """Fetch details of all wire functions."""
    try:
        wires = fetch_wires()
        return wires
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/wire/{function_name}", response_model=WireFunctionDetails)
async def get_wire(function_name: str):
    """Fetch details of a specific wire function."""
    try:
        wire_details = fetch_wire(function_name)
        return WireFunctionDetails(
            function_name=function_name,
            inputs=wire_details["inputs"],
            description=wire_details["description"],
            prompt=wire_details["prompt"],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
