from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Association table for the many-to-many relationship
user_movies = db.Table(
    'user_movies',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.movie_id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)

    # Establishing a relationship with the Movie table
    movies = relationship('Movie', secondary=user_movies, back_populates='users')

    def __repr__(self):
        return f"<User(id={self.user_id}, name={self.user_name})>"


class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(150), nullable=False)
    release_year = db.Column(db.Integer, nullable=True)
    movie_rating = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Establishing a relationship back to the User table
    user = relationship('User', secondary=user_movies, back_populates='movies')

    def __repr__(self):
        return f"'{self.title}' directed by {self.director}, released on {self.release_year}, rated {self.movie_rating}"

