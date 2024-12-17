from gemini_service import execute_function

if __name__ == "__main__":
    #result = execute("add", {"num1": 150, "num2": 30}).data
    #print("Addition result:", result)
    
    #character1 = execute("generate_character", {"name": "Alice", "gender": "female", "age": 22}).data
    #print("Character result:", character1)

    #character2 = execute("generate_character", {"name": "Anas", "gender": "Male", "age": 27}).data
    #print("Character result:", character2)

    #charactersList = [character1, character2]

    #plot = "Coding GeminiWire, a framework where users can define, store, and securely execute custom functions. It integrates AI (like Google Gemini) to process the functions, and users can chain multiple functions together to create automated workflows. Think of it as a dynamic system for creating and managing personalized logic powered by AI and fasAPI."

    #world = execute("generate_world", {"plot": plot, "characters": charactersList}).data
    #print("World result:", world)

    #SQLquery = execute("fetch_users_with_skill", {"skill": "Cooking"}).data
    #print("SQL query:", SQLquery)
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