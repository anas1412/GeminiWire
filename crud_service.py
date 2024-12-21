import re
from function_utils import load_functions

FUNCTIONS_FILE = "wire_definitions.py"

def add_wire(function_name: str, inputs: list, description: str):
    try:
        # Check if the function already exists
        with open(FUNCTIONS_FILE, "r") as f:
            content = f.read()
        if re.search(rf"def {function_name}\(inputs: dict\):", content):
            raise ValueError(f"Function '{function_name}' already exists.")

        # Generate the function signature and inputs handling code
        input_lines = ""
        if inputs:  # Only add input lines if inputs are provided
            for param in inputs:
                input_lines += f"    {param} = inputs.get('{param}')\n"

        # Generate function code, with or without input lines
        function_code = f"def {function_name}(inputs: dict):\n{input_lines}    return f'{description}'\n"

        # Add the new function to the file
        with open(FUNCTIONS_FILE, "a") as f:
            f.write(function_code)

        # Reload the functions registry after adding the new function
        global function_registry  # Ensure to modify the global function registry
        function_registry = load_functions()

        print(f"Function '{function_name}' added successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def update_wire(function_name: str, inputs: list, description: str):
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            content = f.read()

        # Regex to find the function definition and its entire body
        pattern = rf"def {function_name}\(inputs: dict\):\n(    .*\n)*"

        # Check if the function exists
        if not re.search(pattern, content):
            raise ValueError(f"Function '{function_name}' not found.")

        # Remove the old function entirely (matching the function pattern)
        updated_content = re.sub(pattern, "", content)

        # Generate the new function code
        input_lines = ""
        if inputs:  # Only add input lines if inputs are provided
            for param in inputs:
                input_lines += f"    {param} = inputs.get('{param}')\n"

        # Format the new function code without extra blank lines
        function_code = f"def {function_name}(inputs: dict):\n{input_lines}    return f'{description}'\n"

        # Add the new function code (replace the old one)
        updated_content += function_code

        # Write the updated content back to the file
        with open(FUNCTIONS_FILE, "w") as f:
            f.write(updated_content)

        # Reload the functions registry after updating the function
        global function_registry
        function_registry = load_functions()

        print(f"Function '{function_name}' updated successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def delete_wire(function_name: str):
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            content = f.read()

        # Regex to find the function definition and its entire body
        pattern = rf"def {function_name}\(inputs: dict\):\n(    .*\n)*"

        # Check if the function exists
        if not re.search(pattern, content):
            raise ValueError(f"Function '{function_name}' not found.")

        # Remove the function entirely (match and remove the function)
        updated_content = re.sub(pattern, "", content)

        # Write the updated content back to the file
        with open(FUNCTIONS_FILE, "w") as f:
            f.write(updated_content)

        # Reload the functions registry after deleting the function
        global function_registry
        function_registry = load_functions()

        print(f"Function '{function_name}' deleted successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def list_wires():
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            content = f.read()

        # Find all function names by looking for the function signature
        function_names = re.findall(r"def (\w+)\(inputs: dict\):", content)
        return function_names
    except Exception as e:
        print(f"An unexpected error occurred while listing functions: {e}")
        return []
