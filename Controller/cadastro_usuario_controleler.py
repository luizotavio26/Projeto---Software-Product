from flask import Blueprint, request, jsonify
from Model import cadastro_usuario
from Model.cadastro_usuario import *

cadastro_usuarios = Blueprint('cadastro_usuarios', __name__)

app = cadastro_usuarios

@app.route("/usuarios", methods=['GET'])
def listUsuarios():
     response = listarUsuarios()
     return jsonify({"ListaUsuarios" : response}), 200

@app.route("/usuarios/<int:id>", methods=['GET'])
def listarUsuarioPorId(id):
     response = listarUsuarioId(id)
     return jsonify({"Usuario" : response}), 200

@app.route("/usuarios", methods=['POST'])
def cadastro():
     dados = request.get_json(silent=True)   
     r = cadastraUsuarioDB(dados)
     return jsonify({"message":"Deu certo",
                     "statusDB" : r
                     }), 200

@app.route("/usuarios/<int:id>", methods=['PUT'])
def atualizar_usuario(id):
    dados = request.get_json(silent=True)
    response = atualizaUsuarioPorId(id, dados)
    return jsonify({"status": response}), 200

@app.route("/usuarios/<int:id>", methods=['DELETE'])
def deletar_usuario(id):
    response = deletaUsuarioPorId(id)
    return jsonify({"status": response}), 200
