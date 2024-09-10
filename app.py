import os
from flask import Flask, request, flash, render_template, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
import requests
from config.logging_config import setup_logging
from config.config import Config
from data_models import db
from datamanager.sqlite_data_manager import SQLiteDataManager


load_dotenv()
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

# initialize an instance of SQLiteDataManager with the Flask app
data_manager = SQLiteDataManager(app)

# Set up logging
setup_logging(app)

# to initialize or create the database schema - run 'python initialize_db.py' from the terminal or command line


def fetch_movie_details_from_omdb(title):
    """
    Fetch movie details from the OMDb API.
    """
    try:
        # Construct the API URL
        api_url = f'http://www.omdbapi.com/?apikey={API_KEY}&t={title}'

        # Send the request to OMDb API
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()  # Raises an HTTPError if the response status is 4xx, 5xx

        data = response.json()
        if data.get('Response') == 'True':  # Successful response from OMDb
            return {
                'title': data.get('Title'),
                'director': data.get('Director'),
                'release_year': data.get('Year'),
                'rating': data.get('imdbRating')
            }
        else:
            app.logger.error(f"OMDb API Error: {data.get('Error')}")
            return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error happened: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error happened: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error happened: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error happened: {req_err}")

    # Return None for any kind of failure uniformly
    return None


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users', methods=['GET'])
def list_users():
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)


