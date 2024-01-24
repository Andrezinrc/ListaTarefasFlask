from flask import Flask, render_template, redirect, flash, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .form import Formulario  # Importa a classe Formulario do módulo form
import logging

app = Flask(__name__)  # Instancia o objeto Flask
conexao = "sqlite:///tarefas.db"
app.config["SECRET_KEY"] = "amo-programar"
app.config["SQLALCHEMY_DATABASE_URI"] = conexao
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)  # Instancia o objeto SQLAlchemy
migrate = Migrate(app, db)  # Instancia o objeto Migrate

class Tarefas(db.Model):
    # Define o modelo de dados para a tabela 'Tarefas' no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    hora = db.Column(db.String(2), nullable=False)

@app.route("/", methods=["GET", "POST"])
def index():
    form = Formulario()  # Cria uma instância do formulário

    if request.method == "POST" and form.validate_on_submit():
        try:
            # Tenta adicionar uma nova tarefa ao banco de dados
            tarefa = Tarefas(nome=form.nome.data, hora=form.hora.data)
            db.session.add(tarefa)
            db.session.commit()
            flash('Tarefa adicionada com sucesso!', 'success')
        except Exception as e:
            # Em caso de erro, exibe uma mensagem de erro e loga a exceção
            flash(f'Erro ao adicionar tarefa: {e}', 'danger')
            logging.exception("Erro ao adicionar tarefa")

    tarefas = Tarefas.query.all()  # Recupera todas as tarefas do banco de dados
    logging.debug("Tarefas no banco de dados: %s", tarefas)

    return render_template("index.html", form=form, tarefas=tarefas)

@app.route("/editar_tarefa/<int:tarefa_id>", methods=["GET", "POST"])
def editar_tarefa(tarefa_id):
    tarefa = Tarefas.query.get_or_404(tarefa_id)  # Obtém a tarefa do banco de dados ou retorna 404 se não existir
    form = Formulario(obj=tarefa)  # Preenche o formulário com os dados da tarefa

    if form.validate_on_submit():
        # A lógica para lidar com a submissão do formulário deve ser adicionada aqui
        pass

    if request.method == "POST":
        # Atualiza os dados da tarefa com base nos dados do formulário e salva no banco de dados
        tarefa.nome = request.form["nome"]
        tarefa.hora = request.form["hora"]
        db.session.commit()
        return redirect(url_for("index"))  # Redireciona para a página inicial após a edição
    return render_template("editar_tarefa.html", tarefa=tarefa, form=form)

@app.route("/deletar_tarefa/<int:tarefa_id>", methods=["POST"])
def deletar_tarefa(tarefa_id):
    tarefa = Tarefas.query.get_or_404(tarefa_id)  # Obtém a tarefa do banco de dados ou retorna 404 se não existir
    db.session.delete(tarefa)  # Remove a tarefa do banco de dados
    db.session.commit()
    return redirect(url_for("index"))  # Redireciona para a página inicial após a exclusão
