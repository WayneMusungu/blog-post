from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
# def index():
    # return"<h1>Hello World!</h1>"
    

def index():
    return render_template("index.html")

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# Custom Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('fourOwfour.html'),404
    