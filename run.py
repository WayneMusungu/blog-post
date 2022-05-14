from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)


app.config['SECRET_KEY'] = "this is no secret"

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