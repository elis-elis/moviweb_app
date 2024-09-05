import os 

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///moviweb_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    