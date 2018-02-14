from flask import Blueprint, render_template

foods = Blueprint('foods', __name__)

first = 0
last = 2


@foods.route("/")
def foods_overview():
    return render_template('foods/food.html')


@foods.route("/<int:id>")
def food_detail(id):
    """TODO: Have the template be filled from a database in the future"""
    # However the backend will work, use id to find all the info.

    # ID 0-2 returns certain food page, else return error
    icecream = {'img': 'http://del.h-cdn.co/assets/17/23/1600x800/landscape-1497238977-delish-mason-jar-ice-cream-3.jpg', 'name': 'icecream', 'calories': '137', 'serving': '1/2 cup', 'sodium': '53 mg', 'fat': '7 g', 'protein': '2.3 g'}
    burger = {'img': 'http://baileysrestaurants.com/range/files/2013/02/IMG_1700.jpg', 'name': 'burger', 'calories': '354', 'serving': '1 item', 'sodium': '497 mg', 'fat': '17 g', 'protein': '20 g'}
    waffle = {'img': 'http://catchyscoop.com/wp-content/uploads/2016/07/calories-in-a-waffle.jpg', 'name': 'waffle', 'calories': '82', 'serving': '1 oz', 'sodium': '145 mg', 'fat': '4 g', 'protein': '2.2 g'}

    foods = [icecream, burger, waffle]
    if id < first or id > last:
        return render_template('errors/404.html'), 404
    return render_template('foods/fooddetail.html', food=foods[id])
