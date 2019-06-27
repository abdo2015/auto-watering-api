from flask_login import UserMixin

from ... import db, bcrypt, login_manager
from .land import Land


class User(db.Model, UserMixin):
    """ User Model for storing user related details """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    # public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    lands = db.relationship('Land', backref='user', lazy=False)
    role = db.Column(db.String(10), default='user')  # can be user or admin

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def num_of_lands(self):
        return len(self.lands)

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    @property
    def isAdmin(self):
        return True if self.role == 'admin' else False

    def __repr__(self):
        if not self.isAdmin:
            return f"ID: {self.id}, user name: {self.username}, lands: {self.lands}"

        return f"ID: {self.id}, Admin name: {self.username}"
