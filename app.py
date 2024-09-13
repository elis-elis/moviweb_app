import os
from flask import Flask, request, flash, render_template, redirect, url_for
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

# initialize an instance of SQLiteDataManager with the Flask app
data_manager = SQLiteDataManager(app)

# Set up logging
setup_logging(app)


def fetch_movie_details_from_omdb(title):
    """
    Fetch movie details from the OMDb API using the provided title.
    Returns:
        dict: A dictionary containing movie details (title, director, release_year, rating)
        if successful.
        None: If the API request fails or the movie is not found.
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
    """
    Render the home page.
    """
    return render_template('home.html')


@app.route('/users', methods=['GET'])
def list_users():
    """
    Display the list of all users.
    Returns:
        Response: The rendered users page template.
        Redirect: Redirects to the home page if an error occurs.
    """
    try:
        users = data_manager.list_all_users()
        return render_template('users.html', users=users)

    except Exception as e:
        app.logger.error(f"Error fetching users from the database: {e}")
        flash('An error occurred while fetching users. Please try again later. 🛀',
              'error')
        return redirect(url_for('home'))


@app.route('/movies', methods=['GET'])
def list_movies():
    """
    Display the list of all movies.
    Returns:
        Response: The rendered movies page template.
        Redirect: Redirects to the home page if an error occurs.
    """
    try:
        movies = data_manager.get_all_movies()
        return render_template('movies.html', movies=movies)

    except Exception as e:
        app.logger.error(f"Error fetching movies from the database: {e}")
        flash('An error occurred while fetching movies. Please try again later. 🫀',
              'error')
        return redirect(url_for('home'))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Add a new user to the database.
    Methods:
        GET: Render the user addition form.
        POST: Process the form submission and add the user.
    Returns:
        Response: The rendered add user page template or
        a redirect to the same page after submission.
    """
    if request.method == 'POST':
        user_name = request.form.get('user_name')

        # Strip whitespace and validate user input
        if user_name and user_name.strip():
            success = data_manager.add_user(user_name.strip())
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
    """
    Add a new movie to the database.
    Methods:
        GET: Render the movie addition form.
        POST: Process the form submission, fetch details from OMDb, and add the movie.
    Returns:
        Response: The rendered add movie page template or
        a redirect to the movie list page after submission.
    """
    if request.method == 'POST':
        # Get the title from the form
        title = request.form.get('title')

        # Validate and remove any leading or trailing whitespace characters
        if title and title.strip():
            # Fetch movie details from OMDb API
            movie_data = fetch_movie_details_from_omdb(title.strip())

            if not movie_data:
                # Use the initial input title when the API fails to fetch movie data
                flash(f"Could not fetch details for the movie '{title}' from OMDb. 🦈",
                      'error')
                return redirect(url_for('add_movie'))

            try:
                # Add the movie to the database
                movie_id = data_manager.add_movie(movie_data)

                if movie_id:
                    # Use the processed and accurate movie title from the API response
                    flash(f"Movie '{movie_data['title']}' added successfully! 🎬",
                          'success')
                else:
                    flash(f"Failed to add movie '{movie_data['title']}'. 🪗", 'error')

            except Exception as e:
                app.logger.error(f"Error adding movie: {e}")
                flash(f"An unexpected error occurred while adding the movie '{title}'. 💣",
                      'error')

        else:
            flash("Movie title cannot be empty or whitespace. Please enter a valid title. 🧯",
                  'error')

        return redirect(url_for('list_movies'))

    return render_template('add_movie.html', movie_data={})


