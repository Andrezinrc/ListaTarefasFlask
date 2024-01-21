from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class Formulario(FlaskForm):
    nome = StringField('nome', validators=[DataRequired()])
    hora = StringField('hora', validators=[DataRequired()])
