import importlib.util
import logging
import os
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FUNCTIONS_FILE = "function_definitions.py"

def load_functions():
    try:
        # Import the functions file dynamically
        spec = importlib.util.spec_from_file_location("function_definitions", FUNCTIONS_FILE)
        function_definitions_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(function_definitions_module)

        function_registry = {}
        
        # Find all function definitions in the file using regex
        with open(FUNCTIONS_FILE, "r") as f:
            content = f.read()
        function_names = re.findall(r"def (\w+)\(inputs: dict\):", content)

        # Add each function to the registry by dynamically accessing the function from the imported module
        for function_name in function_names:
            # Dynamically get function by name from the module
            func = getattr(function_definitions_module, function_name, None)
            if func:
                function_registry[function_name] = func
            else:
                logger.warning(f"Function '{function_name}' could not be found in {FUNCTIONS_FILE}.")
        
        logger.info(f"Loaded {len(function_names)} functions into the registry.")
        return function_registry
    except Exception as e:
        logger.error(f"Error loading functions: {e}")
        return {}

