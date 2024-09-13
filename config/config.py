import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    db_path = os.path.join(os.getcwd(), 'data', 'moviweb.sqlite')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
