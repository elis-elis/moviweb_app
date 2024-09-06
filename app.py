from flask import Flask
from flask_cors import CORS
from config import Config
from data_models import db, User, Movie, user_movies
from datamanager.sqlite_data_manager import SQLiteDataManager
import requests

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

# initialize an instance of SQLiteDataManager with the Flask app
data_manager = SQLiteDataManager(app)


# with app.app_context():
#    db.create_all()


@app.route('/')
def home():
    return "Welcome, but I am not impressed..."


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)


if __name__ == '__main__':
    app.run(debug=True)
