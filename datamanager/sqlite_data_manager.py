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
        self.db = db    # sqlalchemy object from data_models
        db.init_app(app)    # initialization of the db in the app
        with self.app.app_context():
            # 'with' ensures the Flask application context is active for database operations
            self.db.create_all()    # create all tables

    def list_all_users(self):
        """
        Retrieve all user records from the database.
        """
        return self.db.session.query(User).all()

    def get_all_movies(self):
        """
        Retrieve all movies from the database.
        """
        return self.db.session.query(Movie).all()

    def get_user_by_id(self, user_id):
        """
        Retrieve a specific user by their ID.
        """
        return self.db.session.query(User).filter_by(user_id=user_id).first()

    def get_user_movies(self, user_id):
        """
        Filters the 'Movie' table and returns only movies associated with the provided user_id.
        Returns a list of Movie objects for the specified user.
        """
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
        new_user = User(user_name=user_name)
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user.user_id  # Return the new user's ID to confirm addition

    def add_movie(self, movie_data):
        """
        Add a new movie to the database.
        movie_data is a dictionary containing information about the movie that user wants to add.
        This block creates a new instance of the Movie class using the data provided.
        """
        new_movie = Movie(
            title=movie_data.get('title'),
            director=movie_data.get('director'),
            release_year=movie_data.get('release_year'),
            movie_rating=movie_data.get('rating')
        )
        self.db.session.add(new_movie)
        self.db.session.commit()
        return new_movie.movie_id   # Return the movie ID to confirm addition

    def get_movie_by_id(self, movie_id):
        """
        Retrieve a specific movie by its ID.
        """
        return self.db.session.query(Movie).filter_by(movie_id=movie_id).first()

    def add_movie_to_user(self, user_id, movie_id):
        """
        This method associates an existing movie with a specific user.
        """
        # user_id is unique, so querying for a single record
        # .first() returns that single record (if it exists) or None
        user = self.db.session.query(User).filter_by(user_id=user_id).first()
        movie = self.db.session.query(Movie).filter_by(movie_id=movie_id).first()

        if user and movie:
            # Only append the movie if it is not already in the user's movie list
            if movie not in user.movies:
                user.movies.append(movie)   # This appends the movie to the user's movie list
                self.db.session.commit()
                return True
            else:
                print("Movie already in user's list")
        else:
            print("User or movie not found")
        return False

    def remove_movie_from_user(self, user_id, movie_id):
        """
        This method dissociates a movie from a specific user.
        """
        user = self.db.session.query(User).filter_by(user_id=user_id).first()
        movie = self.db.session.query(Movie).filter_by(movie_id=movie_id).first()
        if user and movie:
            if movie in user.movies:
                # This removes the movie from the user's movie list,
                # rather than trying to delete the movie object directly from the session
                user.movies.remove(movie)
                self.db.session.commit()
                return True
            return False

    def delete_movie(self, movie_id):
        """This method deletes a movie from the database."""
        movie = self.db.session.query(Movie).filter_by(movie_id=movie_id).first()
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()
            return True
        return False    # Return False if movie was not found

    def delete_user(self, user_id):
        """This method deletes a user from the database."""
        user = self.db.session.query(User).filter_by(user_id=user_id).first()
        if user:
            self.db.session.delete(user)
            self.db.session.commit()
            return True   # Return True to indicate successful deletion
        return False

    def update_movie(self, movie_id, updated_movie_data):
        """
        Update movie details in the database that affect all users who have this movie in their favorite list.
        """
        movie = self.db.session.query(Movie).filter_by(movie_id=movie_id).first()
        if movie:
            # If 'title' is present in updated_data, its value is used.
            # If 'title' is not in updated_data, the current movie.title remains unchanged.
            movie.title = updated_movie_data.get('title', movie.title)
            movie.director = updated_movie_data.get('director', movie.director)
            movie.release_year = updated_movie_data.get('release_year', movie.release_year)
            movie.movie_rating = updated_movie_data.get('rating', movie.movie_rating)
            self.db.session.commit()
            return True
        return False
