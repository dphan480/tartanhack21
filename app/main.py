import urllib
import urllib.request
from flask import Flask, request, render_template

urlbase = "https://www.allrecipes.com/search/results/?search="

def searchRecipes(food): #list of first 20 unique recipes found for each food
    recipes = []
    food = food.replace(" ", "+") #adjust string for url
    food = food.replace(",", "%2C")
    search = urlbase + food
    with urllib.request.urlopen(search) as url: #split into sections that begin with a recipe url
        text = str(url.read())
        text = text.split('<a class="card__titleLink manual-link-behavior"\\n                            href=')
        text = text[1:] #irrelevant stuff before first link
        for item in text: #isolate url and add to list
            start = item.find('"')
            end = item.find('"',start+1)
            recipes += [item[start+1:end]]
    uniquerecipes = []
    for i in recipes: #get rid of duplicates
        if i not in uniquerecipes:
            uniquerecipes.append(i)
    return uniquerecipes

def removeKeywords(ingredients): #isolate relevant ingredients
    keywords = ["cups", "tablespoons", "tbsps", "tsps", "teaspoons", "packages",
                "package", "cup", "tablespoon", "tbsp", "tsp",
                "teaspoon", "containers", "container", "cans", "can",'pounds',
                 'pound','pinch','pints','pint',"scoops",
                "scoop", "jars", "jar", "ounces",'ounce', "oz",
                "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    for i in range(len(ingredients)):
        for j in range(len(keywords)):
            indexKeyword = ingredients[i].find(keywords[j])
            if(indexKeyword != -1):
                indexKeyword = indexKeyword + len(keywords[j])
                ingredients[i] = ingredients[i][indexKeyword+1:]
                break
    return ingredients

def cleanIngredients(ingredients): #cleanup string
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].replace(",","")
        ingredients[i] = ingredients[i].replace('"',"")
        ingredients[i] = ingredients[i].strip()
    ingredients = removeKeywords(ingredients)
    return ingredients

def pantryMatch(pantry, ingredients): #checks to see if required ingredients are in pantry
    for ingredient in ingredients:
        if not ([food for food in pantry if food in ingredient]):
            return False
    return True

def findRecipes(food): #searches website for possible recipes given an item
    possible = []
    potential = searchRecipes(food)
    for recipe in potential: #for each recipe url locate ingredients in html source
        with urllib.request.urlopen(recipe) as url:
            text = str(url.read())
            location = text.find("recipeIngredient")
            start = text.find("[",location)
            end = text.find("]",location)
            ingredients = text[start:end] #isolate ingredients, split into list
            ingredients = ingredients.split("\\n")
            ingredients = ingredients[1:len(ingredients)-1] #get rid of extra stuff
            ingredients = cleanIngredients(ingredients)
            if pantryMatch(pantry,ingredients):
                possible.append([recipe] + ingredients)
    return possible

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    global pantry
    if request.method == 'GET':
        pantry = []
    if request.method == 'POST':
        recipes = []
        form_data = request.form.to_dict()
        for key,value in form_data.items():
            items = value.split(",")
            items = cleanIngredients(items)
            if key != "Item":
                if str(key) in pantry:
                    pantry.remove(str(key))
            else:
                for item in items:
                    if item not in pantry:
                        pantry += items
    return render_template("homepage.html", pantry=pantry)

@app.route('/search/', methods = ['GET', 'POST'])
def search():
    if request.method == 'GET':
        return "No"
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
