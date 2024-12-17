import os
import inspect
import function_definitions
from gemini_request import execute

# Dynamically populate the function registry from function_definitions.py
def load_function_registry():
    function_registry = {}
    for name, obj in inspect.getmembers(function_definitions):
        if inspect.isfunction(obj):
            function_registry[name] = obj
    
    # Print the function names in a clean, user-friendly way
    print("Loaded functions:")
    for function_name in function_registry.keys():
        print(f"- {function_name}")
    print("\nRequesting from API...\n")
    return function_registry

# Function registry populated dynamically
function_registry = load_function_registry()

def execute_function(function_name: str, inputs: dict):
    """
    This function dynamically fetches and executes the appropriate function from the registry
    or sends a request to Gemini API if the function is not available.
    """
    # First, check if the function is in the local registry (from function_definitions)
    function_to_execute = function_registry.get(function_name)
    
    if function_to_execute:
        return function_to_execute(inputs)
    
    # If the function isn't in the local registry, call Gemini API
    return execute(function_name, inputs)
