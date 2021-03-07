from flask import Flask, render_template, request, escape

app = Flask(__name__)

@app.route('/')
def hello():
    return ''''<form action="" method="get">
                    <input type="text" name="name">
                    <input type="submit" value="Convert">
                    </form>'''

@app.route('/<name>')
def hello_name(name):
    return f"Hello {name}!"

# @app.route('/')
# def home():
#     celsius = str(escape(request.args.get("celsius", "")))
#     return (
#         """<form action="" method="get">
#                 <input type="text" name="celsius">
#                 <input type="submit" value="Convert">
#             </form>""" + celsius
#     )
#     # return render_template("pantry.html")

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/pantry')
# def pantry():
#     return render_template('pantry.html')

# @app.route("/<int:celsius>")
# def fahrenheit_from(celsius):
#     """Convert Celsius to Fahrenheit degrees."""
#     fahrenheit = float(celsius) * 9 / 5 + 32
#     fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
#     return str(fahrenheit)

# @app.route('/<int:food>')
# def listPantryItems(food):
#     return food

# @app.route('/pantry/<int:food>')
# def listPantryItems2(food):
#     return food

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
