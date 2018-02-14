from flask import Blueprint, render_template

gyms = Blueprint('gyms', __name__)

first = 0
last = 2

gym0 = {
        'img': 'https://www.castlehillfitness.com/wp-content/uploads/2018/01/Castle-Hill-Fitness-Downtown-Lamar-Outside.jpg',
        'name': 'Castle Hill Fitness',
        'ratings': '4.7/5',
        'location': '1112 N Lamar Blvd, Austin, TX',
        'pricing': '$89/month or $139/month memberships'
}

gym1 = {
        'img': 'https://www.goldsgym.com/austinsouthcentraltx/wp-content/uploads/sites/96/2017/11/DTB_8990.jpg',
        'name': "Gold's gyms",
        'ratings': '3.5/5',
        'location': '1701 W Ben White Blvd Suite 165, Austin, TX 78704',
        'pricing': '$40-$100/month'
}

gym2 = {
        'img': 'https://9968c6ef49dc043599a5-e151928c3d69a5a4a2d07a8bf3efa90a.ssl.cf2.rackcdn.com/28263.jpg',
        'name': 'Hyde Park Gym',
        'ratings': '4.9/5',
        'location': '4125 Guadalupe St, Austin, TX 78751',
        'pricing': '$49.50/month'
}

gyms_list = [gym0, gym1, gym2]


@gyms.route("/")
def gyms_overview():
    global gyms_list

    items = []
    for val in gyms_list:
        items.append([val['name'], val['img'], val['ratings'], val['pricing']])

    return render_template('gyms/gyms.html')


@gyms.route("/<int:id>")
def gyms_detail(id):
    global gyms_list
    # TODO: Have the template be filled from a database in the future

# ID 0-2 returns certain food page, else return error
    if id < first or id > last:
        return render_template('errors/404.html'), 404

    return render_template('gyms/gymsdetail.html', gym=gyms_list[id])