@app.route('/movies', methods=['GET'])
def list_movies():
    movies = data_manager.get_all_movies()
    return render_template('movies.html', movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Handle POST request (form submission)
        user_name = request.form.get('user_name')

        # Validate and remove any leading or trailing whitespace characters
        if user_name and user_name.strip():
            success = data_manager.add_user(user_name)
            if success:
                flash('User added successfully! 🦕', 'success')

            else:
                flash('Failed to add user. Please try again later. 🦖', 'error')

            return redirect(url_for('add_user'))

        else:
            flash('User name is required and cannot be empty! 🧉', 'error')

    # Handle GET request (display form)
    return render_template('add_user.html')


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        # Get the title from the form
        title = request.form.get('title')

        # Fetch movie details from OMDb API
        movie_data = fetch_movie_details_from_omdb(title)

        if not movie_data:
            # Use the initial input title when the API fails to fetch movie data
            flash(f"Could not fetch details for the movie '{title}' from OMDb. 🦈", 'error')
            return redirect(url_for('add_movie'))

        try:
            # Add the movie to the database
            movie_id = data_manager.add_movie(movie_data)

            if movie_id:
                # Use the processed and accurate movie title from the API response
                flash(f"Movie '{movie_data['title']}' added successfully! 🎬", 'success')
            else:
                flash(f"Failed to add movie '{movie_data['title']}'.", 'error')

        except Exception as e:
            app.logger.error(f"Error adding movie: {e}")
            flash(f"An unexpected error occurred while adding the movie '{title}'.", 'error')

        return redirect(url_for('list_movies'))

    return render_template('add_movie.html', movie_data={})


@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    # Fetch user from the database, this is to ensure the user exists
    user = data_manager.get_user_by_id(user_id)

    # Fetch the user's favorite movies
    movies = data_manager.get_user_movies(user_id)

    if not user:
        flash(f'User with ID {user_id} is not found. 🍭', 'error')
        return redirect('/users')

    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/add_new_movie', methods=['GET', 'POST'])
def add_new_movie_to_user(user_id):
    # Fetch the user data
    user = data_manager.get_user_by_id(user_id)

    if not user:
        flash(f"User with ID {user_id} not found.", 'error')
        return redirect(url_for('list_users'))

    if request.method == 'POST':
        title = request.form.get('title')
        movie_data = fetch_movie_details_from_omdb(title)

        if not movie_data:
            flash(f"Could not fetch details for the movie '{title}' from OMDb. 🦈", 'error')
            return redirect(url_for('add_new_movie_to_user', user_id=user_id))

        # Add the movie to the database
        movie_id = data_manager.add_movie(movie_data)

        if movie_id:  # Check if movie was added successfully
            # Attempt to associate the new movie with the user
            success = data_manager.add_movie_to_user(user_id, movie_id)

            if success:
                flash(f"Movie '{movie_data['title']}' added to user {user.user_name} successfully! 🎡", 'success')
            else:
                flash(f"Movie '{movie_data['title']}' could not be added to user {user.user_name}. 🪂", 'error')

        else:
            flash(f"Could not add the movie '{movie_data['title']}' to the database. 🦈", 'error')

        return redirect(url_for('add_new_movie_to_user', user_id=user_id))

    return render_template('add_new_movie_to_user.html', movie_data={}, user=user, user_id=user_id)


@app.route('/users/<int:user_id>/add_user_movie', methods=['GET', 'POST'])
def add_existing_movie_to_user(user_id):
    user = data_manager.get_user_by_id(user_id)

    if not user:
        flash(f"User with ID {user_id} not found.", 'error')
        return redirect(url_for('list_users'))

    # Fetch all movies to display in the dropdown
    movies = data_manager.get_all_movies()

    if request.method == 'POST':
        # Get movie_id from the form
        movie_id = request.form.get('movie_id')

        if movie_id:
            success = data_manager.add_movie_to_user(user_id, movie_id)
            if success:
                flash(f"Movie added to user {user.user_name} successfully! 🌤️", 'success')
            else:
                flash(f"Could not add movie to user {user.user_name}. 🦇", 'error')
        else:
            flash("Please select a movie to add. 🦄", 'error')

        return redirect(url_for('add_existing_movie_to_user', user_id=user_id))

    # Render a form to allow the user to select a movie
    return render_template('add_existing_movie_to_user.html', user=user, movies=movies)


@app.route('/movies/<int:movie_id>/edit', methods=['GET', 'POST'])
def update_movie(movie_id):
    movie = data_manager.get_movie_by_id(movie_id)

    if not movie:
        flash('Movie not found. 🪓', 'error')
        return redirect(url_for('list_movies'))

    if request.method == 'POST':
        # Get updated data from the form
        updated_data = {
            'title': request.form.get('title', movie.title),
            'director': request.form.get('director', movie.director),
            'release_year': request.form.get('release_year', movie.release_year),
            'rating': request.form.get('movie_rating', movie.movie_rating)
        }

        # Update the movie in the database
        success = data_manager.update_movie(movie_id, updated_data)
        if success:
            flash(f"Movie '{updated_data['title']}' updated successfully! 👑", 'success')
        else:
            flash(f"Failed to update movie '{updated_data['title']}' 🥁", 'error')
        return redirect(url_for('list_movies'))

    return render_template('update_movie.html', movie=movie)


@app.route('/movies/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    success = data_manager.delete_movie(movie_id)
    if success:
        flash(f"Movie with ID {movie_id} has been deleted successfully! 🪐", 'success')
    else:
        flash(f"Movie with ID {movie_id} could not be deleted. ☔", 'error')

    # Redirect to the list of movies after deletion
    return redirect(url_for('list_movies'))


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def remove_movie_from_user(user_id, movie_id):
    success = data_manager.remove_movie_from_user(user_id, movie_id)
    if success:
        flash(f"Movie with ID {movie_id} has been deleted from user {user_id} successfully! 🦐", 'success')
    else:
        flash(f"Could not delete movie from user {user_id}. 🐌", 'error')

    # Stay on the user's movie list page, where the action was triggered
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/delete_user', methods=['POST'])
def delete_user(user_id):
    success = data_manager.delete_user(user_id)
    if success:
        flash(f"User with ID {user_id} has been deleted successfully! 🦩", 'success')
    else:
        flash(f"User with ID {user_id} could not be deleted. 🦤", 'error')

    # Redirect to the list of users after deletion
    return redirect(url_for('list_users'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
