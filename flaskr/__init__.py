import os
from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from werkzeug.security import generate_password_hash
mail = Mail()


db = SQLAlchemy()
migrate = Migrate(db)
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    db.init_app(app)
    migrate.init_app(app, db)

    # set-up user login security
    login_manager.init_app(app)

    # set-up mail
    mail.init_app(app)

    from .models import User
    
    # home page   
    @app.route('/')
    def home():
        user = User.query.filter_by(username='zahur').first()
        if user:
            return render_template('home/home.html')
        user= User()
        user.username = 'zahur'
        user.password_hash = generate_password_hash('zahur')
        user.email = 'za@hotmail.com'
        user.save()
        return render_template('home/home.html')
        

    # Register auth bp
    from . import auth, example
    app.register_blueprint(auth.bp)
    app.register_blueprint(example.bp)

    return app