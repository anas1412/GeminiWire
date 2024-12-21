from gemini_service import wire_function

if __name__ == "__main__":
    # Test data
    function_name = "fetch_users_with_skill"
    inputs = {"skill": "Cooking"}

    # First call, should be a cache miss and make the API call
    SQLquery1 = wire_function(function_name, inputs)
    print("First query:", SQLquery1.data)

    # Second call with the same inputs, should be a cache hit
    SQLquery2 = wire_function(function_name, inputs)
    print("Second query (cached):", SQLquery2.data)

    # Third call with different inputs, should be a cache miss
    inputs2 = {"skill": "Python"}
    SQLquery3 = wire_function(function_name, inputs2)
    print("Third query:", SQLquery3.data)