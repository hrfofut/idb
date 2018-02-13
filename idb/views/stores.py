from flask import Blueprint, render_template

stores = Blueprint('stores', __name__)


@stores.route("/")
def stores_overview():
    return render_template('stores/stores.html')


@stores.route("/<id>")
def stores_detail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('stores/storesdetail.html', title=id)
