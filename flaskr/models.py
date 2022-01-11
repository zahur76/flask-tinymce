from flaskr import db
from flask_login import UserMixin
from flaskr import login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Page(db.Model):

    __tablename__ = "pages"
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.now())
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    content = db.Column(db.Text())

    def __repr__(self):
        return '<User {}>'.format(self.title)

