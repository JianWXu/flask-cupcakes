from flask_wtf import FlaskForm
from wtforms import StringField, FloatField


class AddCupcakeForm(FlaskForm):

    flavor = StringField("flavor")
    size = StringField("size")
    rating = FloatField("rating")
    image = StringField("image")
