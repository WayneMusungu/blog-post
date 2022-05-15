# from turtle import title
from flask import Flask
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)




app.config['SECRET_KEY'] = '975499ff23f5019775351a3cace85d3309ec313ed1ee70897a29e5bb0cd5d952'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from blogpost import routes
