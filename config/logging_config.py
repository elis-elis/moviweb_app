import logging
from flask import Flask
import os


def setup_logging(app: Flask):
    if not app.debug:
        log_dir = os.path.join(os.path.expanduser("~"), 'moviweb_app', 'logs')

        # Ensure the 'logs' directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            # exist_ok=True: Ensures the directory creation doesn't raise an error if it already exists

        # File handler for logging to 'error.log' in the writable logs directory
        log_file_path = os.path.join(log_dir, 'error.log')
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
