import json
from function_utils import load_functions
from models import WireFunctionRequest

FUNCTIONS_FILE = "wire_definitions.json"

def add_wire(function_name: str, inputs: Optional[dict], description: str, prompt: Optional[str]):
    """Add a new wire function to the definitions."""
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        if function_name in data:
            raise ValueError(f"Function '{function_name}' already exists.")

        data[function_name] = {
            "prompt": prompt,
            "description": description,
            "inputs": inputs if inputs else {}
        }

        with open(FUNCTIONS_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Function '{function_name}' added successfully.")
    except ValueError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def update_wire(function_name: str, inputs: Optional[dict], description: Optional[str], prompt: Optional[str]):
    """Update an existing wire function in the definitions."""
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        if function_name not in data:
            raise ValueError(f"Function '{function_name}' not found.")

        existing_data = data[function_name]
        updated_data = {
            "prompt": prompt if prompt is not None else existing_data["prompt"],
            "description": description if description is not None else existing_data["description"],
            "inputs": inputs if inputs is not None else existing_data["inputs"]
        }

        data[function_name] = updated_data

        with open(FUNCTIONS_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Function '{function_name}' updated successfully.")
    except ValueError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def delete_wire(function_name: str):
    """Delete a wire function from the definitions."""
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        if function_name not in data:
            raise ValueError(f"Function '{function_name}' not found.")

        del data[function_name]

        with open(FUNCTIONS_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Function '{function_name}' deleted successfully.")
    except ValueError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def list_wires():
    """List all wire function names."""
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        return list(data.keys())
    except Exception as e:
        print(f"An unexpected error occurred while listing functions: {e}")
        raise

def fetch_wires():
    """Fetch details of all wire functions."""
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        return data
    except Exception as e:
        print(f"An unexpected error occurred while listing functions: {e}")
        raise

def fetch_wire(function_name: str):
    """Fetch details of a specific wire function."""
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        if function_name not in data:
            raise ValueError(f"Function '{function_name}' not found.")

        return data[function_name]
    except ValueError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
