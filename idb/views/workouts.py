from flask import Blueprint, render_template

workouts = Blueprint('workouts', __name__)

first = 0
last = 2


@workouts.route("/")
def workouts_overview():
    return render_template('workouts/workouts.html')


@workouts.route("/<int:id>")
def workouts_detail(id):
    """TODO: Have the template be filled from a database in the future"""

    # ID 0-2 returns certain food page, else return error
    if id < first or id > last:
        return render_template('errors/404.html'), 404
    return render_template('workouts/workoutsdetail.html', title=id)
