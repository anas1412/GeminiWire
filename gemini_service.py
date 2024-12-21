import os
import time
import hashlib
import json
from gemini_request import execute
from function_utils import load_functions

# Function registry populated dynamically
function_registry = load_functions()

# In-memory cache (simple dictionary cache)
cache = {}

# Set expiration time to 15 minutes (in seconds)
CACHE_EXPIRATION_TIME = 900  # 15 minutes

# Path to the function definitions file
FUNCTIONS_FILE = "function_definitions.py"

# Track the last modified timestamp of the function definitions file
last_modified_time = os.path.getmtime(FUNCTIONS_FILE)

def generate_cache_key(function_name, inputs):
    # Convert the inputs to a sorted JSON string to ensure consistency
    inputs_str = json.dumps(inputs, sort_keys=True)
    return hashlib.md5((function_name + inputs_str).encode()).hexdigest()

def check_for_function_updates():
    global last_modified_time
    # Check if the function definitions file has been modified
    current_modified_time = os.path.getmtime(FUNCTIONS_FILE)
    if current_modified_time != last_modified_time:
        print("Function definitions file has been updated. Resetting cache.")
        last_modified_time = current_modified_time
        return True
    return False

def wire_function(function_name: str, inputs: dict):
    # Check if the function definitions have been modified and reset the cache
    if check_for_function_updates():
        # Reset the cache
        global cache
        cache = {}
    
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
    
    # Only cache the result if it's not None
    if result is not None:
        # Store the result with timestamp in the cache
        cache[cache_key] = {'result': result, 'timestamp': time.time()}
    
    return result
