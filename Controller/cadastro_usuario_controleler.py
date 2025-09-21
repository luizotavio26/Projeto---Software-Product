from flask import Blueprint, request, jsonify
from Model import cadastro_usuario
from Model.cadastro_usuario import *

cadastro_usuarios = Blueprint('cadastro_usuarios', __name__)

app = cadastro_usuarios

@app.route("/listUsuarios", methods=['GET'])
def listUsuarios():
     response = listarUsuarios()
     return jsonify({"ListaUsuarios" : response}), 200

@app.route("/cadastroU", methods=['POST'])
def cadastro():
     dados = request.get_json(silent=True)   
     r = cadastraUsuarioDB(dados)
     return jsonify({"message":"Deu certo",
                     "statusDB" : r
                     }), 200
     
@app.route("/deleta", methods=['DELETE']) # isso deleta a tabela em si
def deletar():
     response = deletarTudo()
     return jsonify({"status" : response}), 200



