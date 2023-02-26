import os
import openai
import requests
from bs4 import BeautifulSoup
import json

def load_data(message):
    dinings = ["worcester", "franklin", "hampshire", "berkshire"]
    for hall in dinings: 
      if hall in message.lower(): 
        dining = hall
      else:
        dining = "worcester"

    with open(f'./data/{dining}.json', 'r') as f:
        data = json.load(f)
    return data

def classify_intent(query):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print("intent classification query = ", query)
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Give a single word class from the following list: ['filter', 'nofilter', 'poem', 'chitchat']. Do not answer the query itself. Don't add punctuation to the answer. If query is vague choose 'other' as answer. Example - query: What are some healthy recipes with eggs, answer: filter | query: I'm allergic to soy. What recipes would you suggest?, answer: filter | query: I want something that has chicken, answer: filter | query: Can you suggest me a combination of recipes suitable for lunch, answer: nofilter | query: What do I eat for dinner? I want to have something light, answer: filter | query: Write a poem on tofu, answer: poem | query: What music do you like?, answer: chitchat. | query: What do you think of the movie Avatar?, answer: chitchat | query: What are some low calorie dishes?, answer: filter | query: {query}, answer: ",
    temperature=0.5,
    max_tokens=500,
    top_p=1.0,
    frequency_penalty=0.8,
    presence_penalty=0.0
    )

    return response["choices"][0]["text"].strip()

def get_data(dining):
    worcester_url = f'https://umassdining.com/locations-menus/{dining}/menu'
    html_text = requests.get(worcester_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    myLists = soup.find_all("li", {"class": "lightbox-nutrition"})
    recipe_list = []
    for l in myLists:
        recipe = {}
        a = l.find("a")
        recipe['ingredients'] = a['data-ingredient-list']
        recipe['recipe_name'] = a.text
        recipe['healthfulness'] = a['data-healthfulness']
        recipe['carbon'] = a['data-carbon-list']
        recipe['allergens'] = a['data-allergens']
        recipe['calories'] = a['data-calories']
        recipe_list.append(recipe)

    # save the data in a json file
    with open(f'./data/{dining}.json', 'w') as f:
        json.dump(recipe_list, f)

def get_recipe_names(recipes):
    recipe_names = []
    for recipe in recipes:
        recipe_names.append(recipe["recipe_name"])
    return recipe_names

def filter_recipes(recipes, query):
    # get coditions from query
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
    model="text-davinci-003",
    # TODO: add negative example for ingredients
    prompt="""Keys and possible values = 'calories': range(1, 100, 1), 'healthfulness': range(10, 50, 10), 'carbon': ['A', 'B', 'C', 'D', 'E'], 'ingredients': [str], 'allergens': [str]. Examples: query - egg dishes with low calories. answer - calorie/40, ingredients/egg | query - I'm allergic to soy. answer - calorie/40, allergens/soy | query: {}, answer:""".format(query),
    temperature=0.5,
    max_tokens=500,
    top_p=1.0,
    frequency_penalty=0.8,
    presence_penalty=0.0
    )

    calories = 100 
    allergens = []
    healthfulness = 0
    carbon = 'A'
    ingredients = []
    tokens = response["choices"][0]["text"].strip().split(",")
    print("tokens = ", tokens)
    for token in tokens:
        key, value = token.split("/")
        if key == "calories":
            calories = value
        elif key == "healthfulness":
            healthfulness = value
        elif key == "carbon":
            carbon = value
        elif key == "ingredients":
            ingredients.append(value)
        elif key == "allergens":
            allergens.append(value)

    # TODO: ability to select different dining halls
    final_recipes = []
    for recipe in recipes:
        if int(recipe['calories']) <= int(calories) and int(recipe['healthfulness']) >= int(healthfulness) and recipe['carbon'] >= carbon:
            if len(allergens) != 0 or len(ingredients) != 0:
                for allergen in allergens:
                    if allergen not in recipe['allergens']:
                        if len(ingredients) != 0:
                            for ingredient in ingredients:
                                if ingredient in recipe['ingredients']:
                                    final_recipes.append(recipe)
            else:
                final_recipes.append(recipe)
    
    return final_recipes 

def generate_response(query, recipes):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"{recipes}\n {query}. Generate friendly response as a part of a conversation. Maximum recipes = 5.",
    temperature=0.5,
    max_tokens=500,
    top_p=1.0,
    frequency_penalty=0.8,
    presence_penalty=0.0
    )

    print("generated response = ", response["choices"][0]["text"].strip())
    return response["choices"][0]["text"].strip()

def generate_chitchat_response(query):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"You are Audrey, chatbot assistant for UMass dining. You are a female black girl aged 10. Respond to the conversation: {query}",
    temperature=0.5,
    max_tokens=500,
    top_p=1.0,
    frequency_penalty=0.8,
    presence_penalty=0.0
    )

    print("generated response = ", response["choices"][0]["text"].strip())
    return response["choices"][0]["text"].strip()