"""
The sqlite_data_manager.py file defines a class, SQLiteDataManager,
that manages interactions with an SQLite database for the MoviWeb application.
This class implements the DataManagerInterface, providing the actual functionality
required to perform operations on the database, such as retrieving, adding, deleting,
and updating movies for users.
"""

from datamanager.data_manager_interface import DataManagerInterface
from data_models import db, User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        """
        Initialize the SQLiteDataManager with a Flask app instance.
        Flask app instance is passed to the SQLiteDataManager class because SQLAlchemy needs
        to be configured and initialized in the context of the Flask application.
        The Flask application context (app) holds the configuration settings necessary for
        SQLAlchemy to connect to the database, manage sessions, and handle requests.
        """
        self.app = app
        self.db = db
        self.db.init_app(app)   # binds the database to the Flask application

    def get_all_users(self):
        """
        Retrieve all user records from the database.
        """
        with self.app.app_context():
            # 'with' ensures the Flask application context is active for database operations
            return self.db.session.query(User).all()

    def get_user_movies(self, user_id):
        """
        Filters the 'Movie' table and returns only movies associated with the provided user_id.
        Returns a list of Movie objects for the specified user.
        """
        with self.app.app_context():
            user = self.db.session.query(User).filter_by(user_id=user_id).first()

            # Check if the user was found
            if user is not None:
                movies = user.movies
            else:
                movies = []

            return movies

    def add_user(self, user_name):
        """
        This method adds a new user to the database.
        """
        with self.app.app_context():
            new_user = User(user_name=user_name)
            self.db.session.add(new_user)
            self.db.session.commit()

    def add_movie(self, movie_data):
        """
        Add a new movie to the database.
        movie_data is a dictionary containing information about the movie that user wants to add.
        This block creates a new instance of the Movie class using the data provided.
        """
        with self.app.app_context():
            new_movie = Movie(
                title=movie_data.get('title'),
                director=movie_data.get('director'),
                release_year=movie_data.get('release_year'),
                movie_rating=movie_data.get('rating')
            )
            self.db.session.add(new_movie)
            self.db.session.commit()
            return new_movie.movie_id

    def add_movie_to_user(self, user_id, movie_id):
        """
        This method associates a movie with a specific user.
        """
        with self.app.app_context():
            # user_id is unique, so querying for a single record
            # .first() returns that single record (if it exists) or None
            user = self.db.session.query(User).filter_by(user_id=user_id).first()
            movie = self.db.session.query(Movie).filter_by(movie_id=movie_id).first()
            if user and movie:
                if movie not in user.movies:
                    self.db.session.append(movie)   # This appends the movie to the user's movie list
                    self.db.session.commit()

    def remove_movie_from_user(self, user_id, movie_id):
        """
        This method dissociates a movie from a specific user.
        """
        with self.app.app_context():
            user = self.db.session.query(User).filter_by(user_id=user_id).first()
            movie = self.db.session.query(Movie).filter_by(movie_id=movie_id).first()
            if user and movie:
                if movie in user.movies:
                    self.db.session.remove(movie)   # This removes the movie from the user's movie list
                    self.db.session.commit()

    def delete_movie(self, movie_id):
        """This method deletes a movie from the database."""
        with self.app.app_context():
            movie = self.db.session.query(Movie).filter_by(movie_id=movie_id).first()
            if movie:
                self.db.session.delete(movie)
                self.db.session.commit()

    def delete_user(self, user_id):
        """This method deletes a user from the database."""
        with self.app.app_context():
            user = self.db.session.query(User).filter_by(user_id=user_id).first()
            if user:
                self.db.session.delete(user)
                self.db.session.commit()

    def update_movie(self, movie_id, updated_data):
        """
        Updates the movie record in the database. This affects all users who have this movie
        associated with them because the movie’s details are stored centrally in the Movie table.
        """
        with self.app.app_context():
            movie = self.db.session.query(Movie).filter_by(movie_id=movie_id).first()
            if movie:
                # If 'title' is present in updated_data, its value is used.
                # If 'title' is not in updated_data, the current movie.title remains unchanged.
                movie.title = updated_data.get('title', movie.title)
                movie.director = updated_data.get('director', movie.director)
                movie.release_year = updated_data.get('release_year', movie.release_year)
                movie.movie_rating = updated_data.get('rating', movie.movie_rating)
                self.db.session.commit()
