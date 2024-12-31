import os
from bson import ObjectId
from fastapi import HTTPException
from typing import Dict, List, Optional, Union
from models import (
    WireSchema, WireSchemaUpdate, WireflowSchema, WireflowSchemaUpdate,
    WireExecutionLog, WireflowExecutionLog, get_db, SimplifiedGeminiResponse,
    WireResponse, WireflowResponse
)
import requests
from dotenv import load_dotenv
from logger import logger  # Import the shared logger
from datetime import datetime

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")

# CRUD operations for Wire
async def create_wire(wire: WireSchema):
    logger.info(f"Creating wire with data: {wire.dict()}")
    wire_data = wire.dict()

    # Check if wire_id already exists
    existing_wire = await get_db()["wires"].find_one({"wire_id": wire_data["wire_id"]})
    if existing_wire:
        logger.error(f"Wire with ID {wire_data['wire_id']} already exists")
        raise HTTPException(status_code=400, detail="Wire with this ID already exists")

    result = await get_db()["wires"].insert_one(wire_data)
    logger.info(f"Wire created with ID: {result.inserted_id}")

    # Fetch the newly created wire and return it as a WireResponse
    new_wire = await get_db()["wires"].find_one({"_id": result.inserted_id})
    if not new_wire:
        logger.error(f"Failed to fetch newly created wire with ID: {result.inserted_id}")
        raise HTTPException(status_code=500, detail="Failed to fetch newly created wire")

    # Convert ObjectId to string and remove the "_id" field
    new_wire["id"] = str(new_wire["_id"])
    del new_wire["_id"]

    # Ensure all required fields are present
    return WireResponse(**new_wire)

async def get_wire(wire_id: str):
    logger.info(f"Fetching wire with ID: {wire_id}")
    wire = await get_db()["wires"].find_one({"wire_id": wire_id})
    if not wire:
        logger.error(f"Wire not found with ID: {wire_id}")
        raise HTTPException(status_code=404, detail="Wire not found")
    wire["id"] = str(wire["_id"])
    del wire["_id"]
    logger.info(f"Wire fetched successfully: {wire}")
    return WireResponse(**wire)

async def update_wire(wire_id: str, wire: WireSchemaUpdate):
    logger.info(f"Updating wire with ID: {wire_id} with data: {wire.dict()}")
    update_data = {k: v for k, v in wire.dict().items() if v is not None}
    if not update_data:
        logger.error("No fields to update")
        raise HTTPException(status_code=400, detail="No fields to update")

    # Perform the update
    result = await get_db()["wires"].update_one(
        {"wire_id": wire_id}, {"$set": update_data}
    )
    logger.info(f"Update result: matched={result.matched_count}, modified={result.modified_count}")

    if result.matched_count == 0:
        logger.error(f"Wire not found with ID: {wire_id}")
        raise HTTPException(status_code=404, detail="Wire not found")

    # Determine the new wire_id if it was updated
    new_wire_id = update_data.get("wire_id", wire_id)

    # Fetch the updated wire using the new wire_id
    updated_wire = await get_db()["wires"].find_one({"wire_id": new_wire_id})
    if not updated_wire:
        logger.error(f"Failed to fetch updated wire with ID: {new_wire_id}")
        raise HTTPException(status_code=500, detail="Failed to fetch updated wire")

    # Convert ObjectId to string and remove the "_id" field
    updated_wire["id"] = str(updated_wire["_id"])
    del updated_wire["_id"]

    logger.info(f"Wire updated successfully: {result.modified_count} fields updated")
    return WireResponse(**updated_wire)


async def delete_wire(wire_id: str):
    logger.info(f"Deleting wire with ID: {wire_id}")
    result = await get_db()["wires"].delete_one({"wire_id": wire_id})
    if result.deleted_count == 0:
        logger.error(f"Wire not found with ID: {wire_id}")
        raise HTTPException(status_code=404, detail="Wire not found")
    logger.info(f"Wire deleted successfully: {result.deleted_count} items deleted")
    return {"deleted_count": result.deleted_count}

async def list_wires():
    logger.info("Listing all wires")
    wires = await get_db()["wires"].find().to_list(100)
    for wire in wires:
        wire["id"] = str(wire["_id"])
        del wire["_id"]
    logger.info(f"Total wires fetched: {len(wires)}")
    return wires

# CRUD operations for Wireflow
async def validate_wires_exist(wire_ids: List[str]):
    for wire_id in wire_ids:
        wire = await get_wire(wire_id)
        if not wire:
            logger.error(f"Wire not found with ID: {wire_id}")
            raise HTTPException(status_code=404, detail=f"Wire with ID {wire_id} not found")

