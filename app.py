from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from config import Config
from data_models import db, User, Movie
import requests


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)

# with app.app_context():
#    db.create_all()
