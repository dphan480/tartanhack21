import urllib
import urllib.request
import createDatabase
from bs4 import BeautifulSoup
import time

urlbase = "https://www.allrecipes.com/search/results/?search="

#Puts 2d list of possible recipes into csv file format
def recipesToCSV(recipes):
    createDatabase.turnListsToCSV(recipes)

#find possible recipes
def findRecipes(pantry,timex=time.time()):
    possible = []
    potential = searchRecipes(pantry)
    print(f'All URLs found: {time.time()-timex}')
    for recipe in potential:
        #create list of ingredients
        startTime = time.time()
        with urllib.request.urlopen(recipe) as url:
            text = str(url.read())
            location = text.find("recipeIngredient") #locate ingredients in html source
            start = text.find("[",location)
            end = text.find("]",location)
            ingredients = text[start:end] #isolate ingredients, split into list
            ingredients = ingredients.split("\\n") #The 'ingredients' on the right used to say "relevant"
            ingredients = ingredients[1:len(ingredients)-1]
            
            #startTime = time.time()
            ingredients = cleanIngredients(ingredients)
            elapseTime = time.time() - startTime
            print(f'Ingredient Analysis took {elapseTime}')
    
        possible.append([recipe] + ingredients)
        # if pantrymatch(pantry, ingredients):
        #     possible += [link] + relevant
    print(f'Everything completed in {time.time()-timex}')    
    return possible

#list of first 20 recipes found for each food item, gets rid of duplicates
def searchRecipes(pantry):
    recipes = []

    #loop through pantry and find recipes
    for food in pantry:
        food = food.replace(" ", "+")
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

def removeKeywords(ingredients):
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


def cleanIngredients(ingredients):
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].replace(",","")
        ingredients[i] = ingredients[i].replace('"',"")
        ingredients[i] = ingredients[i].strip()
    ingredients = removeKeywords(ingredients)
    return ingredients

def testFindRecipes():
    print('beginning testing...')
    pantry = ["banana","apple",'walnut','butter','milk','butter','granola',
                'onion','chicken','beef','soup','carrot','cheese','sugar',
                'broccoli','soy sauce','bread','pasta','egg','oyster sauce',
                'pork','turkey','chocolate','fish','vanilla','potato','olive oil']
    recipes = findRecipes(pantry)
    print('recipes Found! Turning to CSV')
    recipesToCSV(recipes)
    print('Passed')

def test():
    contents = readFile("RecipeList.csv")
    "www,a,bac\nhhh,sada"
    line = "URL,ingredient,ingredient"
    pass

def readFile(path):
    with open(path,'rt') as f:
        return f.read()