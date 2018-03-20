from idb import db


# Need to figure out what to put in here
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    phone = db.Column(db.Integer)
    ratings = db.Column(db.Float)

    def __init__(self, id, name, location, description, phone, ratings):
        self.id = id
        self.name = name
        self.location = location
        self.description = description
        self.phone = phone
        self.ratings = ratings


class Gyms(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50))
    ratings = db.Column(db.Float)

    def __init__(self, id, name, location, price, ratings):
        self.id = id
        self.name = name
        self.location = location
        self.price = price
        self.ratings = ratings


class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(255))
    link = db.Column(db.String(255))
    category = db.Column(db.String(10))
    equipment = db.Column(db.String(50))
    description = db.Column(db.String(255))
    muscle = db.Column(db.String(50))
    met = db.Column(db.Float)

    def __init__(self, id, name, img, link, category, equipment, description, muscle, met):
        self.id = id
        self.name = name
        self.img = img
        self.link = link
        self.category = category
        self.equipment = equipment
        self.description = description
        self.muscle = muscle
        self.met = met
