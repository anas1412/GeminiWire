from gemini_service import wire_function
from crud_service import add_wire, update_wire, delete_wire, list_wires, fetch_wires, fetch_wire

if __name__ == "__main__":
    # Add a new wire function
    add_wire(
        function_name="multiply",
        inputs={"num1": "The first number", "num2": "The second number"},
        description="Multiply two numbers.",
        prompt="Multiply {num1} by {num2} and only return the result."
    )

    # Execute the wire function
    result = wire_function("multiply", {"num1": 5, "num2": 10}).data
    print(f"Result: {result}")

    # Fetch the wire function details
    multiply_details = fetch_wire("multiply")
    print("\nFetched 'multiply' function details:")
    print(multiply_details)

    # Update the wire function
    update_wire(
        function_name="multiply",
        inputs={"num1": "The first number", "num2": "The second number"},
        description="Add two numbers.",
        prompt="Add {num1} to {num2} and return only the result."
    )

    # Execute the updated wire function
    result = wire_function("multiply", {"num1": 5, "num2": 10}).data
    print(f"Updated Result: {result}")

    # Delete the wire function
    print("\nDeleting 'multiply' function...")
    delete_wire("multiply")

    # List available functions after deletion
    print("\nAvailable functions after deleting 'multiply':", list_wires())

