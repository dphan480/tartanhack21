import urllib
import urllib.request
from bs4 import BeautifulSoup
from flask import Flask, redirect, request, url_for, render_template

urlbase = "https://www.allrecipes.com/search/results/?search="

def findRecipes(food): #searches website for possible recipes given an item
    possible = []
    potential = searchRecipes(food)
    for recipe in potential: #checks potential recipes to see which are possible
        with urllib.request.urlopen(recipe) as url:
            text = str(url.read())
            location = text.find("recipeIngredient") #locate ingredients in html source
            start = text.find("[",location)
            end = text.find("]",location)
            ingredients = text[start:end] #isolate ingredients, split into list
            ingredients = ingredients.split("\\n")
            ingredients = ingredients[1:len(ingredients)-1]
            ingredients = cleanIngredients(ingredients)
            if pantryMatch(pantry,ingredients):
                possible.append([recipe] + ingredients)
    return possible

def searchRecipes(food): #list of first 20 unique recipes found for each food
    recipes = []
    # for food in pantry:
    food = food.replace(" ", "+")
    food = food.replace(",", "%2C")
    search = urlbase + food
    with urllib.request.urlopen(search) as url: #split into sections that begin with recipe url
        text = str(url.read())
        text = text.split('<a class="card__titleLink manual-link-behavior"\\n                            href=')
        text = text[1:] #irrelevant stuff before first link
        for item in text: 
            start = item.find('"')
            end = item.find('"',start+1)
            recipes += [item[start+1:end]]
    uniquerecipes = []
    for i in recipes: 
        if i not in uniquerecipes: 
            uniquerecipes.append(i) 
    return uniquerecipes

def cleanIngredients(ingredients): #clean up strings
    chars = {
    '\xc2\x82' : ',',        # High code comma
    '\xc2\x84' : ',,',       # High code double comma
    '\xc2\x85' : '...',      # Tripple dot
    '\xc2\x88' : '^',        # High carat
    '\xc2\x91' : '\x27',     # Forward single quote
    '\xc2\x92' : '\x27',     # Reverse single quote
    '\xc2\x93' : '\x22',     # Forward double quote
    '\xc2\x94' : '\x22',     # Reverse double quote
    '\xc2\x95' : ' ',
    '\xc2\x96' : '-',        # High hyphen
    '\xc2\x97' : '--',       # Double hyphen
    '\xc2\x99' : ' ',
    '\xc2\xa0' : ' ',
    '\xc2\xa6' : '|',        # Split vertical bar
    '\xc2\xab' : '<<',       # Double less than
    '\xc2\xbb' : '>>',       # Double greater than
    '\xc2\xbc' : '1/4',      # one quarter
    '\xc2\xbd' : '1/2',      # one half
    '\xc2\xbe' : '3/4',      # three quarters
    '\xca\xbf' : '\x27',     # c-single quote
    '\xcc\xa8' : '',         # modifier - under curve
    '\xcc\xb1' : ''          # modifier - under line
    }
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].replace(",","")
        ingredients[i] = ingredients[i].replace('"',"")
        ingredients[i] = ingredients[i].strip()
    return ingredients

def pantryMatch(pantry, ingredients):
    for ingredient in ingredients:
        if not ([food for food in pantry if food in ingredient]):
            return False
    return True

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    global pantry
    if request.method == 'GET':
        pantry = []
    if request.method == 'POST':
        form_data = request.form.to_dict()
        for key,value in form_data.items():
            items = value.split(",")
            items = [item.strip() for item in items]
            if key == "Item":
                for item in items:
                    if item not in pantry:
                        pantry += items
            if key == "RemoveItem":
                for item in items:
                    if item in pantry:
                        pantry.remove(item)
    return render_template("homepage.html",
                            pantry=pantry)

@app.route('/search/', methods = ['POST', 'GET'])
def search():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        recipes = []
        form_data = request.form.to_dict()
        for key,value in form_data.items():
            items = value.split(",")
            items = [item.strip() for item in items]
            for item in items:
                recipes += findRecipes(item)
        return render_template("search.html",recipes = recipes)

if __name__ == "__main__":
    app.run()
