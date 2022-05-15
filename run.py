from turtle import title
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '975499ff23f5019775351a3cace85d3309ec313ed1ee70897a29e5bb0cd5d952'

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
    
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
   return render_template("about.html", title='About')

@app.route("/register", methods=['GET', 'POST'] )
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


# Custom Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('fourOwfour.html'),404

if __name__ == '__main__':
    app.run(debug=True)
    