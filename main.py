from gemini_service import execute_function

if __name__ == "__main__":
    # Test data
    function_name = "fetch_users_with_skill"
    inputs = {"skill": "Cooking"}

    # First call, should be a cache miss and make the API call
    SQLquery1 = execute_function(function_name, inputs)
    print("First query:", SQLquery1.data)

    # Second call with the same inputs, should be a cache hit
    SQLquery2 = execute_function(function_name, inputs)
    print("Second query (cached):", SQLquery2.data)

    # Third call with different inputs, should be a cache miss
    inputs2 = {"skill": "Python"}
    SQLquery3 = execute_function(function_name, inputs2)
    print("Third query:", SQLquery3.data)