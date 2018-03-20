from idb import db


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name


class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))
    phone = db.Column(db.Integer)
    ratings = db.Column(db.Integer)

    def __init__(self, id, name, location, description, phone, ratings)
        self.id = id
        self.name = name
        self.location = location
        self.description = description
        self.phone = phone
        self.ratings = ratings
