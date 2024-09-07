from flask import Flask, request, jsonify, flash, render_template
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
    # return render_template('home.html')
    return 'Welcome, but I am not impressed...🛸'


@app.route('/users', methods=['GET'])
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user():
    user_name = request.form.get('user_name')

    if user_name:
        data_manager.add_user(user_name)
        flash('User added successfully! 🦕', 'success')
        return jsonify({'message': f"User '{user_name}' added successfully!"}), 201
    else:
        flash('User name is required! 🦖', 'error')
        return jsonify({'error': 'User name is required.'}), 400


@app.route('/add_movie', methods=['POST'])
def add_movie():
    movie_data = {
        'title': request.form.get('title'),
        'director': request.form.get('director'),
        'release_year': request.form.get('release_year'),
        'rating': request.form.get('movie_rating')
    }
    if movie_data['title'] and movie_data['director'] and movie_data['release_year'] and movie_data['rating']:
        data_manager.add_movie(movie_data)
        flash('Movie added successfully! 🎡', 'success')
        return jsonify({'message': f"Movie '{movie_data['title']}' added successfully!"}), 201
    else:
        flash('All fields are required! 🌋', 'error')
        return jsonify({'error': 'All fields are required.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
