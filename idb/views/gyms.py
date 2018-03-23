from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from idb.models import Gyms, Images
# Later lets have a python thing that has all db calls
from idb import db
import base64
gyms = Blueprint('gyms', __name__)

first = 0
last = -1


@gyms.route("/")
def gyms_overview():
    img = 'https://vignette.wikia.nocookie.net/spongebob/images/2/2e/Bikini_Bottom_Gym.png/revision/latest?cb=20140828023711'
    items = []

    get_gyms = db.session.query(Gyms).all()

    for val in get_gyms:
        image = db.session.query(Images).get(val.pic_id).pic
        x = str(base64.b64encode(image))
        x = x[2:]
        x = x[:-1]
        items.append([val.name, img, val.location, val.ratings, val.id, x])

    return render_template('gyms/gyms.html', items=items)


@gyms.route("/<int:id>")
def gyms_detail(id):
    global last
    # TODO: Have the template be filled from a database in the future
    if last == -1:
        last = db.session.query(Gyms).count()

# ID 0-2 returns certain food page, else return error
    if id < first or id > last:
        abort(404)

    gym = db.session.query(Gyms).get(id)

    image = db.session.query(Images).get(gym.pic_id).pic
    x = str(base64.b64encode(image))
    x = x[2:]
    x = x[:-1]
    return render_template('gyms/gymsdetail.html', gym=gym, pic=x)
