from gemini_service import wire_function
from crud_service import add_function, update_function, delete_function, list_functions

if __name__ == "__main__":

    print("Available functions before adding 'multiply':", list_functions())

    # Add function with code
    new_function_code = """    
    num1 = inputs.get('num1')
    num2 = inputs.get('num2')
    return f'The result of multiplying {num1} by {num2}'
    """
    add_function("multiply", new_function_code)

    print("Available functions after adding 'multiply':", list_functions())

    number = wire_function("multiply", {"num1": 25, "num2": 4}).data
    print("Multiply Output:", number)

    # Update function with new code
    updated_function_code = """    
    num1 = inputs.get('num1')
    num2 = inputs.get('num2')
    return f'The result of multiplying {num1} by {num2}. Only send the result'
    """
    update_function("multiply", updated_function_code)

    print("Available functions after update:", list_functions())

    # Test the updated multiply function
    updated_number = wire_function("multiply", {"num1": 25, "num2": 4}).data
    print("Updated Multiply Output:", updated_number)