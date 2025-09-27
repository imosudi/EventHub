from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy

# Import models and forms
#from .models import db, Event, Registration

# Create Flask application instance
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise database with app
# Initialise SQLAlchemy
db = SQLAlchemy()

db.init_app(app)

from .routes import *