from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import Request
from typing import List
from models import (
    get_db_client, get_db, GeminiRequest, SimplifiedGeminiResponse,
    WireSchema, WireSchemaUpdate, WireflowSchema, WireflowSchemaUpdate,
    ExecuteWireRequest, ExecuteWireflowRequest, WireExecutionLog, WireflowExecutionLog,
    WireResponse, WireflowResponse  # Import the response models
)
from crud import (
    create_wire, get_wire, update_wire, delete_wire, list_wires,
    create_wireflow, get_wireflow, update_wireflow, delete_wireflow, list_wireflows,
    execute_wire, execute_wireflow, ask_gemini
)
from logger import logger  # Import the shared logger

# Initialize FastAPI app
app = FastAPI(
    title="GeminiWire API",
    description="A simple API for executing wire functions and managing wireflows.",
    version="0.5.1",
)

# Get allowed origins from environment variables
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    logger.info("Starting up database client...")
    app.mongodb_client = get_db_client()
    app.mongodb = get_db()
    logger.info("Database client started successfully.")

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Shutting down database client...")
    app.mongodb_client.close()
    logger.info("Database client shut down successfully.")

@app.get("/")
async def home(request: Request):
    def get_docs_url(request: Request) -> str:
        return f"{request.url.scheme}://{request.client.host}:{request.url.port}/docs"
    
    def get_redoc_url(request: Request) -> str:
        return f"{request.url.scheme}://{request.client.host}:{request.url.port}/redoc"

    return {
        "message": "Welcome to the GeminiWire API, your gateway to seamless wire and wireflow management and execution.",
        "docs_url": get_docs_url(request),
        "redoc_url": get_redoc_url(request)
    }

# Wire Routes
@app.post("/wires/", response_model=WireResponse)
async def create_wire_route(wire: WireSchema):
    return await create_wire(wire)

@app.get("/wires/{wire_id}", response_model=WireResponse)
async def get_wire_route(wire_id: str):
    return await get_wire(wire_id)

@app.put("/wires/{wire_id}", response_model=WireResponse)
async def update_wire_route(wire_id: str, wire: WireSchemaUpdate):
    return await update_wire(wire_id, wire)

@app.delete("/wires/{wire_id}", response_model=dict)
async def delete_wire_route(wire_id: str):
    return await delete_wire(wire_id)

@app.get("/wires/", response_model=List[WireResponse])
async def list_wires_route():
    return await list_wires()

# Wire Execution Route
@app.post("/wires/execute", response_model=WireExecutionLog)
async def execute_wire_route(request: ExecuteWireRequest):
    logger.info(f"Executing wire with ID: {request.wire_id}")
    logger.debug(f"Inputs provided: {request.inputs}")

    try:
        execution_log = await execute_wire(request.wire_id, request.inputs)
        return execution_log
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error executing wire {request.wire_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Wireflow Routes
@app.post("/wireflows/", response_model=WireflowResponse)
async def create_wireflow_route(wireflow: WireflowSchema):
    return await create_wireflow(wireflow)

@app.get("/wireflows/{wireflow_id}", response_model=WireflowResponse)
async def get_wireflow_route(wireflow_id: str):
    return await get_wireflow(wireflow_id)

@app.put("/wireflows/{wireflow_id}", response_model=WireflowResponse)
async def update_wireflow_route(wireflow_id: str, wireflow: WireflowSchemaUpdate):
    return await update_wireflow(wireflow_id, wireflow)

@app.delete("/wireflows/{wireflow_id}", response_model=dict)
async def delete_wireflow_route(wireflow_id: str):
    return await delete_wireflow(wireflow_id)

@app.get("/wireflows/", response_model=List[WireflowResponse])
async def list_wireflows_route():
    return await list_wireflows()

@app.post("/wireflows/execute", response_model=WireflowExecutionLog)
async def execute_wireflow_route(request: ExecuteWireflowRequest):
    logger.info(f"Executing wireflow with ID: {request.wireflow_id}")
    logger.debug(f"Inputs provided: {request.inputs}")

    try:
        # Fetch the wireflow from the database
        wireflow = await get_wireflow(request.wireflow_id)
        if not wireflow:
            logger.error(f"Wireflow not found with ID: {request.wireflow_id}")
            raise HTTPException(status_code=404, detail="Wireflow not found")

        # Execute the wireflow
        execution_log = await execute_wireflow(wireflow, request.inputs)
        return execution_log
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error executing wireflow {request.wireflow_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")