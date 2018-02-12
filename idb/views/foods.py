from flask import Blueprint, render_template

foods = Blueprint('foods', __name__)


@foods.route("/")
def foods_overview():
    return render_template('foods/food.html')


@foods.route("/<id>")
def food_detail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('foods/fooddetail.html')
