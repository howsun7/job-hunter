import os

db_path = os.path.join(os.path.dirname(__file__), 'app.db')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'not-a-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_URL') or \
        f'sqlite:///{db_path}'
