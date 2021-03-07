import urllib
import urllib.request
import scrape
from bs4 import BeautifulSoup
from flask import Flask, redirect, request, url_for, render_template

urlbase = "https://www.allrecipes.com/search/results/?search="

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
            for item in items:
                if key == "Item":
                    if item not in pantry:
                        pantry += items
                if key == "RemoveItem":
                    if item in pantry:
                        pantry.remove(item)
    return render_template("homepage.html",
                            pantry=pantry)

@app.route('/search/', methods = ['POST', 'GET'])
def search():
    if request.method == 'GET':
        return f"No"
    if request.method == 'POST':
        recipes = []
        form_data = request.form.to_dict()
        for key,value in form_data.items():
            items = value.split(",")
            items = [item.strip() for item in items]
            for item in items:
                recipes += scrape.findRecipes(item)
        return render_template("search.html",recipes = recipes)

if __name__ == "__main__":
    app.run(host='localhost',debug=True)

