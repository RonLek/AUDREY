import requests
from bs4 import BeautifulSoup


worcester_url = 'https://umassdining.com/locations-menus/worcester/menu'
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
	recipe_list.append(recipe['recipe_name'])

print(recipe_list)
