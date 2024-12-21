import re

FUNCTIONS_FILE = "function_definitions.py"

def add_function(name: str, code: str):
    try:
        # Check if the function already exists
        with open(FUNCTIONS_FILE, "r") as f:
            content = f.read()
        if re.search(rf"def {name}\(inputs: dict\):", content):
            raise ValueError(f"Function '{name}' already exists.")

        # Add the new function
        with open(FUNCTIONS_FILE, "a") as f:
            f.write(f"\n\ndef {name}(inputs: dict):\n{code}\n")
        print(f"Function '{name}' added successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

import re

FUNCTIONS_FILE = "function_definitions.py"

def update_function(name: str, code: str):
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            content = f.read()

        # Regex to find the function definition and its entire body
        pattern = rf"def {name}\(inputs: dict\):\n(    .*\n)*"

        # Check if the function exists
        if not re.search(pattern, content):
            raise ValueError(f"Function '{name}' not found.")

        # Remove the old function entirely
        updated_content = re.sub(pattern, "", content)

        # Add the new function
        updated_content += f"\ndef {name}(inputs: dict):\n{code}\n"

        # Write the updated content back to the file
        with open(FUNCTIONS_FILE, "w") as f:
            f.write(updated_content)

        print(f"Function '{name}' updated successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def delete_function(name: str):
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            content = f.read()

        # Regex to find the function definition and its entire body
        pattern = rf"def {name}\(inputs: dict\):\n(    .+\n)*"

        if not re.search(pattern, content):
            raise ValueError(f"Function '{name}' not found.")

        # Remove the function entirely
        updated_content = re.sub(pattern, "", content)

        with open(FUNCTIONS_FILE, "w") as f:
            f.write(updated_content)
        print(f"Function '{name}' deleted successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def list_functions():
    try:
        with open(FUNCTIONS_FILE, "r") as f:
            content = f.read()

        return re.findall(r"def (\w+)\(inputs: dict\):", content)
    except Exception as e:
        print(f"An unexpected error occurred while listing functions: {e}")
