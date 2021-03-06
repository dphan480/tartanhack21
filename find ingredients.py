import urllib
import urllib.request
import createDatabase
from bs4 import BeautifulSoup

urlbase = "https://www.allrecipes.com/search/results/?search="

#Puts 2d list of possible recipes into csv file format
def recipesToCSV(recipes):
    createDatabase.turnListsToCSV(recipes)

#find possible recipes
def findRecipes(pantry):
    possible = []
    potential = searchRecipes(pantry)
    for recipe in potential:
        #create list of ingredients
        with urllib.request.urlopen(recipe) as url:
            text = str(url.read())
            location = text.find("recipeIngredient") #locate ingredients in html source
            start = text.find("[",location)
            end = text.find("]",location)
            ingredients = text[start:end] #isolate ingredients, split into list
            ingredients = ingredients.split("\\n") #The 'ingredients' on the right used to say "relevant"
            ingredients = ingredients[1:len(ingredients)-1]
            
            ingredients = cleanIngredients(ingredients)
    
        possible.append([recipe] + ingredients)
        # if pantrymatch(pantry, ingredients):
        #     possible += [link] + relevant
        
    return possible

#list of first 20 recipes found for each food item, gets rid of duplicates
def searchRecipes(pantry):
    recipes = []

    #loop through pantry and find recipes
    for food in pantry:
        search = urlbase + food

        #split into sections that begin with recipe url
        with urllib.request.urlopen(search) as url: 
            text = str(url.read())
            text = text.split('<a class="card__titleLink manual-link-behavior"\\n                            href=')
            text = text[1:] #irrelevant stuff before first link
            
            #find urls, add to list
            for item in text: 
                start = item.find('"')
                end = item.find('"',start+1)
                recipes += [item[start+1:end]]

    #get rid of duplicates
    uniquerecipes = []
    for i in recipes: 
        if i not in uniquerecipes: 
            uniquerecipes.append(i) 

    return uniquerecipes

#compare ingredients to pantry
def pantrymatch(pantry, ingredients):
    pass

def cleanIngredients(ingredients):
    # chars = {
    # '\xc2\x82' : ',',        # High code comma
    # '\xc2\x84' : ',,',       # High code double comma
    # '\xc2\x85' : '...',      # Tripple dot
    # '\xc2\x88' : '^',        # High carat
    # '\xc2\x91' : '\x27',     # Forward single quote
    # '\xc2\x92' : '\x27',     # Reverse single quote
    # '\xc2\x93' : '\x22',     # Forward double quote
    # '\xc2\x94' : '\x22',     # Reverse double quote
    # '\xc2\x95' : ' ',
    # '\xc2\x96' : '-',        # High hyphen
    # '\xc2\x97' : '--',       # Double hyphen
    # '\xc2\x99' : ' ',
    # '\xc2\xa0' : ' ',
    # '\xc2\xa6' : '|',        # Split vertical bar
    # '\xc2\xab' : '<<',       # Double less than
    # '\xc2\xbb' : '>>',       # Double greater than
    # '\xc2\xbc' : '1/4',      # one quarter
    # '\xc2\xbd' : '1/2',      # one half
    # '\xc2\xbe' : '3/4',      # three quarters
    # '\xca\xbf' : '\x27',     # c-single quote
    # '\xcc\xa8' : '',         # modifier - under curve
    # '\xcc\xb1' : ''          # modifier - under line
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].replace(",","")
        ingredients[i] = ingredients[i].replace('"',"")
        ingredients[i] = ingredients[i].strip()
    return ingredients

def testFindRecipes():
    pantry = ["banana","apple",'walnut','butter','milk']
    recipes = findRecipes(pantry)
    recipesToCSV(recipes)

def test():
    contents = readFile("RecipeList.csv")
    "www,a,bac\nhhh,sada"
    line = "URL,ingredient,ingredient"
    pass

def readFile(path):
    with open(path,'rt') as f:
        return f.read()