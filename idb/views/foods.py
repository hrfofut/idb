from flask import Blueprint, render_template

foods = Blueprint('foods', __name__)


@foods.route("/")
def foods_overview():
    return render_template('foods/food.html')


@foods.route("/<id>")
def food_detail(id):
    """TODO: Have the template be filled from a database in the future"""
    # However the backend will work, use id to find all the info.

    return render_template('foods/fooddetail.html', title=id)
