from flask import Flask, render_template, redirect, flash, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .form import Formulario
import logging

app = Flask(__name__)
conexao = "sqlite:///tarefas.db"
app.config["SECRET_KEY"] = "amo-programar"
app.config["SQLALCHEMY_DATABASE_URI"] = conexao
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    hora = db.Column(db.String(2), nullable=False)

@app.route("/", methods=["GET", "POST"])
def index():
    form = Formulario()
    
    if request.method == "POST" and form.validate_on_submit():
        try:
            tarefa = Tarefas(nome=form.nome.data, hora=form.hora.data)
            db.session.add(tarefa)
            db.session.commit()
            flash('Tarefa adicionada com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao adicionar tarefa: {e}', 'danger')
            logging.exception("Erro ao adicionar tarefa")

    tarefas = Tarefas.query.all()
    logging.debug("Tarefas no banco de dados: %s", tarefas)

    return render_template("index.html", form=form, tarefas=tarefas)

@app.route("/editar_tarefa/<int:tarefa_id>", methods=["GET", "POST"])
def editar_tarefa(tarefa_id):
    tarefa = Tarefas.query.get_or_404(tarefa_id)
    form = Formulario(obj=tarefa)


    if form.validate_on_submit():
        pass

    if request.method == "POST":
        tarefa.nome = request.form["nome"]
        tarefa.hora = request.form["hora"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("editar_tarefa.html", tarefa=tarefa, form=form)

@app.route("/deletar_tarefa/<int:tarefa_id>", methods=["POST"])
def deletar_tarefa(tarefa_id):
    tarefa = Tarefas.query.get_or_404(tarefa_id)
    db.session.delete(tarefa)
    db.session.commit()
    flash('Tarefa deletada com sucesso!', 'success')
    return redirect(url_for("index"))
