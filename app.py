from flask import Flask, request, jsonify, flash
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


@app.route('/users', methods=['GET'])
def list_users():
    users = data_manager.get_all_users()
    user_list = []
    for user in users:
        user_dict = {'id': user.user_id, 'name': user.user_name}
        user_list.append(user_dict)

    flash('🚀Here are all the users: ')
    return jsonify(user_list)


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


if __name__ == '__main__':
    app.run(debug=True)
