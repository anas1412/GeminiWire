from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# MongoDB connection
def get_db_client():
    return AsyncIOMotorClient(MONGO_URI)

def get_db():
    client = get_db_client()
    return client[DATABASE_NAME]

#########################################################

class GeminiRequest(BaseModel):
    prompt: str  # The wire's prompt

class SimplifiedGeminiResponse(BaseModel):
    data: str

#########################################################

# Wire Schema
class WireSchema(BaseModel):
    wire_id: str = Field(..., example="generate_test_msg")
    description: str = Field(..., example="Generate a test statement from a provided name")
    prompt: str = Field(..., example="Generate a test statement from {name}")
    inputs: Dict[str, str] = Field(..., example={"name": "A name to generate the test statement"})
    output_key: Optional[str] = Field(None, example="name_generated")

# Wire Schema Update
class WireSchemaUpdate(BaseModel):
    wire_id: str | None = None
    description: str | None = None
    prompt: str | None = None
    inputs: Dict[str, str] | None = None
    output_key: str | None = None

#########################################################

# Simplified Wire Schema for Wireflows
class WireflowWireSchema(BaseModel):
    wire_id: str = Field(..., example="wire_1")
    inputs: Dict[str, str] = Field(..., example={"name": "Alice"})
    output_key: Optional[str] = Field(None, example="name_generated")

# Wireflow Schema
class WireflowSchema(BaseModel):
    wireflow_id: str = Field(..., example="greeting_wireflow")
    description: str = Field(..., example="Generate a greeting using a random name")
    wires: List[WireflowWireSchema] = Field(
        ...,
        example=[
            {
                "wire_id": "wire_1",
                "inputs": {},
                "output_key": "name_generated"
            },
            {
                "wire_id": "wire_2",
                "inputs": {"name": "{name_generated}"},
                "output_key": "greeting_result"
            }
        ],
        description="List of wires in the wireflow. Each wire must already exist in the database."
    )

# Wireflow Schema Update
class WireflowSchemaUpdate(BaseModel):
    wireflow_id: str | None = Field(None, example="greeting_wireflow")
    description: str | None = Field(None, example="Generate a greeting using a random name")
    wires: List[WireflowWireSchema] | None = Field(
        None,
        example=[
            {
                "wire_id": "wire_1",
                "inputs": {},
                "output_key": "name_generated"
            }
        ],
        description="List of wires in the wireflow. Each wire must already exist in the database."
    )

#########################################################

class ExecuteWireRequest(BaseModel):
    wire_id: str = Field(..., example="generate_name")
    inputs: Dict[str, str] = Field(..., example={"name": "Alice"})

class ExecuteWireflowRequest(BaseModel):
    wireflow_id: str = Field(..., example="greeting_wireflow")
    inputs: Dict[str, str] = Field(..., example={})

#########################################################

class WireExecutionLog(BaseModel):
    wire_id: str
    inputs: Dict[str, str]  # Inputs provided to the wire
    output: str  # Output generated by the wire
    status: str  # Execution status (e.g., "success", "failed")
    error_message: Optional[str] = None  # Error message if the wire failed
    executed_at: str  # Timestamp of execution

class WireflowExecutionLog(BaseModel):
    wireflow_id: str
    inputs: Dict[str, str]  # Initial inputs provided to the wireflow
    wire_executions: List[WireExecutionLog]  # Execution logs for each wire
    final_output: str  # Final output of the wireflow
    status: str  # Overall status of the wireflow execution
    error_message: Optional[str] = None  # Error message if the wireflow failed
    executed_at: str  # Timestamp of execution

#########################################################

# Response Models
class WireResponse(BaseModel):
    id: str
    wire_id: str
    description: str
    prompt: str
    inputs: Dict[str, str]
    output_key: Optional[str] = None

class WireflowResponse(BaseModel):
    id: str
    wireflow_id: str
    description: str
    wires: List[Dict[str, Union[str, Dict[str, str]]]]