async def create_wireflow(wireflow: WireflowSchema):
    # Validate that all wires exist
    wire_ids = [wire.wire_id for wire in wireflow.wires]
    await validate_wires_exist(wire_ids)

    logger.info(f"Creating wireflow with data: {wireflow.dict()}")
    wireflow_data = wireflow.dict()

    # Check if wireflow_id already exists
    existing_wireflow = await get_db()["wireflows"].find_one({"workflow_id": wireflow_data["workflow_id"]})
    if existing_wireflow:
        logger.error(f"Wireflow with ID {wireflow_data['workflow_id']} already exists")
        raise HTTPException(status_code=400, detail="Wireflow with this ID already exists")

    result = await get_db()["wireflows"].insert_one(wireflow_data)
    logger.info(f"Wireflow created with ID: {result.inserted_id}")

    # Fetch the newly created wireflow and return it as a WireflowResponse
    new_wireflow = await get_db()["wireflows"].find_one({"_id": result.inserted_id})
    if not new_wireflow:
        logger.error(f"Failed to fetch newly created wireflow with ID: {result.inserted_id}")
        raise HTTPException(status_code=500, detail="Failed to fetch newly created wireflow")

    # Convert ObjectId to string and remove the "_id" field
    new_wireflow["id"] = str(new_wireflow["_id"])
    del new_wireflow["_id"]

    return WireflowResponse(**new_wireflow)

async def get_wireflow(wireflow_id: str):
    logger.info(f"Fetching wireflow with ID: {wireflow_id}")
    wireflow = await get_db()["wireflows"].find_one({"workflow_id": wireflow_id})
    if not wireflow:
        logger.error(f"Wireflow not found with ID: {wireflow_id}")
        raise HTTPException(status_code=404, detail="Wireflow not found")

    # Convert ObjectId to string and remove the "_id" field
    wireflow["id"] = str(wireflow["_id"])
    del wireflow["_id"]

    # Ensure the wires field is a list of dictionaries
    if "wires" in wireflow and isinstance(wireflow["wires"], list):
        # If wires is already a list of dictionaries, no conversion is needed
        pass
    else:
        # If wires is not in the expected format, log an error and raise an exception
        logger.error(f"Invalid wires format in wireflow with ID: {wireflow_id}")
        raise HTTPException(status_code=500, detail="Invalid wireflow data format")

    # Return the wireflow as a WireflowResponse object
    return WireflowResponse(**wireflow)

async def update_wireflow(wireflow_id: str, wireflow: WireflowSchemaUpdate):
    # Validate that all wires exist (if wires are provided)
    if wireflow.wires:
        wire_ids = [wire.wire_id for wire in wireflow.wires]
        await validate_wires_exist(wire_ids)

    logger.info(f"Updating wireflow with ID: {wireflow_id} with data: {wireflow.dict()}")
    update_data = {k: v for k, v in wireflow.dict().items() if v is not None}
    if not update_data:
        logger.error("No fields to update")
        raise HTTPException(status_code=400, detail="No fields to update")

    # Perform the update
    result = await get_db()["wireflows"].update_one(
        {"workflow_id": wireflow_id}, {"$set": update_data}  # Use "workflow_id" instead of "wireflow_id"
    )
    logger.info(f"Update result: matched={result.matched_count}, modified={result.modified_count}")

    if result.matched_count == 0:
        logger.error(f"Wireflow not found with ID: {wireflow_id}")
        raise HTTPException(status_code=404, detail="Wireflow not found")

    # Determine the new workflow_id if it was updated
    new_workflow_id = update_data.get("workflow_id", wireflow_id)

    # Fetch the updated wireflow using the new workflow_id
    updated_wireflow = await get_db()["wireflows"].find_one({"workflow_id": new_workflow_id})
    if not updated_wireflow:
        logger.error(f"Failed to fetch updated wireflow with ID: {new_workflow_id}")
        raise HTTPException(status_code=500, detail="Failed to fetch updated wireflow")

    # Convert ObjectId to string and remove the "_id" field
    updated_wireflow["id"] = str(updated_wireflow["_id"])
    del updated_wireflow["_id"]

    # Ensure the wires field is a list of dictionaries
    if "wires" in updated_wireflow and isinstance(updated_wireflow["wires"], list):
        # If wires is already a list of dictionaries, no conversion is needed
        pass
    else:
        # If wires is not in the expected format, log an error and raise an exception
        logger.error(f"Invalid wires format in wireflow with ID: {new_workflow_id}")
        raise HTTPException(status_code=500, detail="Invalid wireflow data format")

    # Return the updated wireflow as a WireflowResponse object
    return WireflowResponse(**updated_wireflow)

