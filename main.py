from gemini_service import wire_function
from crud_service import add_wire, update_wire, delete_wire, list_wires

if __name__ == "__main__":

        
    add_wire("multiply", ['num1', 'num2'], "Multiply {num1} by {num2} and only return the result.")

    result = wire_function("multiply", {"num1": 5, "num2": 10}).data
    print(f"Result: {result}")

    update_wire("multiply", ['num1', 'num2'], "Add {num1} to {num2} and return only the result.")

    result = wire_function("multiply", {"num1": 5, "num2": 10}).data
    print(f"Updated Result: {result}")


    print("\nDeleting 'multiply' function...")
    delete_wire("multiply")


    print("\nAvailable functions after deleting 'multiply':", list_wires())
    
    add_wire("test", [], "Return a very short test statement.")
    result = wire_function("test", {}).data
    print(f"Result: {result}")

    update_wire("test", [], "Return a very short test statement with a random name.")
    result2 = wire_function("test", {}).data
    print(f"Result: {result2}")
