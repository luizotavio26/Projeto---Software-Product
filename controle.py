from flask import Flask, Blueprint
from bancoS import versaoBD , consulta
from sqlalchemy import create_engine, text 
import os
from bancoS import Cliente , jsonify


linkBD = os.getenv('DB_URL')
url = Blueprint("run", __name__)


@url.route('/')
def index():
     return "Hello, World!"


@url.route('/v', methods=['GET'])
def v():
     if not linkBD:
          return {"error": "DB_URL não configurado"}, 500
     try:
          return versaoBD(linkBD)
     except Exception as e:
          return {"error": str(e)}, 500


@url.route('/c', methods=['GET'])
def c():
     if not linkBD:
          return {"error": "DB_URL não configurado"}, 500
     try:
          return consulta(linkBD)
     except Exception as e:
          return {"error": str(e)}, 500
     
@url.route('/c2', methods=['GET'])
def consulta_cliente():
     clientes = Cliente.query.all()
     resultado = []
     for cliente in clientes:
          item = {"id": cliente.id, "nome": cliente.nome}
          # Adiciona idade se existir
          if hasattr(cliente, "idade"):
               item["idade"] = cliente.idade
          resultado.append(item)
     return jsonify(resultado)