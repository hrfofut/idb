from flask import Blueprint, render_template, abort

stores = Blueprint('stores', __name__)

first = 0
last = 2

store0 = {
        'img': 'https://bloximages.newyork1.vip.townnews.com/herald-dispatch.com/content/tncms/assets/v3/editorial/5/b5/5b51e47e-bbd5-5b84-915f-5bd9b67bdbe1/581bc9504452f.image.jpg',
        'name': "Trader Joe's",
        'ratings': '4.6/5',
        'location': '211 Walter Seaholm Dr #100, Austin, TX 78701',
        'description': 'Grocery chain with a variety of signature items, plus produce, dairy & more (most sell wine & beer).',
        'phone': '(512) 474-2263'
}

store1 = {
        'img': 'http://upstream-assets-prod.s3.amazonaws.com/Barshopoles/production/uploads/properties/thumbnails/25/large.jpg?1357766527',
        'name': "H-E-B Plus!",
        'ratings': '4.2/5',
        'location': '2508 E Riverside Dr, Austin, TX 78741',
        'description': 'H-E-B plus! in Austin at East Riverside & South Pleasant Valley includes Curbside Grocery Pickup, Grocery Home Delivery, pharmacy, gas station & car wash.',
        'phone': '(512) 448-3544'
}

store2 = {
        'img': 'http://media.culturemap.com/crop/c7/5c/800x700/Whole-Foods-Market-flagship-store-in-Austin_213727.jpg',
        'name': "Whole Foods Market",
        'ratings': '4.6/5',
        'location': '1525 N Lamar Blvd, Austin, TX 78703',
        'description': 'Eco-minded chain with natural & organic grocery items, housewares & other products.',
        'phone': '(512) 476-1206'
}

stores_list = [store0, store1, store2]


@stores.route("/")
def stores_overview():
    global stores_list

    items = []
    for val in stores_list:
        items.append([val['name'], val['img'], val['location'], val['ratings']])

    return render_template('stores/stores.html', items=items)


@stores.route("/<int:id>")
def stores_detail(id):
    global stores_list
    # TODO: Have the template be filled from a database in the future

    # ID 0-2 returns certain food page, else return error
    if id < first or id > last:
        abort(404)

    return render_template('stores/storesdetail.html', store=stores_list[id])
