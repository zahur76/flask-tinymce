import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User
from flaskr import db

from flask_login import login_user, logout_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        password_encode = generate_password_hash(password)

        user = User.query.filter_by(username=username).first()
        check_email = User.query.filter_by(email=email).first()
        
        if user:
            flash(f"User {username} is already registered.")
            return redirect(url_for('home'))
        elif check_email:
            flash(f"Email {email} is already registered.")
            return redirect(url_for('home'))
        else:
            user = User(username=username, password_hash=password_encode, email=email)
            db.session.add(user)
            db.session.commit()
            flash('Registered')
            print('registration complete')
            return redirect(url_for('home'))

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password_hash, password):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        else:
            login_user(user)
            return redirect(url_for('example.example'))

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))