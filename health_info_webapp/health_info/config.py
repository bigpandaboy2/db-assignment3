import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://database_postgres_c915_user:OX1MeboNb9M13zKX05xm4upXXo4fsdYJ@dpg-cstm1mi3esus73d5e220-a/database_postgres_c915'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False