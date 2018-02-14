from flask import Blueprint, render_template

gyms = Blueprint('gyms', __name__)

first = 0
last = 2


@gyms.route("/")
def gyms_overview():
    return render_template('gyms/gyms.html')


@gyms.route("/<int:id>")
def gyms_detail(id):
    """TODO: Have the template be filled from a database in the future"""

    # ID 0-2 returns certain food page, else return error
    if id < first or id > last:
        return render_template('errors/404.html'), 404

    return render_template('gyms/gymsdetail.html', title=id)
