from flask import Blueprint, render_template, abort, g
from flask import current_app as app
import requests
import json

workouts = Blueprint('workouts', __name__)

first = 0
last = 2

bench_press = {
        'name': 'Bench Press',
        'img': 'http://cdn2.coachmag.co.uk/sites/coachmag/files/styles/insert_main_wide_image/public/2016/07/1-1-bench-press.jpg?itok=bJYGPFGO',
        'link': 'https://www.youtube.com/embed/9l9guSIjnZY',
        'category': 'Chest',
        'equipment': 'Barbell, Bench',
        'description': "Lay down on a bench, the bar should be directly above your eyes, the knees are somewhat angled and the feet are firmly on the floor. Concentrate, breath deeply and grab the bar more than shoulder wide. Bring it slowly down till it briefly touches your chest at the height of your nipples. Push the bar up.",
        'muscle': 'Pectoralis major, biceps brachii',
        'met': 5.0
}

push_up = {
        'name': 'Push Ups',
        'img': 'https://yurielkaim.com/wp-content/uploads/2013/07/Advanced-Push-up-Variations-Traditional-Push-up.jpg',
        'link': 'https://www.youtube.com/embed/_l3ySVKYVJ8',
        'category': 'Arms',
        'equipment': 'None',
        'description': "Start with your body streched, your hands are shoulder-wide appart on the ground. Push yourself off the ground till you strech your arms. The back is always straight and as well as the neck (always look to the ground). Lower yourself to the initial position and repeat.",
        'muscle': 'Anterior deltoid, pectoralis major, rectus abdominis, triceps brachii',
        'met': 3.8
}

running = {
        'name': 'Running',
        'img': 'http://www.runguides.com/assets/running-icon.svg',
        'link': 'https://www.youtube.com/embed/lCpotGr0TB4',
        'category': 'Legs',
        'equipment': 'None',
        'description': "Running or jogging outside in a park, on the tracks,...",
        'muscle': 'Hamstrings, quadriceps, hip flexors, gluteals, calf muscles',
        'met': 7.0
}

workouts_list = [bench_press, push_up, running]


def get_exercise_images():
    exercise_images = getattr(g, '_exercise_images', None)
    if exercise_images is None:
        g._exercise_images = {}
        url = 'https://wger.de/api/v2/exerciseimage/'
        data = {'page': 1, 'limit': 1000}
        headers = {'Authorization': 'Token ' + app.config['WGER_KEY']}
        req = requests.get(url=url, data=data, headers=headers)
        if req.status_code == requests.codes.ok:
            req_images_json = req.json()
            for image in req_images_json['results']:
                g._exercise_images[image['exercise']] = image['image']
    return g._exercise_images


def get_categories():
    categories = getattr(g, '_categories', None)
    if categories is None:
        g._categories = {}
        url = 'https://wger.de/api/v2/exercisecategory/'
        data = {'page': 1, 'limit': 1000}
        headers = {'Authorization': 'Token ' + app.config['WGER_KEY']}
        req = requests.get(url=url, data=data, headers=headers)
        if req.status_code == requests.codes.ok:
            req_categories_json = req.json()
            for category in req_categories_json['results']:
                g._categories[category['id']] = category['name']
    return g._categories


def get_muscles():
    muscles = getattr(g, '_muscles', None)
    if muscles is None:
        g._muscles = {}
        url = 'https://wger.de/api/v2/muscle/'
        data = {'page': 1, 'limit': 1000}
        headers = {'Authorization': 'Token ' + app.config['WGER_KEY']}
        req = requests.get(url=url, data=data, headers=headers)
        if req.status_code == requests.codes.ok:
            req_muscles_json = req.json()
            for muscle in req_muscles_json['results']:
                g._muscles[muscle['id']] = muscle['name']
        return g._muscles


def get_equipments():
    equipments = getattr(g, '_equipments', None)
    if equipments is None:
        g._equipments = {}
        url = 'https://wger.de/api/v2/equipment/'
        data = {'page': 1, 'limit': 1000}
        headers = {'Authorization': 'Token ' + app.config['WGER_KEY']}
        req = requests.get(url=url, data=data, headers=headers)
        if req.status_code == requests.codes.ok:
            req_equipments_json = req.json()
            for equipment in req_equipments_json['results']:
                g._equipments[equipment['id']] = equipment['name']
    return g._equipments


def get_exercises():
    ...


@workouts.route("/")
def workouts_overview():
    global workouts_list, first, last
    items = []
    for val in workouts_list:
        items.append([val['name'], val['img'], val['category'], val['muscle']])

    images = get_exercise_images()
    categories = get_categories()
    muscles = get_muscles()
    equipments = get_equipments()
    exercises = get_exercises()

    url = 'https://wger.de/api/v2/exercise/'
    data = {'page': 1, 'language': 2}
    headers = {'Authorization': 'Token ' + app.config['WGER_KEY']}
    print(app.config['WGER_KEY'])
    req = requests.get(url=url, data=data, headers=headers)
    if req.status_code == requests.codes.ok:
        req_exercise_json = req.json()
        for exercise in req_exercise_json['results']:
            items.append([exercise['name'], 'https://i2.wp.com/lwvnaperville.org/wp-content/uploads/2017/06/placeholder.png?w=1500', str(exercise['category']), exercise['muscles']])
            exer_a = {
                    'name': exercise['name'],
                    'img': 'https://i2.wp.com/lwvnaperville.org/wp-content/uploads/2017/06/placeholder.png?w=1500',
                    'link': 'None',
                    'category': exercise['category'],
                    'equipment': 'placeholder',
                    'description': exercise['description'],
                    'muscle': 'placeholder',
                    'met': 0.0
                    }
            workouts_list.append(exer_a)
            last += 1

    return render_template('workouts/workouts.html', items=items)


@workouts.route("/<int:id>")
def workouts_detail(id):
    global workouts_list
# TODO: Have the template be filled from a database in the future

# ID 0-2 returns certain food page, else return error

    if id < first or id > last:
        abort(404)

    return render_template('workouts/workoutsdetail.html', workout=workouts_list[id])
