from turtle import title
from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        
        'author': 'Wayne Musungu',
        'title': 'Blog Post 1',
        'content': 'Initial post',
        'date_posted': 'May 15, 2021'
    },
     {
        
        'author': 'James White',
        'title': 'Blog Post 2',
        'content': 'Second post',
        'date_posted': 'June 15, 2021'
    },
]




@app.route('/')
# def index():
    # return"<h1>Hello World!</h1>"
    
@app.route('/home')
def home():
    return render_template("home.html", posts=posts)

@app.route('/about')
def about():
   return render_template("about.html", title='About')

# Custom Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('fourOwfour.html'),404

if __name__ == '__main__':
    app.run(debug=True)
    