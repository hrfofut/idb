from flask import Blueprint, render_template, abort

foods = Blueprint('foods', __name__)

first = 0
last = 2

icecream = {'img': 'http://del.h-cdn.co/assets/17/23/1600x800/landscape-1497238977-delish-mason-jar-ice-cream-3.jpg', 'name': 'Ice Cream', 'calories': '137', 'serving': '1/2 cup', 'sodium': '53 mg', 'fat': '7 g', 'protein': '2.3 g'}
burger = {'img': 'http://baileysrestaurants.com/range/files/2013/02/IMG_1700.jpg', 'name': 'Burger', 'calories': '354', 'serving': '1 item', 'sodium': '497 mg', 'fat': '17 g', 'protein': '20 g'}
waffle = {'img': 'http://catchyscoop.com/wp-content/uploads/2016/07/calories-in-a-waffle.jpg', 'name': 'Waffle', 'calories': '82', 'serving': '1 oz', 'sodium': '145 mg', 'fat': '4 g', 'protein': '2.2 g'}
foods_list = [icecream, burger, waffle]


@foods.route("/")
def foods_overview():
    global foods_list

    # TODO: I need to remember to describe whats going on later.
    items = []
    for val in foods_list:
        items.append([val['name'], val['img'], val['calories'], val['fat']])

    return render_template('foods/food.html', items=items)


@foods.route("/<int:id>")
def food_detail(id):
    global foods_list
    """TODO: Have the template be filled from a database in the future"""
    # However the backend will work, use id to find all the info.

    # ID 0-2 returns certain food page, else return error
    if id < first or id > last:
        return abort(404)
    return render_template('foods/fooddetail.html', food=foods_list[id])
