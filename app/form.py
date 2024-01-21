from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class Formulario(FlaskForm):
    nome = StringField('nome', validators=[DataRequired()])
    hora = IntegerField('hora', validators=[DataRequired(), NumberRange(min=0)])
