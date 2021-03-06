
import RecipeList

# Search through Recipe List CSV file

def FindRecipes(Ingredients):
    # Ingredients should be lowercase core words
    # like "egg", "milk", "chicken", "flour"
    Recipes = readFile("RecipeList.csv")
    for line in RecipeList
    return

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, 'wt') as f:
        f.write(contents)