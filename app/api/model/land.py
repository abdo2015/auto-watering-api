from flask_login import UserMixin

from ... import db  # , bcrypt, login_manager


class Land(db.Model, UserMixin):
    """ Lands Model for storing Lands related details """
    __tablename__ = "land"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    positive_area = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'))

    def __repr__(self):
        plant = None
        if self._plant_id:
            plant = Plant.query.get(self._plant_id) or None
        if not plant:
            return f"land ID : {self.id}, Land Area: {self.positive_area}, No plant in this land!"

        return f"land ID : {self.id}, Land Area: {self.positive_area}, plant Info: [{plant}]"
        # return dict(ID=self.id, Area=self.positive_area, plant_info=plant)

    @property
    def land_area(self):
        return self.land_area

    @land_area.setter
    def land_area(self, area):
        if int(area) < 0:
            raise ValueError("area can't be >= 0 !!")
        else:
            self.positive_area = area

    @property
    def plant_id(self):
        return self._plant_id

    @plant_id.setter
    def plant_id(self, pid):
        plant = Plant.query.get(pid)
        if not plant:
            raise ValueError(f"no plant has id = {pid}")
        self._plant_id = pid

    @property
    def serialize(self):
        plant = None
        if self._plant_id:
            plant = Plant.query.get(self._plant_id) or None
        if not plant:
            return {"land_ID": self.id, "Area": self.positive_area}

        return {"land_ID": self.id, "Area": self.positive_area, "plant_ID": plant.id,
                "plant_name": plant.name, "water_amount": plant._water_amount}


class Plant(db.Model, UserMixin):
    """ Plant Model for storing Plant related details """
    __tablename__ = "plant"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    _water_amount = db.Column(db.Float, nullable=False)
    fertilizer = db.Column(db.String, nullable=False)
    lands = db.relationship('Land', backref='land', lazy=False)

    def __repr__(self):
        return f"plant ID : {self.id},name : {self.name}, water amount: {self._water_amount}"
        # return dict(plant_ID=self.id, name=self.name, water_amount=self._water_amount)

    @property
    def water_amount(self):
        return self._water_amount

    @water_amount.setter
    def water_amount(self, w_amount):
        if int(w_amount) <= 0:
            raise ValueError("Water amount can't be <=0!")
        self._water_amount = w_amount
