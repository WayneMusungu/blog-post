from email.policy import default
from enum import unique
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Creating a Flask Instance
app = Flask(__name__)

#Adding a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Secret Key
app.config['SECRET_KEY'] = "this is no secret"
#Database Initialization
db = SQLAlchemy(app)

#Model Creation
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    email =db.Column(db.String(150),unique=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Name %r>' % self.name

#Form Class
class NameForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


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
    
    
# Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    #Form Validation
    
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        
        flash("Your Form has been Submitted Successfully")
    
    
    return render_template("name.html", name= name, form = form)