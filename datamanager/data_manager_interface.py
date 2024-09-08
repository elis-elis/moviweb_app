"""
The file data_manager_interface.py defines an interface called DataManagerInterface
for managing data in my application.
This interface uses abstract methods to outline a set of methods that any data manager
class (like an SQLite or JSON data manager) must implement.
"""

from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def list_all_users(self):
        """
        Retrieve a list of all users.
        """
        pass

    @abstractmethod
    def get_all_movies(self):
        """
        Retrieve all movies from the database.
        """
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        """
        Retrieve a specific user by their ID.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieve a list of movies for a specific user.
        """
        pass

    @abstractmethod
    def add_movie(self, movie_data):
        """
        Add a new movie to the database.
        """
        pass

    @abstractmethod
    def get_movie_by_id(self, movie_id):
        """
        Retrieve a specific movie by its ID.
        """
        pass

    @abstractmethod
    def add_movie_to_user(self, user_id, movie_id):
        """
        Associate an existing movie with a specific user.
        If the movie does not exist, it should be added first before associating it with the user.
        """
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """
        Delete a movie from the database.
        """
        pass

    @abstractmethod
    def remove_movie_from_user(self, user_id, movie_id):
        """
        Dissociate a movie from a specific user.
        """
        pass

    @abstractmethod
    def delete_user(self, user_id):
        """
        Delete a user from the database.
        """
        pass

    @abstractmethod
    def update_movie(self, movie_id, updated_data):
        """
        Update a movie in the database.
        """
        pass
