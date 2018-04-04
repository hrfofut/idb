import json
import requests

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from idb.models import Workouts, Images
# Next three lines create the app and then load config from the instance folder.


def parse_file(num):
    results = []
    file_on = num
    path = "resources/metdata" + str(file_on) + "word"
    f = open(path, 'r')
    for line in f:
        # print (line)
        words = iter(line.split())

        workout_id = int(next(words))
        # print("id: "+ str(workout_id))

        met = float(next(words))
        # print("met: "+ str(met))
        category = ''
        for n in range(0, file_on):
            category += next(words) + ' '
        # print("category: "+ str(category))
        category = category.rstrip(' ')
        # cat_set.add(category) #later we can count categories.
        index = 0
        name = ''
        desc = ''
        on_desc = False
        for word in words:
            # print(str(index)+": "+ word)
            index += 1
            if '(' in word and ')' not in word:  # Make sure to exclude (Weight)
                on_desc = True

            if on_desc:
                desc += word + ' '
            else:
                if ',' in word:
                    on_desc = True
                name += word + ' '

        name = name.replace(',', '')  # Remove any commas.

        name = name.rstrip(' ')
        desc = desc.rstrip(' ')
        # print("name: " + name)
        # print("desc: " + desc)
        di = {'id': workout_id, 'met': met, 'category': category, 'name': name, 'description': desc}
        if len(name) < 50:
            results.append(di)

    return results


if __name__ == '__main__':
    # cat_set = set()
    # init the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('default_config.py')
    app.config.from_pyfile('application.py', silent=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # init the database
    db = SQLAlchemy(app)
    cid_match = {'miscellaneous': 0, 'dancing': 1, 'conditioning exercise': 2, 'home repair': 3, 'home activities': 4, 'walking': 5, 'fishing and hunting': 6, 'bicycling': 7, 'running': 8, 'lawn and garden': 9, 'winter activities': 10, 'music playing': 11, 'sports': 12, 'water activities': 13, 'occupation': 14}
    # begin parsing
    lidi = parse_file(1)
    lidi += parse_file(2)
    lidi += parse_file(3)
    # form search request
    CSE_URI = 'https://www.googleapis.com/customsearch/v1'
    params = {'q': 'INVALID', 'num': 3, 'start': 1, 'imgSize': 'medium', 'searchType': 'image', 'filetype': 'jpg', 'key': app.config['PLACE_KEY'], 'cx': app.config['CSE_ID']}
    params['safe'] = 'high'  # Safe search is important.
    # the search params are all prepared except for query.

    for workout in lidi:  # Iterate over each workout inside.
        params['q'] = workout['name'] + ' ' + workout['description']
        search_response = requests.get(url=CSE_URI, params=params).json()
        # print(json.dumps(search_response, indent=4, sort_keys=True)) #Neatly prints the json for viewing pleasure.

        # Check our results.
        print(params['q'])
        link = ''
        if 'items' in search_response:
            for item in search_response['items']:
                link = item['link']
                print(link)
                if len(link) < 255:
                    workout['img'] = link
                    workout['cid'] = cid_match[workout['category']]
                    break
                else:
                    link = ''
            if link == '':
                print("no valid img found for ID: " + str(workout['id']) + ", invalidating.")
                workout['id'] = -1
        else:
            # print(json.dumps(search_response, indent=4, sort_keys=True))
            print(workout)
            print("img not found for ID: " + str(workout['id']) + ", invalidating.")
            workout['id'] = -1

        if workout['id'] != -1:  # if valid we add to db
            # print(workout)
            # def __init__(self, id, name, img, link, category, equipment, description, muscle, met, cid):
            workout_row = Workouts(**workout)  # unpack the dict and init.
            # db.session.add(workout_row)
            # db.session.commit()#probably don't need to commit after every add.

        # For now, lets just hotlink. We have the image url in link, so we can change this later.

    # not dynamic, but lets do it anyways. First prints a dict for the categories, second prints sql insert.
    # print("{")
    # i = 0
    # for cat in cat_set:
    #     print ("\'"+cat+"\'"+": "+str(i)+",")
    #     i+=1
    # print("}")
    # print("INSERT INTO categories VALUES")
    # i = 0
    # for cat in cat_set:
    #     print ("("+str(i)+", \'"+cat+"\'),")
    #     i+=1

"""
{
'miscellaneous': 0,
'dancing': 1,
'conditioning exercise': 2,
'home repair': 3,
'home activities': 4,
'walking': 5,
'fishing and hunting': 6,
'bicycling': 7,
'running': 8,
'lawn and garden': 9,
'winter activities': 10,
'music playing': 11,
'sports': 12,
'water activities': 13,
'occupation': 14
}

INSERT INTO categories VALUES
(0, 'miscellaneous'),
(1, 'dancing'),
(2, 'conditioning exercise'),
(3, 'home repair'),
(4, 'home activities'),
(5, 'walking'),
(6, 'fishing and hunting'),
(7, 'bicycling'),
(8, 'running'),
(9, 'lawn and garden'),
(10, 'winter activities'),
(11, 'music playing'),
(12, 'sports'),
(13, 'water activities'),
(14, 'occupation')

"""
