import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    
    # postgres
    USER = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    HOST = os.getenv('POSTGRES_HOST')
    PORT = os.getenv('POSTGRES_PORT')
    DB = os.getenv('POSTGRES_DB')

    # SQLALCH
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
