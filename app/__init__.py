from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .form import Formulario

app = Flask(__name__)
conexao = "sqlite:///tarefas.db"

app.config["SECRET_KEY"] = "amo-programar"
app.config["SQLALCHEMY_DATABASE_URI"] = conexao

db = SQLAlchemy(app) 

migrate = Migrate(app, db)

class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    hora = db.Column(db.Integer, nullable=False)

@app.route("/", methods=["GET", "POST"])
def index():
    form = Formulario()

    if form.validate_on_submit():
        flash('Tarefa adicionada com sucesso!', 'success')
      
    if request.method == "POST":
        tarefa = Tarefas(nome=request.form["nome"], hora=request.form["hora"])
        db.session.add(tarefa)
        db.session.commit()
        return render_template("index.html", form=form, tarefa=tarefa)

    return render_template("index.html", form=form)
