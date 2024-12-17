import os
import inspect
import function_definitions
from gemini_request import execute
from function_utils import load_functions
import hashlib
import json
import time

# Function registry populated dynamically
function_registry = load_functions()

# In-memory cache (simple dictionary cache)
cache = {}

# Set expiration time to 15 minutes (in seconds)
CACHE_EXPIRATION_TIME = 900  # 15 minutes

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
    Cache expiration is checked before returning cached results.
    """
    # Generate a cache key based on function_name and inputs
    cache_key = generate_cache_key(function_name, inputs)
    
    # Check if the result is already cached
    if cache_key in cache:
        cache_entry = cache[cache_key]
        # Check if the cached result has expired
        if time.time() - cache_entry['timestamp'] < CACHE_EXPIRATION_TIME:
            print(f"Cache hit for function '{function_name}' with inputs {inputs}")
            return cache_entry['result']  # Return cached result if it hasn't expired

        # If expired, remove it from cache
        print(f"Cache expired for function '{function_name}' with inputs {inputs}")
        del cache[cache_key]

    print(f"Cache miss for function '{function_name}' with inputs {inputs}")
    
    # Execute via Gemini API
    result = execute(function_name, inputs)
    
    # Store the result with timestamp in the cache
    cache[cache_key] = {'result': result, 'timestamp': time.time()}
    return result
