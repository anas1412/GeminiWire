import inspect
import function_definitions
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_functions():
    """
    Dynamically load all functions from the function_definitions module.
    :return: A dictionary of function names and their corresponding function objects.
    """
    functions = {name: obj for name, obj in inspect.getmembers(function_definitions) if inspect.isfunction(obj)}
    
    if not functions:
        logger.warning("No functions were loaded from function_definitions.py.")
    #else:
    #    logger.info(f"Loaded {len(functions)} functions from function_definitions.py.")
    
    return functions
