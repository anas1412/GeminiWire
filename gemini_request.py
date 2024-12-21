import os
import requests
from dotenv import load_dotenv
import wire_definitions
import inspect
from models import GeminiRequest, GeminiResponse
from function_utils import load_functions

# Load environment variables from the .env file
load_dotenv()

# Get the Gemini API key from the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")

if not GEMINI_API_KEY or not GEMINI_API_URL:
    raise EnvironmentError("GEMINI_API_KEY and GEMINI_API_URL must be set in the environment variables.")

def execute(function_name: str, inputs: dict) -> GeminiResponse:
    try:
        # Step 1: Validate and construct the GeminiRequest
        request = GeminiRequest(function_name=function_name, inputs=inputs)

        # Step 2: Fetch function dynamically (centralized)
        function_registry = load_functions()
        function_to_execute = function_registry.get(request.function_name)

        if not function_to_execute:
            raise ValueError(f"Function '{request.function_name}' not found in wire_definitions.py")

        # Step 3: Generate the prompt using the function
        prompt = function_to_execute(request.inputs)

        # Step 4: Prepare and send API payload
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, json=data)

        # Step 5: Process the response
        return process_gemini_response(response, function_name)
        
    except Exception as e:
        return GeminiResponse(function_name=function_name, status="error", data=None, message=str(e))

def process_gemini_response(response, function_name):
    if response.status_code == 200:
        response_json = response.json()
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            output_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return GeminiResponse(function_name=function_name, status="success", data=output_text, message=None)
        return GeminiResponse(function_name=function_name, status="error", data=None, message="No candidates found.")
    else:
        return GeminiResponse(function_name=function_name, status="error", data=None, message=f"Error {response.status_code}: {response.text}")


def get_function_from_registry(function_name: str):
    # Get all functions from wire_definitions dynamically
    functions = load_functions()

    # Return the function if it exists
    return functions.get(function_name, None)
