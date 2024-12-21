def summarize(inputs: dict):
    text = inputs.get('text')
    version = inputs.get('version')
    return f"Summarize the following text: {text} and add GPT as JSON {version} at the end."

def translate(inputs: dict):
    text = inputs.get('text')
    language = inputs.get('language')
    return f"Translate the following text: '{text}' to {language}."


def numberReader(inputs: dict):
    num = inputs.get('num')
    lang = inputs.get('lang')
    return f"Translate {num} to {lang} in letters and only return the result."

def reverse_string(inputs: dict):
    text = inputs.get("text")
    return f"Reverse this string: {text}"

def translate_amount(inputs: dict):
    amount = inputs.get('amount')
    return f"Translate the amount {amount} into words."

def generate_character(inputs: dict):
    name = inputs.get('name')
    gender = inputs.get('gender')
    age = inputs.get('age')
    return f"Generate a brief anime character description based on {name}, {gender}, {age}."

def generate_world(inputs: dict):
    plot = inputs.get('plot')
    characters = ", ".join(map(str, inputs.get('characters', [])))
    return f"Generate an anime world short story with {plot} and {characters}."

def fetch_users_with_skill(inputs: dict):
    skill = inputs.get('skill')
    return f"Generate an SQL query to fetch users who have the '{skill}' skill from mysql DB. Only send the sql query in plain text dont use commas."

