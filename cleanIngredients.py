def removeKeywords(ingredients):
    keywords = ["cups", "tablespoons", "tbsps", "tsps", "teaspoons", "packages", 
                "package", "cup", "tablespoon", "tbsp", "tsp", 
                "teaspoon", "containers", "container", "cans", "can", "scoops", 
                "scoop", "jars", "jar", "ounces", "oz" 
                "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    for i in range(len(ingredients)):
        for j in range(len(keywords)):
            indexKeyword = ingredients[i].find(keywords[j])
            if(indexKeyword != -1):    
                ingredients[i] = ingredients[i][indexKeyword+2:]
                break
    return ingredients

        

