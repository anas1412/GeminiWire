def translate(inputs: dict):
    text = inputs.get('text')
    language = inputs.get('language')
    return f'Translate the following text: {text} to {language}.'
def numberReader(inputs: dict):
    num = inputs.get('num')
    lang = inputs.get('lang')
    return f'Translate {num} to {lang} in letters and only'
def summarize(inputs: dict):
    text = inputs.get('text')
    version = inputs.get('version')
    return f'Summarize the following text: {text} and add GPT as JSON {version} at the end.'
def fetch_users_with_skill(inputs: dict):
    skill = inputs.get('skill')
    return f'Generate an SQL query to fetch users who have the {skill} skill from mysql DB. Only send the sql query in plain text dont use commas.'
def translate_amount(inputs: dict):
    amount = inputs.get('amount')
    return f'Translate the amount {amount} into words.'
def novel_summary(inputs: dict):
    novel = inputs.get('novel')
    return f'Make a detailed summary of {novel}'
def novel_theory(inputs: dict):
    novel = inputs.get('novel')
    return f'Give me relevant theoretical approaches about this novel {novel}'
def reverse_string(inputs: dict):
    msg = inputs.get('msg')
    return f'Reverse this string: {msg}'
def weird_test_message(inputs: dict):
    vibe = inputs.get('vibe')
    name = inputs.get('name')
    someone = inputs.get('someone')
    return f'Generate a test message in {vibe} vibe from {name} to {someone}'
def generate_character(inputs: dict):
    name = inputs.get('name')
    gender = inputs.get('gender')
    age = inputs.get('age')
    description = inputs.get('description')
    return f'Generate a description based on {name}, {gender}, {age} and a {description}.'
def test(inputs: dict):
    name = inputs.get('name')
    return f'Return a very short creative test messgae from {name} to test connectivity'
def fetch_customers_by_product(inputs: dict):
    product = inputs.get('product')
    date = inputs.get('date')
    return f'Generate me an sql query that fetchs a list of customers that bought a {product} in a specific date: {date} only send me the sql query'
