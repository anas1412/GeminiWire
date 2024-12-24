import os
import hashlib
import json
import time
from function_utils import load_functions
from gemini_request import execute

# Function registry populated dynamically
function_registry = load_functions()

# In-memory cache (simple dictionary cache)
cache = {}

# Set expiration time to 15 minutes (in seconds)
CACHE_EXPIRATION_TIME = 900  # 15 minutes

# Track the last modified time of the function definitions file
FUNCTION_DEFINITIONS_FILE = "wire_definitions.json"
last_mod_time = os.path.getmtime(FUNCTION_DEFINITIONS_FILE)

def generate_cache_key(function_name, inputs):
    # Convert the inputs to a sorted JSON string to ensure consistency
    inputs_str = json.dumps(inputs, sort_keys=True)
    cache_key = hashlib.md5((function_name + inputs_str).encode()).hexdigest()
    print(f"Generated cache key: {cache_key}")
    return cache_key

def check_and_reset_cache():
    global last_mod_time
    current_mod_time = os.path.getmtime(FUNCTION_DEFINITIONS_FILE)

    # If the file has been modified, reset the cache
    if current_mod_time != last_mod_time:
        print(f"Function definitions file changed. Clearing cache...")
        cache.clear()  # Reset cache
        last_mod_time = current_mod_time  # Update last modified time

def wire_function(function_name: str, inputs: dict):
    # Check if the function definitions file has changed and reset cache if needed
    check_and_reset_cache()

    # Generate a cache key based on function_name and inputs
    cache_key = generate_cache_key(function_name, inputs)

    # Check if the result is already cached
    if cache_key in cache:
        cache_entry = cache[cache_key]
        # Check if the cached result has expired
        elapsed_time = time.time() - cache_entry['timestamp']

        # If the cache hasn't expired, return the cached result
        if elapsed_time < CACHE_EXPIRATION_TIME:
            print(f"Cache hit for function '{function_name}' with inputs {inputs}. Elapsed time: {elapsed_time:.2f}s")
            return cache_entry['result']  # Return cached result if it hasn't expired

        # If expired, log and remove it from cache
        print(f"Cache expired for function '{function_name}' with inputs {inputs}. Elapsed time: {elapsed_time:.2f}s")
        del cache[cache_key]

    print(f"Cache miss for function '{function_name}' with inputs {inputs}")

    # Execute the function via Gemini API (execute is expected to be defined elsewhere)
    result = execute(function_name, inputs)
    print(f"Function executed. Result: {result}")

    # If the result is not None, store it in the cache with a timestamp
    if result is not None:
        cache[cache_key] = {'result': result, 'timestamp': time.time()}
        print(f"Cache updated for function '{function_name}' with inputs {inputs}")
    else:
        # Handle the case where the result is None (e.g., function didn't return a value)
        print(f"No result returned for function '{function_name}' with inputs {inputs}")

    return result
