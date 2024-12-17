import os
import inspect
import function_definitions
from gemini_request import execute
from function_utils import load_functions
import hashlib
import json

# Function registry populated dynamically
function_registry = load_functions()

# In-memory cache (simple dictionary cache)
cache = {}

def generate_cache_key(function_name, inputs):
    """
    Generate a consistent hash key for caching based on function_name and inputs.
    """
    # Convert the inputs to a sorted JSON string to ensure consistency
    inputs_str = json.dumps(inputs, sort_keys=True)
    return hashlib.md5((function_name + inputs_str).encode()).hexdigest()

def execute_function(function_name: str, inputs: dict):
    """
    This function sends a request to the Gemini API for the specified function.
    Caching is implemented to avoid redundant API calls.
    """
    # Generate a cache key based on function_name and inputs
    cache_key = generate_cache_key(function_name, inputs)
    
    # Check if the result is already cached
    if cache_key in cache:
        print(f"Cache hit for function '{function_name}' with inputs {inputs}")
        return cache[cache_key]  # Return cached result

    print(f"Cache miss for function '{function_name}' with inputs {inputs}")
    
    # Execute via Gemini API
    result = execute(function_name, inputs)
    
    # Cache the result from the API call
    cache[cache_key] = result
    return result
