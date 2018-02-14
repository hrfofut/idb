from flask import Blueprint, render_template

foods = Blueprint('foods', __name__)

first = 1
last = 3


@foods.route("/")
def foods_overview():
    return render_template('foods/food.html')


@foods.route("/<int:id>")
def food_detail(id):
    """TODO: Have the template be filled from a database in the future"""
    # However the backend will work, use id to find all the info.

    # ID 1-3 returns certain food page, else return error
    if id < first or id > last:
        return render_template('errors/404.html'), 404
    return render_template('foods/fooddetail.html', title=id)
