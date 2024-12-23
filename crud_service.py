import re
from function_utils import load_functions
from models import WireFunctionRequest

import json

FUNCTIONS_FILE = "wire_definitions.json"

def add_wire(function_name: str, inputs: dict, description: str, prompt: str):
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        if function_name in data:
            raise ValueError(f"Function '{function_name}' already exists.")

        data[function_name] = {
            "prompt": prompt,  # Use 'prompt' here
            "description": description,  # Use 'description' here
            "inputs": inputs
        }

        with open(FUNCTIONS_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Function '{function_name}' added successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def update_wire(function_name: str, inputs: dict, description: str, prompt: str):
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        if function_name not in data:
            raise ValueError(f"Function '{function_name}' not found.")

        # Get the existing function data
        existing_data = data[function_name]

        # Update only the description and prompt while preserving the other fields (inputs)
        updated_data = {
            "prompt": prompt if prompt else existing_data["prompt"],  # Update prompt if new prompt is provided
            "description": description,  # Update description
            "inputs": inputs if inputs else existing_data["inputs"]  # Only update inputs if they are provided
        }

        # Update the function data
        data[function_name] = updated_data

        # Write the updated data back to the file
        with open(FUNCTIONS_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Function '{function_name}' updated successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def delete_wire(function_name: str):
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
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def list_wires():
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        return list(data.keys())
    except Exception as e:
        print(f"An unexpected error occurred while listing functions: {e}")
        return []

def fetch_wires():
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        return data
    except Exception as e:
        print(f"An unexpected error occurred while listing functions: {e}")
        return {}


def fetch_wire(function_name: str):
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            data = json.load(f)

        if function_name not in data:
            raise ValueError(f"Function '{function_name}' not found.")

        return data[function_name]
    except ValueError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None