from flask import render_template, url_for, flash, redirect
from blogpost import app, db, bcrypt
from blogpost.forms import RegistrationForm, LoginForm
from blogpost.models import User, Post



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
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        
        
        flash('Your account has been created you can now Login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'wayne@qq.com' and form.password.data == '12345':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid Credentials!', 'danger')
    return render_template('login.html', title='Login', form=form)


# Custom Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('fourOwfour.html'),404