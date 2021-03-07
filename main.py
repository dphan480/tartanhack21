from flask import Flask, render_template, request, escape

app = Flask(__name__)

@app.route('/home')
def about():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pantry')
def pantry():
    return render_template('pantry.html')

@app.route('/pantry/<int:food>')
def listPantryItems2(food):
    return food

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
