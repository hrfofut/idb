from flask import Blueprint, render_template

gyms = Blueprint('gyms', __name__)

@gyms.route("/")
def gyms_overview():
    return render_template('gyms/gyms.html')


@gyms.route("/<id>")
def gyms_detail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('gyms/gymsdetail.html')
