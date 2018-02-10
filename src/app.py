from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/<name>")
def splash(name):
    return render_template('splash.html', name=name)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/foods")
def food():
    return render_template('foods/food.html')


@app.route("/foods/<id>")
def fooddetail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('foods/fooddetail.html')


@app.route("/workouts")
def workouts():
    return render_template('workouts/workouts.html')


@app.route("/workouts/<id>")
def workoutsdetail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('workouts/workoutsdetail.html')


@app.route("/gyms")
def gyms():
    return render_template('gyms/gyms.html')


@app.route("/gyms/<id>")
def gymsdetail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('gyms/gymsdetail.html')


@app.route("/stores")
def stores():
    return render_template('stores/stores.html')


@app.route("/stores/<id>")
def storesdetail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('stores/storesdetail.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
