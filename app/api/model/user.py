from flask_login import UserMixin

from ... import db, bcrypt, login_manager


class User(db.Model, UserMixin):
    """ User Model for storing user related details """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    # public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    def __repr__(self):
        return f"ID: {self.id}, user name: {self.username}"
