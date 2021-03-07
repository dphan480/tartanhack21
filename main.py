from flask import Flask, render_template, request, escape


app = Flask(__name__)
# <!-- The core Firebase JS SDK is always required and must be listed first -->
# <script src="/__/firebase/8.2.10/firebase-app.js"></script>

# <!-- TODO: Add SDKs for Firebase products that you want to use
#      https://firebase.google.com/docs/web/setup#available-libraries -->

# <!-- Initialize Firebase -->
# <script src="/__/firebase/init.js"></script>

@app.route('/home')
def home():
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
