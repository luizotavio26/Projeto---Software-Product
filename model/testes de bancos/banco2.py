from flask import Flask, jsonify
from sqlalchemy import create_engine, text 
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
url = os.getenv("DB_URL")

engine = create_engine(url)

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # recomendado para evitar warning

db = SQLAlchemy(app)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    
class Produto(db.Model):
     __tablename_ = 'produtos'
     id = db.Column(db.Integer, primary_key=True)
     nome = db.Column(db.String(50))
     preco = db.Column(db.Float)
     estoque = db.Column(db.Integer)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/version', methods=['GET'])
def get_version():
     con = engine.connect()
     result = con.execute(text("SELECT version();"))
     version = result.fetchone()[0]
     con.close()
     return jsonify({"version": version})

@app.route('/clientes', methods=['GET'])
def get_clientes():
     con = engine.connect()
     result = con.execute(text("SELECT * FROM clientes"))
     cliente = []
     for row in result.fetchall():
           cliente.append({"id": row[0], "nome": row[1], "idade": row[2]})
     con.close()
     return jsonify(cliente)

@app.route('/clientes2', methods=['GET'])
def get_clientes2():
     clientes = Cliente.query.all()
     cliente = []
     for row in clientes:
           cliente.append({"id": row.id, "nome": row.nome})
     return jsonify(cliente)


if __name__ == "__main__":
    app.run(debug=True)
