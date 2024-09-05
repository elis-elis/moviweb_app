from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """Retrieve a list of all users."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Retrieve a list of movies for a specific user."""
        pass

    @abstractmethod
    def add_movie(self, user_id, movie_data):
        """Add a movie to a specific user's list."""
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """Delete a movie to a specific user's list."""
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, updated_data):
        """Updates the details of a specific movie in a specific user's list."""
        pass
