from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os
import psycopg2
from forms import AddCupcakeForm

load_dotenv(override=True)
pw = os.getenv("pw")
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{pw}@localhost/cupcakes'

app.app_context().push()


app.config['SECRET_KEY'] = "HELLO123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/api/cupcakes')
def all_cupcakes():
    cupcakes = Cupcake.query.all()
    cupcake = [c.serialize() for c in cupcakes]
    return jsonify(cupcakes=cupcake)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    cupcakes = Cupcake.query.all()
    form = AddCupcakeForm()
    if form.validate_on_submit():
        flavor = form.flavor.data
        size = form.size.data
        rating = form.rating.data
        image = form.image.data
        new_cupcake = Cupcake(flavor=flavor, size=size,
                              rating=rating, image=image)
        db.session.add(new_cupcake)
        db.session.commit()
        return redirect("/")
    else:
        return render_template('index.html', cupcakes=cupcakes, form=form)


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")


@app.route('/', methods=["GET", "POST"])
def index_page():
    cupcakes = Cupcake.query.all()
    form = AddCupcakeForm()
    return render_template('index.html', cupcakes=cupcakes, form=form)
