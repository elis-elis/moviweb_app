"""
The sqlite_data_manager.py file defines a class, SQLiteDataManager,
that manages interactions with an SQLite database for the MoviWeb application.
This class implements the DataManagerInterface, providing the actual functionality
required to perform operations on the database, such as retrieving, adding, deleting,
and updating movies for users.
"""

from data_manager_interface import DataManagerInterface
from data_models import db, User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_session):
        self.db_session = db_session
