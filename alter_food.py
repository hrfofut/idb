from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from idb.models import Food

# Next three lines create the app and then load config from the instance folder.
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('default_config.py')
app.config.from_pyfile('application.py', silent=True)

app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
food_list = db.session.query(Food).all()
aisles = set()
x = 0

# Food Aile Collision Dict

aisle_d = {
'Online': 1,
'Cereal': 2,
'Condiments': 4,
'Dried Fruits': 8,
'Not in Grocery Store/Homemade': 16,
'Bakery/Bread': 32,
'Savory Snacks': 64,
'Beverages': 128,
'Milk, Eggs, Other Dairy': 256,
'Canned and Jarred': 512,
'Oil, Vinegar, Salad Dressing': 1024,
'Nut butters, Jams, and Honey': 2048,
'Produce': 4096,
'Alcoholic Beverages': 8192,
'Health Foods': 16384,
'Cheese': 32768,
'Tea and Coffee': 65536,
'Sweet Snacks': 131072,
'Bread': 262144,
'Meat': 524288,
'Baking': 1048576,
'Seafood': 2097152,
'Refrigerated': 4194304,
'Frozen': 8388608,
'Pasta and Rice': 16777216,
'Gourmet': 33554432,
'Ethnic Foods': 67108864,
'Spices and Seasonings': 134217728,
'Nuts': 268435456,
'Gluten Free': 536870912
}
large = 0
for food in food_list:
    x += 1
    s = food.aisle
    s_list = s.split(';')
    i = 0
    for aisle in s_list:
        aisles.add(aisle)
        i += aisle_d[aisle]
    print(format(x, '04d') + ": " + s + " => " + str(s_list) + " will become " + format(i, '#030b'))
    large = max(large, len(s_list))
print(str(aisles))
print(str(len(aisles)))
print("largest " + str(large))
# print("{")
# i = 1
# for aisle in aisles:
#     print ("\'"+aisle+"\'"+": "+str(i)+",")
#     i*=2
# print("}")

# place details
#     db.session.add(gym)
# db.session.commit()
