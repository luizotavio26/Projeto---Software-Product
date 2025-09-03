from flask import Flask, Blueprint
from model.bancoS import versaoBD , consulta
from sqlalchemy import create_engine, text 
import os



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
     
