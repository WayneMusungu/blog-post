from turtle import title
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime


app = Flask(__name__)




app.config['SECRET_KEY'] = '975499ff23f5019775351a3cace85d3309ec313ed1ee70897a29e5bb0cd5d952'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='user_comments', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comments', backref='topicpost', lazy=True)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Post('{self.content}', '{self.date_posted}')"

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
        
        flash('Your account has been created you can now Login!', 'success')
        return redirect(url_for('home'))
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

if __name__ == '__main__':
    app.run(debug=True)
    