# GeminiWire

## **Overview**

**GeminiWire** is a framework where users can define, store, and securely execute custom prompts as functions. It integrates AI (specifically Google Gemini) to process the functions, and users can chain multiple functions together to create automated workflows. Think of it as a dynamic system for creating and managing personalized logic powered by AI and fasAPI.

## **Flow of Execution**

### **Step 1: Function Selection**

When a function is called through API or from main.py , **GeminiWire**:

1.  Checks if the function exists in function_definitions.py.
2.  If available, forwards the request to the Gemini API.

### **Step 2: Prompt Preparation**

If the request is sent to the Gemini API:

- A dynamically generated prompt is crafted based on the function's logic.

### **Step 3: API Interaction**

The crafted prompt is sent to the Gemini API, and the response is processed:

- If successful, the content is extracted and returned.
- If unsuccessful, the error details are encapsulated in a GeminiResponse.

### **Step 4: Response Delivery**

The result is standardized into a GeminiResponse object, ensuring consistent output for both local and API-based executions.

## **How to Use GeminiWire**

### **1\. Setting Up**

1.  Clone the repository.
2.  Execute `pip install -r requirements.txt`
3.  Copy the `.env.example` rename it to `.env`and put your `GEMINI_API_KEY=your_gemini_api_key`

### **2\. Running the Service**

1.  Run `uvicorn server:app --reload`
2.  Access the API documentation at http://127.0.0.1:8000/docs.

### **3\. Defining a New Function inside function_definitions.py**

```python
def generate_character(inputs: dict):
    name = inputs.get('name')
    gender = inputs.get('gender')
    age = inputs.get('age')
    return f"Generate a brief anime character description based on {name}, {gender}, {age}."
```

### **4\. Executing Requests**

#### Via FastAPI Endpoint:

Use http://localhost:8000/docs to execute the JSON payload or use any REST API client to send the request.

Send a POST request to /execute with the following JSON payload:

```json
{
  "function_name": "generate_character",
  "inputs": {
    "name": "Alice",
    "gender": "female",
    "age": "22"
  }
}
```

#### Expected Response Example:

```json
{
  "function_name": "generate_character",
  "outputs": "Alice, 22, possesses a captivating blend of ethereal beauty and quiet strength. Her long, silver hair often frames a delicate face with striking emerald eyes, hinting at a hidden depth.  While appearing initially soft-spoken and reserved, a determined set to her jaw and a flash of steel in her gaze betray a resilient spirit ready to face any challenge.  She favors flowing, pastel-colored clothing, yet carries herself with an air of subtle elegance that belies a surprising agility.\n"
}
```

## **Testing the System**

### **Testing Locally**

Run the main.py file to execute and chain multiple operations:

`python main.py`

Add your function inside main.py

```python
character1 = wire_function("generate_character", {"name": "Alice", "gender": "female", "age": 22}).data
print("Character result:", character1)

```

Example Output:

```
Character result: Alice, 22, possesses striking, sapphire-blue eyes that hold a hint of mischievousness behind their usually calm demeanor. Her shoulder-length, silver hair is often braided, framing a delicate face with a slightly pointed chin.  Clad in practical yet stylish clothing – often incorporating shades of blue and white – she carries herself with a quiet grace, belying a surprisingly sharp wit and hidden strength.
```

## **Adding New Functions (examples)**

### **Generating anime world short story with a given plot and characters**

1.  Adding the function to function_definitions.py

```python
def generate_world(inputs: dict):
    plot = inputs.get('plot')
    characters = ", ".join(map(str, inputs.get('characters', [])))
    return f"Generate an anime world short story with {plot} and {characters}."
```

2. Executing the request in main.py:

```python

```

3. Expected Output:

```

```

### **Generating an SQL query that fetches users with a specific skill from a MySQL database**

1.  Adding the function to function_definitions.py

```python
def fetch_users_with_skill(inputs: dict):
    skill = inputs.get('skill')
    return f"Generate an SQL query to fetch users who have the '{skill}' skill from mysql DB. Only send the sql query in plain text dont use commas."
```

2. Executing the request in main.py:

```python
SQLquery = wire_function("fetch_users_with_skill", {"skill": "Cooking"}).data
print("SQL query:", SQLquery)
```

3. Expected Output

```bash
SQL query: SELECT * FROM users WHERE skills LIKE '%Cooking%'
```

## **Error Handling**

1.  If a function is missing:

    - Error Message: Function '' not found in function_definitions.py.

2.  If the Gemini API fails:

    - Error Message: Error : .

3.  Validation errors for request inputs:

    - Error Message: "Invalid input format: ".

## **Future Enhancements**

- [x] Implement caching for frequently used functions.
- [ ] Extend function_definitions.py with more advanced NLP tasks
- [ ] Add a noSQL database to register function_definitions and their inputs for each user.
- [ ] Add a user authentication system to secure function calls.
- [ ] Add a user interface for easy function management and execution.
- [ ] Add detailed logging for debugging API and local function calls.
- [ ] Support batch processing of multiple tasks in a single request.
