import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = (
        'postgresql://myuser:aibekarsen@localhost:5432/health_info_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False