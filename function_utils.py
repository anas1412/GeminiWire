import json
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FUNCTIONS_FILE = "wire_definitions.json"

def load_functions():
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        function_registry = {}

        # Add each function to the registry by dynamically accessing the function from the imported module
        for function_name, function_details in data.items():
            # Dynamically get function by name from the module
            function_registry[function_name] = function_details

        logger.info(f"Loaded {len(function_registry)} functions into the registry.")
        return function_registry
    except Exception as e:
        logger.error(f"Error loading functions: {e}")
        return {}

