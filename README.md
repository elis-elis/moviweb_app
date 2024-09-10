# Flask Movie Management Application

This is a Flask-based web application that allows users to manage a list of movies and associate them with different users. Users can add new movies, edit their details, and delete them. Additionally, users can add existing movies to their personal lists or remove them as desired. This application integrates with the OMDb API to fetch movie details dynamically.

## Features

- **User Management:** Add, view, and delete users.
- **Movie Management:** Add new movies by fetching details from the OMDb API, edit existing movies, and delete them.
- **User-Movie Association:** Associate existing movies with users, and manage (add/remove) movies in a user's personal list.
- **Error Handling:** Custom error pages for 404 (Page Not Found) and 500 (Internal Server Error).
- **Persistent Data Storage:** Utilizes SQLite for data storage, ensuring persistence even after server restarts.
- **Logging:** Error and information logging to facilitate debugging.

## Project Structure

- **app.py**: The main application file containing all route definitions and core logic.
- **config/**: Configuration files for logging and application settings.
- **data_models.py**: Data models for SQLite integration.
- **datamanager/**: Contains the `SQLiteDataManager` class to handle data operations.
- **templates/**: HTML templates for rendering web pages.
- **static/**: Static files such as CSS, JavaScript, and images.
- **initialize_db.py**: A script to initialize or reset the database schema.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [OMDb API](http://www.omdbapi.com/)