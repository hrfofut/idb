import json
import requests

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from idb.models import Workouts

file_on = 1
path = "resources/metdata" + str(file_on) + "word"
f = open(path, 'r')
for line in f:
    print (line)
    words = iter(line.split())

    workout_id = int(next(words))
    # print("id: "+ str(workout_id))

    met_val = float(next(words))
    # print("met: "+ str(met_val))

    category = next(words)
    # print("category: "+ str(category))

    index = 0
    name = ''
    desc = ''
    on_desc = False
    for word in words:
        # print(str(index)+": "+ word)
        index += 1
        if '(' in word:
            on_desc = True

        if on_desc:
            desc += word + ' '
        else:
            if ',' in word:
                on_desc = True
            name += word + ' '

    print("name: " + name)
    print("desc: " + desc)
