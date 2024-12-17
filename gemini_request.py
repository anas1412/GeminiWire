import os
import requests
from dotenv import load_dotenv
import function_definitions
import inspect
from models import GeminiRequest, GeminiResponse

# Load environment variables from the .env file
load_dotenv()

# Get the Gemini API key from the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API URL
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

def execute(function_name: str, inputs: dict) -> GeminiResponse:
    """
    Executes a request to the Gemini API for a specified function.
    :param function_name: Name of the function to execute (e.g., 'summarize').
    :param inputs: The input parameters required by the function (e.g., text, language).
    :return: A standardized GeminiResponse object.
    """
    try:
        # Step 1: Validate and construct the GeminiRequest
        request = GeminiRequest(function_name=function_name, inputs=inputs)

        # Step 2: Fetch the function dynamically from function_definitions.py
        function_to_execute = get_function_from_registry(request.function_name)
        if not function_to_execute:
            raise ValueError(f"Function '{request.function_name}' not found in function_definitions.py")

        # Step 3: Generate the prompt using the function
        prompt = function_to_execute(request.inputs)

        # Step 4: Prepare the API payload
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        # Step 5: Construct the request URL with the API key
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"

        # Step 6: Send the POST request to the Gemini API
        response = requests.post(url, json=data)

        if response.status_code == 200:
            # Parse the response JSON
            response_json = response.json()

            # Extract the first candidate's content
            if "candidates" in response_json and len(response_json["candidates"]) > 0:
                output_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
                return GeminiResponse(
                    function_name=function_name,
                    status="success",
                    data=output_text,
                    message=None
                )
            else:
                # No candidates found in the response
                return GeminiResponse(
                    function_name=function_name,
                    status="error",
                    data=None,
                    message="No candidates found in the response."
                )
        else:
            # API returned an error
            return GeminiResponse(
                function_name=function_name,
                status="error",
                data=None,
                message=f"Error {response.status_code}: {response.text}"
            )
    except Exception as e:
        # Handle unexpected errors
        return GeminiResponse(
            function_name=function_name,
            status="error",
            data=None,
            message=str(e)
        )


def get_function_from_registry(function_name: str):
    """
    Dynamically fetch the function from the function_definitions module.
    :param function_name: The name of the function to retrieve.
    :return: The function object, or None if not found.
    """
    # Get all functions from function_definitions dynamically
    functions = {name: obj for name, obj in inspect.getmembers(function_definitions) if inspect.isfunction(obj)}

    # Return the function if it exists
    return functions.get(function_name, None)
