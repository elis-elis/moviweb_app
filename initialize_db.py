from app import app
from data_models import db


with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
