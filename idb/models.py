from idb import db


# Need to figure out what to put in here
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(100))
    servings = db.Column(db.String(10))
    calorie = db.Column(db.String(10))
    sodium = db.Column(db.String(10))
    fat = db.Column(db.String(10))
    protein = db.Column(db.String(10))

    def __init__(self, id, name, img, servings, calorie, sodium, fat, protein):
        self.id = id
        self.name = name
        self.img = img
        self.servings = servings
        self.calorie = calorie
        self.sodium = sodium
        self.fat = fat
        self.protein = protein


class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    gid = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    price_level = db.Column(db.Integer)
    ratings = db.Column(db.Float)

    def __init__(self, id, gid, name, location, price_level, ratings):
        self.id = id
        self.gid = gid
        self.name = name
        self.location = location
        self.price_level = price_level
        self.ratings = ratings


class Gyms(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    gid = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50))
    ratings = db.Column(db.Float)

    def __init__(self, id, gid, name, location, price, ratings):
        self.id = id
        self.gid = gid
        self.name = name
        self.location = location
        self.price = price
        self.ratings = ratings


class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(255))
    link = db.Column(db.String(255))
    category = db.Column(db.String(20))
    equipment = db.Column(db.String(100))
    description = db.Column(db.String(1024))
    muscle = db.Column(db.String(512))
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
