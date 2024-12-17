import inspect
import function_definitions

def load_functions():
    """
    Dynamically load all functions from the function_definitions module.
    :return: A dictionary of function names and their corresponding function objects.
    """
    return {name: obj for name, obj in inspect.getmembers(function_definitions) if inspect.isfunction(obj)}
