from gemini_service import execute

if __name__ == "__main__":
    #result = execute("add", {"num1": 150, "num2": 30}).data
    #print("Addition result:", result)
    
    #translation = execute("numberReader", {"num": result, "lang": "Japanese"}).data
    #print("Translation result:", translation)

    #amount500 = execute("translate_amount", {"amount": 500}).data
    #print("Amount result:", amount500)

    #character1 = execute("generate_character", {"name": "Anas", "gender": "Male", "age": 27}).data
    #print("Character result:", character1)

    #character2 = execute("generate_character", {"name": "Mei", "gender": "Female", "age": 22}).data
    #print("Character result:", character2)

    #character3 = execute("generate_character", {"name": "Achref", "gender": "Male", "age": 21}).data
    #print("Character result:", character3)

    #charactersList = [character1, character2, character3]

    #world = execute("generate_world", {"plot":"Fighting a dragon", "characters": charactersList}).data
    #print("World result:", world)

    character1 = execute("generate_character", {"name": "Alice", "gender": "female", "age": 22}).data
    print("Character result:", character1)

    character2 = execute("generate_character", {"name": "Anas", "gender": "Male", "age": 27}).data
    print("Character result:", character2)

    charactersList = [character1, character2]

    plot = "Coding GeminiWire, a framework where users can define, store, and securely execute custom functions. It integrates AI (like Google Gemini) to process the functions, and users can chain multiple functions together to create automated workflows. Think of it as a dynamic system for creating and managing personalized logic powered by AI and fasAPI."

    world = execute("generate_world", {"plot": plot, "characters": charactersList}).data
    print("World result:", world)

    SQLquery = execute("fetch_users_with_skill", {"skill": "Cooking"}).data
    print("SQL query:", SQLquery)
