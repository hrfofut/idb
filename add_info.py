import json
import requests

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from idb.models import Stores,

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://Calorieking:seargohsiEHFGUOAEHRGIOHPOSk578@ckcdbinstance.c48dginqtauy.us-west-2.rds.amazonaws.com/CKCDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

req_stores = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=30.2671530,-97.7430610&radius=5000&type=supermarket&key=AIzaSyDZfXyk7j9KmKSc88XsI0YkUvpPKufPlUs')
if(req_stores.status_code == requests.codes.ok):
    req_stores_json = req_stores.json()
    for stores in req_stores_json['results']:
        pl = 0
        rating = 0

        if 'price_level' in stores:
            pl = stores['price_level']

        if 'rating' in stores:
            rating = stores['rating']

        store = Stores(
                id=stores['id'],
                name=stores['name'],
                location=stores['vicinity'],
                price_level=pl,
                ratings=rating
        )

        db.session.add(store)
        db.session.commit()
