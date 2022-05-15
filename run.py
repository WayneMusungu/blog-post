from email.policy import default
from enum import unique
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Creating a Flask Instance
app = Flask(__name__)

#Adding a database
# oLd SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#Secret Key
app.config['SECRET_KEY'] = "this is no secret"
#Database Initialization
db = SQLAlchemy(app)







#Model Creation
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email =db.Column(db.String(150),unique=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Name %r>' % self.name
    

#Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
#Dtabase Update Record

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
        except:
            db.session.commit()
            flash("Error looks like there was a problem. Kindly try again")
            return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
        
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
    
            
    
       

#Form Class
class NameForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user= Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        
       
      
        
        flash("User has been added successfully 👍")
        
    our_users = Users.query.order_by(Users.date_added)
    
    return render_template("add_user.html", form=form, name=name, our_users=our_users)
    


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