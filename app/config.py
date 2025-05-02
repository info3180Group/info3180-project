from dotenv import load_dotenv
load_dotenv()
import os


class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    #SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed