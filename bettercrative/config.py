import os
import psycopg2

# creates a base directory for environment
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'a7fc44f15ab68e45d593cf6f03197c50'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'bettercrative@gmail.com'
    MAIL_PASSWORD = 'kK6yH2x*Lx!M'
    # we need this because we're developing on localhost
    AUTHLIB_INSECURE_TRANSPORT = True


# For production server
class ProductionConfig(Config):
    DEBUG = False


# Where we work on things
class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


# where we test things
class TestingConfig(Config):
    TESTING = True
