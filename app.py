from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

# Modelo da Tabela
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_vencimento = db.Column(db.String(10))
    prioridade = db.Column(db.String(10))
    status = db.Column(db.String(20), default="pendente")

# Criar banco caso não exista
with app.app_context():
    db.create_all()


# ------------------------------
# ROTA PRINCIPAL: LISTAR TAREFAS
# ------------------------------
@app.route("/")
def index():
    tarefas = Tarefa.query.all()
    return render_template("index.html", tarefas=tarefas)


# ------------------------------
# CRIAR TAREFA
# ------------------------------
@app.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        nova = Tarefa(
            titulo=request.form["titulo"],
            descricao=request.form["descricao"],
            data_vencimento=request.form["data_vencimento"],
            prioridade=request.form["prioridade"],
            status="pendente"
        )
        db.session.add(nova)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("criar.html")


# ------------------------------
# EDITAR TAREFA
# ------------------------------
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    tarefa = Tarefa.query.get_or_404(id)

    if request.method == "POST":
        tarefa.titulo = request.form["titulo"]
        tarefa.descricao = request.form["descricao"]
        tarefa.data_vencimento = request.form["data_vencimento"]
        tarefa.prioridade = request.form["prioridade"]
        tarefa.status = request.form["status"]

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("editar.html", tarefa=tarefa)


# ------------------------------
# DELETAR TAREFA
# ------------------------------
@app.route("/delete/<int:id>")
def delete(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
