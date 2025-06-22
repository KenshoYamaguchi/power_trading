import os
from datetime import timedelta

SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///power_trade.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
PERMANENT_SESSION_LIFETIME = timedelta(days=7)