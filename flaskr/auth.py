import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User
from flaskr import db

from flask_login import login_user, logout_user, current_user

from .email.email import send_email
from flask import render_template
from flask import session


import uuid

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
            send_email(subject='Logged In',
               sender='zahur@gmail.com',
               recipients=[user.email],
               text_body=render_template('emails/email_template.txt'),
               html_body=render_template('emails/email_template.html'))
            return redirect(url_for('example.example'))

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@bp.route('/reset_password',  methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']

        otp = uuid.uuid4().hex[:6]
        print(otp)
        session['otp'] = otp
        session['email']= email

        user = User.query.filter_by(email=session['email']).first()

        send_email(subject='Reset Email',
               sender='zahur@gmail.com',
               recipients=[email],
               text_body=render_template('emails/reset_email.txt', email=email, opt=otp, name=user.username),
               html_body=render_template('emails/reset_email.html', email=email, otp=otp, name=user.username))
        return redirect(url_for('auth.password_change')) 

    return render_template('auth/reset_password.html')


@bp.route('/password_change',  methods=['GET', 'POST'])
def password_change():
    email = session['email']
    otp = session['otp']
    user = User.query.filter_by(email=email).first()
    if request.method == 'POST':
        form_password_one= request.form['password']
        form_password_two= request.form['password_two']
        form_otp = request.form['otp']

        if form_otp != otp:
            flash('Incorrect otp. Try again')
            return redirect(url_for('auth.reset_password'))
        elif form_password_one != form_password_two:
            flash('Password do not match, Try again')
            return redirect(url_for('auth.reset_password'))
        else:
            user.password_hash = generate_password_hash(form_password_one)
            db.session.commit()

            session.pop('email', None)
            session.pop('otp', None)

            flash('Password reset successful')
            return redirect(url_for('auth.login'))
                
    return render_template('auth/password_change.html')