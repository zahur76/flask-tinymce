import os
basedir = os.path.abspath(os.path.dirname(__file__))

from pathlib import Path

class Config(object):
    ENV = "development"
    DEBUG = True
    SECRET_KEY = os.urandom(12)
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    EMAIL_CONFIRMATION_DISABLED = False

    BASE_DIR = Path(__file__).resolve().parent
    print(BASE_DIR)
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'flaskr/static/upload')
    
    # flask-mailman configs
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = '' # os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = '' # os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = 'zahur@mail.com' # os.environ.get("MAIL_DEFAULT_SENDER")