async def delete_wireflow(wireflow_id: str):
    logger.info(f"Deleting wireflow with ID: {wireflow_id}")
    result = await get_db()["wireflows"].delete_one({"wireflow_id": wireflow_id})
    if result.deleted_count == 0:
        logger.error(f"Wireflow not found with ID: {wireflow_id}")
        raise HTTPException(status_code=404, detail="Wireflow not found")
    logger.info(f"Wireflow deleted successfully: {result.deleted_count} items deleted")
    return {"deleted_count": result.deleted_count}

async def list_wireflows():
    logger.info("Listing all wireflows")
    wireflows = await get_db()["wireflows"].find().to_list(100)
    for wireflow in wireflows:
        wireflow["id"] = str(wireflow["_id"])
        del wireflow["_id"]
    logger.info(f"Total wireflows fetched: {len(wireflows)}")
    return wireflows

# Wire Execution Logic
async def execute_wire(wire_id: str, inputs: Dict[str, str]) -> WireExecutionLog:
    wire = await get_wire(wire_id)
    if not wire:
        logger.error(f"Wire not found with ID: {wire_id}")
        raise HTTPException(status_code=404, detail="Wire not found")

    try:
        prompt = wire.prompt  # Access the prompt attribute using dot notation
        for key, value in inputs.items():
            prompt = prompt.replace(f"{{{key}}}", value)

        logger.debug(f"Generated prompt for wire {wire_id}: {prompt}")
        logger.info(f"Inputs for wire {wire_id}: {inputs}")

        gemini_response = await ask_gemini(prompt)
        output = gemini_response.data

        execution_log = WireExecutionLog(
            wire_id=wire.wire_id,  # Access the wire_id attribute using dot notation
            inputs=inputs,
            output=output,
            status="success",
            error_message=None,
            executed_at=datetime.now().isoformat()
        )

        logger.info(f"Wire {wire_id} executed successfully. Output: {output}")
        return execution_log
    except Exception as e:
        logger.error(f"Error executing wire {wire_id}: {str(e)}")
        return WireExecutionLog(
            wire_id=wire.wire_id,  # Access the wire_id attribute using dot notation
            inputs=inputs,
            output=None,
            status="failed",
            error_message=str(e),
            executed_at=datetime.now().isoformat()
        )
# Wireflow Execution Logic
async def execute_wireflow(wireflow: Union[WireflowSchema, Dict], inputs: Dict[str, str]) -> WireflowExecutionLog:
    # If wireflow is a dictionary, convert it to a WireflowSchema object
    if isinstance(wireflow, dict):
        wireflow = WireflowSchema(**wireflow)

    wire_executions = []
    final_output = None
    dynamic_outputs = {}

    logger.info(f"Executing wireflow {wireflow.workflow_id} with inputs: {inputs}")

    for wire in wireflow.wires:
        wire_inputs = {}
        for input_key, input_value in wire.inputs.items():
            if isinstance(input_value, str):
                for key, value in dynamic_outputs.items():
                    input_value = input_value.replace(f"{{{key}}}", value)
            wire_inputs[input_key] = input_value

        logger.info(f"Executing wire {wire.wire_id} with inputs: {wire_inputs}")
        wire_response = await execute_wire(wire.wire_id, wire_inputs)

        if wire.output_key:
            dynamic_outputs[wire.output_key] = wire_response.output

        wire_executions.append(wire_response)
        final_output = wire_response.output

    logger.info(f"Wireflow {wireflow.workflow_id} executed successfully. Final output: {final_output}")
    return WireflowExecutionLog(
        workflow_id=wireflow.workflow_id,
        inputs=inputs,
        wire_executions=wire_executions,
        final_output=final_output,
        status="success" if final_output else "failed",
        error_message=None,
        executed_at=datetime.now().isoformat()
    )

# Gemini Integration
async def ask_gemini(req: str) -> SimplifiedGeminiResponse:
    logger.info(f"Asking Gemini: {req}")
    
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": req}]
        }]
    }
    
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload
        )
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        
        result = response.json()
        logger.info(f"Gemini response: {result}")
        
        # Extract the text from the response
        if "candidates" in result and len(result["candidates"]) > 0:
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            return SimplifiedGeminiResponse(data=text.strip())  # Remove any leading/trailing whitespace
        else:
            raise ValueError("No valid response from Gemini API")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Gemini API: {e}")
        raise HTTPException(status_code=500, detail="Failed to call Gemini API")
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"Error parsing Gemini API response: {e}")
        raise HTTPException(status_code=500, detail="Invalid response from Gemini API")