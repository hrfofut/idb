from flask import Blueprint, render_template

stores = Blueprint('stores', __name__)

first = 0
last = 2


@stores.route("/")
def stores_overview():
    return render_template('stores/stores.html')


@stores.route("/<int:id>")
def stores_detail(id):
    """TODO: Have the template be filled from a database in the future"""
    # ID 0-2 returns certain food page, else return error
    if id < first or id > last:
        return render_template('errors/404.html'), 404
    return render_template('stores/storesdetail.html', title=id)
