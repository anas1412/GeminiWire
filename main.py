from gemini_service import wire_function
from crud_service import add_function, update_function, delete_function, list_functions

if __name__ == "__main__":
    print("\nAdding 'multiply' function...")
    add_function("multiply", ['num1', 'num2'], "Multiply {num1} by {num2} and only return the result.")
    # Test the 'multiply' function
    print("\nTesting 'multiply' function with inputs {'num1': 5, 'num2': 10}...")
    result = wire_function("multiply", {"num1": 5, "num2": 10}).data
    print(f"Result: {result}")
    result = wire_function("multiply", {"num1": 5, "num2": 10}).data
    print(f"Result: {result}")

    # List available functions after adding 'multiply'
    print("\nAvailable functions after adding 'multiply':", list_functions())

    # Update the 'multiply' function
    print("\nUpdating 'multiply' function to return a string with more details...")
    update_function("multiply", ['num1', 'num2'], "Add {num1} to {num2} and return only the result.")

    # Test the updated 'multiply' function
    print("\nTesting updated 'multiply' function with inputs {'num1': 5, 'num2': 10}...")
    result = wire_function("multiply", {"num1": 5, "num2": 10}).data
    print(f"Updated Result: {result}")

    # Delete the 'multiply' function
    print("\nDeleting 'multiply' function...")
    delete_function("multiply")

    # List available functions after deleting 'multiply'
    print("\nAvailable functions after deleting 'multiply':", list_functions())