@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    """
    Display the movies associated with a specific user.
    Args:
        user_id (int): The ID of the user.
    Returns:
        Response: The rendered user movies page template or
        a redirect to the users page if the user is not found.
    """
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
    """
    Add a new movie to a specific user by fetching movie details from OMDb.
    Args:
        user_id (int): The ID of the user.
    Methods:
        GET: Render the form to add a new movie.
        POST: Process the form submission and add the movie to the user.
    Returns:
        Response: The rendered add new movie to user page template or
        a redirect to the same page after submission.
    """
    try:
        # Fetch the user data
        user = data_manager.get_user_by_id(user_id)

        if not user:
            flash(f"User with ID {user_id} not found. 💎", 'error')
            return redirect(url_for('list_users'))

        if request.method == 'POST':
            title = request.form.get('title')

            if title and title.strip():
                movie_data = fetch_movie_details_from_omdb(title.strip())

                if not movie_data:
                    flash(f"Could not fetch details for the movie '{title}' from OMDb. 🚰",
                          'error')
                    return redirect(url_for('add_new_movie_to_user', user_id=user_id))

                # Add the movie to the database
                movie_id = data_manager.add_movie(movie_data)

                if movie_id:  # Check if movie was added successfully
                    # Attempt to associate the new movie with the user
                    success = data_manager.add_movie_to_user(user_id, movie_id)

                    if success:
                        flash(f"Movie '{movie_data['title']}' added to user {user.user_name} "
                              f"successfully! 🎡", 'success')
                    else:
                        flash(f"Movie '{movie_data['title']}' could not be added to user "
                              f"{user.user_name}. 🪂", 'error')

                else:
                    flash(f"Could not add the movie '{movie_data['title']}' to the database. 🌵",
                          'error')

                return redirect(url_for('add_new_movie_to_user', user_id=user_id))

    except Exception as e:
        app.logger.error(f"An unexpected error occurred while adding a new movie to user {user_id}: {e}")
        flash(f"An unexpected error occurred. Please try again later. 🐉", 'error')
        return redirect(url_for('list_users'))

    return render_template('add_new_movie_to_user.html',
                           movie_data={}, user=user, user_id=user_id)


@app.route('/users/<int:user_id>/add_user_movie', methods=['GET', 'POST'])
def add_existing_movie_to_user(user_id):
    """
    Add an existing movie from the database to a specific user.
    Args:
        user_id (int): The ID of the user.
    Methods:
        GET: Render the form to select an existing movie.
        POST: Process the form submission and associate the selected movie with the user.
    Returns:
        Response: The rendered add existing movie to user page template
        or a redirect to the same page after submission.
    """
    try:
        user = data_manager.get_user_by_id(user_id)

        if not user:
            flash(f"User with ID {user_id} not found. 📺", 'error')
            return redirect(url_for('list_users'))

        # Fetch all movies to display in the dropdown
        movies = data_manager.get_all_movies()

        if request.method == 'POST':
            # Get movie_id from the form
            movie_id = request.form.get('movie_id')

            if movie_id:
                success = data_manager.add_movie_to_user(user_id, movie_id)
                if success:
                    flash(f"Movie added to user {user.user_name} successfully! 🌤️",
                          'success')
                else:
                    flash(f"Could not add movie to user {user.user_name}. 🦇",
                          'error')
            else:
                flash("Please select a movie to add. 🦄", 'error')

            return redirect(url_for('add_existing_movie_to_user', user_id=user_id))

    except Exception as e:
        app.logger.error(f"An error occurred while adding an existing movie to user {user_id}: {e}")
        flash("An unexpected error occurred. Please try again later. 👽", 'error')
        return redirect(url_for('list_users'))

    # Render a form to allow the user to select a movie
    return render_template('add_existing_movie_to_user.html',
                           user=user, movies=movies)


