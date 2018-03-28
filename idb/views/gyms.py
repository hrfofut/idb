from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from idb.models import Gyms, Images
# Later lets have a python thing that has all db calls
from idb import db

from backend.tools import unbinary
import base64

gyms = Blueprint('gyms', __name__)

first = 0
last = -1


@gyms.route("/")
def gyms_overview():
    items = []
    all_gyms = db.session.query(Gyms).all()
    for gym in all_gyms:
        image = db.session.query(Images).get(gym.pic_id).pic
        img = unbinary(str(base64.b64encode(image)))
        items.append([gym.name, img, gym.location, gym.ratings, gym.id])
    return render_template('gyms/gyms.html', items=items)


@gyms.route("/<int:id>")
def gyms_detail(id):
    global last
    if last == -1:
        last = db.session.query(Gyms).count()
    # ID 0 to gym count returns certain gym page, else return error
    if id < first or id > last:
        abort(404)
    gym = db.session.query(Gyms).get(id)
    image = db.session.query(Images).get(gym.pic_id).pic
    img = unbinary(str(base64.b64encode(image)))
    return render_template('gyms/gymsdetail.html', gym=gym, pic=img)
