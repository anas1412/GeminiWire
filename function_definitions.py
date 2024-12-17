def summarize(inputs: dict):
    """
    Summarizes the provided text and adds the version at the end.
    """
    text = inputs.get('text')
    version = inputs.get('version')
    return f"Summarize the following text: {text} and add GPT as JSON {version} at the end."

def translate(inputs: dict):
    """
    Translates the provided text to the target language.
    """
    text = inputs.get('text')
    language = inputs.get('language')
    return f"Translate the following text: '{text}' to {language}."

def add(inputs: dict):
    """
    Add the first provided number to the next provided number and return it as a number.
    """
    num1 = inputs.get('num1')
    num2 = inputs.get('num2')
    return f"Add {num1} to {num2} and return it as a number."

def numberReader(inputs: dict):
    """
    Translate the provided number to the target language in letters and only return the result.
    """
    num = inputs.get('num')
    lang = inputs.get('lang')
    return f"Translate {num} to {lang} in letters and only return the result."

def reverse_string(inputs: dict):
    """
    Reverses the provided string.
    """
    text = inputs.get("text")
    return f"Reverse this string: {text}"

# Function to translate the expense amount to words
def translate_amount(inputs: dict):
    """
    Converts an amount into words (e.g., 150 -> 'one hundred fifty').
    """
    amount = inputs.get('amount')
    # This function assumes that the number is passed as an integer
    return f"Translate the amount {amount} into words."

def generate_character(inputs: dict):
    """
    Generate a brief anime character description based on provided name, gender and age.
    """
    name = inputs.get('name')
    gender = inputs.get('gender')
    age = inputs.get('age')
    return f"Generate a brief anime character description based on {name}, {gender}, {age}."

def generate_world(inputs: dict):
    """
    Generate an anime world short story with the provided plot and characters.
    """
    plot = inputs.get('plot')
    characters = ", ".join(map(str, inputs.get('characters', [])))
    return f"Generate an anime world short story with {plot} and {characters}."

def fetch_users_with_skill(inputs: dict):
    """
    Generate an SQL query to fetch users who have a specific skill from mysql DB. Only send the sql query in plain text dont use commas.
    """
    skill = inputs.get('skill')
    return f"Generate an SQL query to fetch users who have the '{skill}' skill from mysql DB. Only send the sql query in plain text dont use commas."
