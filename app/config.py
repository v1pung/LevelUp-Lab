import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)

    # SQLALCH
    default_local_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@127.0.0.1:5332/{os.getenv('POSTGRES_DB')}"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default_local_url)
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
