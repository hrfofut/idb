import json
import requests


from io import open as iopen

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from idb.models import Stores, Images, Gyms
# Next three lines create the app and then load config from the instance folder.
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('default_config.py')
app.config.from_pyfile('application.py', silent=True)

app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
p_det1 = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='
p_det2 = '&key=' + app.config['PLACE_KEY']  # The key header for place apis.

p_img1 = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference='
print("running")

# Changing type=gym to type=supermarket will change the search to be about stores.
req_gyms = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=30.2671530,-97.7430610&radius=5000&type=gym&key=' + app.config['PLACE_KEY'])
if(req_gyms.status_code == requests.codes.ok):
    req_gyms_json = req_gyms.json()
    print("here")
    ident = 0
    for gyms in req_gyms_json['results']:
        print("next")
        pl = 0
        rating = 0
        if 'price_level' in gyms:
            pl = gyms['price_level']

        if 'rating' in gyms:
            rating = gyms['rating']
        gym = Gyms(
                id=ident,
                gid=gyms['place_id'],
                name=gyms['name'],
                location=gyms['vicinity'],
                price_level=pl,
                ratings=rating
                )
        ident += 1
        # place details
        details_response = requests.get(p_det1 + gym.gid + p_det2)
        det_r = details_response.json()
        pr = ''
        print('chk')
        if 'photos' in gyms:
            for photo in gyms['photos']:
                pr = photo['photo_reference']
            if 'formatted_phone_number' in det_r['result']:
                gym.phone = det_r['result']['formatted_phone_number']
            print(gym.phone)
            print("pr:" + pr)
            # place image
            i = requests.get(p_img1 + pr + p_det2)
            name = "test.jpg"
            if i.status_code == requests.codes.ok:
                with iopen(name, 'wb') as file:
                    file.write(i.content)
            else:
                print("failure")
                print(i.json())
            image = Images(pic=i.content)

            """COMMENTS AFTER THIS POINT ACTUALLY MODIFY OUR DATABASE. UNCOMMENT TO ACTUALLY MODIFY."""
            # pid = db.session.execute("SELECT nextval('images_pic_id_seq') AS id").fetchone()
            # pid2 = pid['id']
            # image.pic_id = pid2
            # db.session.add(image)
            # db.session.commit()

            # gym.pic_id = pid2

            # db.session.add(gym)
            # db.session.commit()
