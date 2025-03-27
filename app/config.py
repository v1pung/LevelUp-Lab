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
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    SECRET_KEY = 'a9d88e801e38392980c6710f3e5e742443e8c159'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

