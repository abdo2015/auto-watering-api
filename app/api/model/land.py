from flask_login import UserMixin

from ... import db  # , bcrypt, login_manager


class Land(db.Model, UserMixin):
    """ Lands Model for storing Lands related details """
    __tablename__ = "land"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    positive_area = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"land ID : {self.id}, Land Area: {self.positive_area}"

    @property
    def land_area(self):
        return self.land_area

    @land_area.setter
    def land_area(self, area):
        if int(area) < 0:
            raise ValueError("area can't >= 0 !!")
        else:
            self.positive_area = area
