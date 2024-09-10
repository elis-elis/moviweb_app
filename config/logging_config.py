import logging
from flask import Flask
import os


def setup_logging(app: Flask):
    if not app.debug:
        # Ensure the 'logs' directory exists
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # File handler for logging to 'logs/error.log'
        file_handler = logging.FileHandler('logs/error.log')  # Update this line
        file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
