import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/elisnothing/PycharmProjects/moviweb_app/data/moviweb_app.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
