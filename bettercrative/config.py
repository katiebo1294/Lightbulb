import os

basedir = os.path.abspath(os.path.dirname(__file__))  # creates a base directory for environment


class Config(object):
    SECRET_KEY = 'a7fc44f15ab68e45d593cf6f03197c50'
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')


# For production server
class ProductionConfig(Config):
    DEBUG = False


# Where we work on things
class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = False


# where we test things
class TestingConfig(Config):
    TESTING = True
