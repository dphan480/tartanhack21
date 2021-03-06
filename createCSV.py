# Copy and paste this into find ingredients

# Given a 2d list of lists, turns it into a csv file
def turnListsToCSV(Lists):
    for singleList in Lists:
        addListToCSV(singleList)
    pass

# Adds the list to CSV file
def addListToCSV(recipe):
    content = ""
    for i in range(len(recipe)):
        content += recipe[i].replace(",","")
        if i != (len(recipe) - 1):
            content += ","
    writeFile("RecipeList.csv",content+"\n")

# Clears CSV File
def clearCSVFile():
    with open("RecipeList.csv","wt") as f:
        f.write("")
    print('File Cleared!')

# appends content into a file at path. 
def writeFile(path, contents):
    with open(path, 'a') as f: # "a" is for append "wt" is overwrite
        f.write(contents)