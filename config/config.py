import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')

    basedir = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
    db_path = os.path.join(basedir, 'data', 'moviweb.sqlite')

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
