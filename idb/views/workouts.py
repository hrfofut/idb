from flask import Blueprint, render_template, abort
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


@workouts.route("/")
def workouts_overview():

    url = 'https://wger.de/api/v2/exercise/'
    data = {'page': 1, 'language': 2}
    headers = {'Authorization': 'Token 6df1fbfa2e24402b9a3e2451167d0cb4461a5b14'}
    req = requests.get(url=url, data=data, headers=headers)

    global workouts_list
    items = []
    for val in workouts_list:
        items.append([val['name'], val['img'], val['category'], val['muscle']])

    if req.status_code == requests.codes.ok:
        req_exercise_json = req.json()
        for exercise in req_exercise_json['results']:
            items.append([exercise['name'], 'https://i2.wp.com/lwvnaperville.org/wp-content/uploads/2017/06/placeholder.png?w=1500', str(exercise['category']), exercise['muscles']])

    return render_template('workouts/workouts.html', items=items)


@workouts.route("/<int:id>")
def workouts_detail(id):
    global workouts_list
# TODO: Have the template be filled from a database in the future

# ID 0-2 returns certain food page, else return error

    if id < first or id > last:
        abort(404)

    return render_template('workouts/workoutsdetail.html', workout=workouts_list[id])
