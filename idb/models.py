from idb import db


# Need to figure out what to put in here
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(100))
    servings = db.Column(db.String(10))
    calorie = db.Column(db.Float)
    sodium = db.Column(db.Float)
    fat = db.Column(db.Float)
    protein = db.Column(db.Float)
    aisle = db.Column(db.String(40))

    def __init__(self, id, name, img, servings, calorie, sodium, fat, protein, aisle):
        self.id = id
        self.name = name
        self.img = img
        self.servings = servings
        self.calorie = calorie
        self.sodium = sodium
        self.fat = fat
        self.protein = protein
        self.aisle = aisle


class Stores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    price_level = db.Column(db.Integer)
    ratings = db.Column(db.Float)
    phone = db.Column(db.String(15))
    pic_id = db.Column(db.Integer)

    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __init__(self, id, gid, name, location, price_level, ratings, lat, lng, phone="", pic_id=0):
        self.id = id
        self.gid = gid
        self.name = name
        self.location = location
        self.price_level = price_level
        self.ratings = ratings
        self.lat = lat
        self.lng = lng


class Gyms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    price_level = db.Column(db.Integer)
    ratings = db.Column(db.Float)
    phone = db.Column(db.String(15))
    pic_id = db.Column(db.Integer)

    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __init__(self, id, gid, name, location, price_level, ratings, lat, lng, phone="", pic_id=0):
        self.id = id
        self.gid = gid
        self.name = name
        self.location = location
        self.price_level = price_level
        self.ratings = ratings
        self.lat = lat
        self.lng = lng


class Images(db.Model):
    pic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pic = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, pic):
        self.pic = pic


class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(255))
    category = db.Column(db.String(64))
    description = db.Column(db.String(1024))
    met = db.Column(db.Float)
    cid = db.Column(db.Integer)
    parent = db.Column(db.Integer)

    def __init__(self, id, name, img, category, description, met, cid):
        self.id = id
        self.name = name
        self.img = img
        self.category = category
        self.description = description
        self.met = met
        self.cid = cid
