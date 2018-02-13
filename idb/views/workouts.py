from flask import Blueprint, render_template

workouts = Blueprint('workouts', __name__)


@workouts.route("/")
def workouts_overview():
    return render_template('workouts/workouts.html')


@workouts.route("/<id>")
def workouts_detail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('workouts/workoutsdetail.html', title=id)
