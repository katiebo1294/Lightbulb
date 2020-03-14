import os


class Config:
    SECRET_KEY = 'a7fc44f15ab68e45d593cf6f03197c50'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:bettercrative@localhost/bettercrative_db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