@app.route('/movies/<int:movie_id>/edit', methods=['GET', 'POST'])
def update_movie(movie_id):
    try:
        movie = data_manager.get_movie_by_id(movie_id)

        if not movie:
            flash('Movie not found. 🪓', 'error')
            return redirect(url_for('list_movies'))

        if request.method == 'POST':
            # Get updated data from the form
            updated_data = {
                'title': request.form.get('title', movie.title).strip(),
                'director': request.form.get('director', movie.director).strip(),
                'release_year': request.form.get('release_year', movie.release_year).strip(),
                'rating': request.form.get('movie_rating', movie.movie_rating).strip()
            }
            # Validate the stripped inputs to avoid updating with empty values
            if not updated_data['title']:
                flash("Movie title cannot be empty. 🥫", 'error')
                return render_template('update_movie.html', movie=movie)

            # Update the movie in the database
            success = data_manager.update_movie(movie_id, updated_data)
            if success:
                flash(f"Movie '{updated_data['title']}' updated successfully! 👑",
                      'success')
            else:
                flash(f"Failed to update movie '{updated_data['title']}' 🥁",
                      'error')

            return redirect(url_for('list_movies'))

    except Exception as e:
        app.logger.error(f"Error updating movie with ID {movie_id}: {e}")
        flash("An unexpected error occurred while updating the movie. "
              "Please try again later. 🥨", 'error')
        return redirect(url_for('list_movies'))

    return render_template('update_movie.html', movie=movie)


@app.route('/movies/<int:movie_id>/delete_movie', methods=['POST'])
def delete_movie(movie_id):
    """
    Delete a movie from the database.
    Args:
        movie_id (int): The ID of the movie to be deleted.
    Returns:
        Response: Redirects to the list of movies page after attempting to delete the movie.
                  Displays a success or error message based on the result of the deletion.
    """
    try:
        success = data_manager.delete_movie(movie_id)
        if success:
            flash(f"Movie with ID {movie_id} has been deleted successfully! 🪐",
                  'success')
        else:
            flash(f"Movie with ID {movie_id} could not be deleted. ☔", 'error')

    except Exception as e:
        app.logger.error(f"Error deleting movie with ID {movie_id}: {e}")
        flash('An error occurred while deleting the movie. Please try again later. 🌽',
              'error')

    # Redirect to the list of movies after deletion
    return redirect(url_for('list_movies'))


@app.route('/users/<int:user_id>/remove_movie/<int:movie_id>', methods=['POST'])
def remove_movie_from_user(user_id, movie_id):
    """
    Remove a movie from a specific user's collection.
    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie to be removed.
    Returns:
        Response: Redirect to the user's movie list page with a flash message indicating
        success or failure.
    """
    try:
        success = data_manager.remove_movie_from_user(user_id, movie_id)
        if success:
            flash(f"Movie with ID {movie_id} has been deleted from user {user_id} "
                  f"successfully! 🦐", 'success')
        else:
            flash(f"Could not delete movie from user {user_id}. 🐌", 'error')

    except Exception as e:
        app.logger.error(f"Error removing movie with ID {movie_id} from user {user_id}: {e}")
        flash('An error occurred while removing the movie from the user. '
              'Please try again later. 🍸', 'error')

    # Stay on the user's movie list page, where the action was triggered
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/delete_user', methods=['POST'])
def delete_user(user_id):
    """
    Delete a user from the database.
    Args:
        user_id (int): The ID of the user to be deleted.
    Returns:
        Response: Redirect to the list of users with a flash message indicating success or failure.
    """
    try:
        success = data_manager.delete_user(user_id)
        if success:
            flash(f"User with ID {user_id} has been deleted successfully! 🦩",
                  'success')
        else:
            flash(f"User with ID {user_id} could not be deleted. 🦤", 'error')

    except Exception as e:
        app.logger.error(f"Error deleting user with ID {user_id}: {e}")
        flash('An error occurred while deleting the user. Please try again later. 🌭',
              'error')

    # Redirect to the list of users after deletion
    return redirect(url_for('list_users'))


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 (Page Not Found) errors.
    Args:
        e (HTTPException): The exception object for the 404 error.
    Returns:
        Response: Render the 404 error page template with the status code 404.
    """
    app.logger.warning(f"404 error occurred: {e}")
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """
    Handle 500 (Internal Server Error) errors.
    Args:
        e (HTTPException): The exception object for the 500 error.
    Returns:
        Response: Render the 500 error page template with the status code 500.
    """
    # Log the error for debugging purposes
    app.logger.error(f"Server error: {e}, route: {request.url}")
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
