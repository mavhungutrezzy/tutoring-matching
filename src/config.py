import logging
import os

from dotenv import load_dotenv


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = ""
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "postgresql://mavhungu:password@localhost:5432/affidavit"


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = ""
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
