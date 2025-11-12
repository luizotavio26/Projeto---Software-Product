from flask import Blueprint, request, jsonify
from model import user_model
from model.user_model import *

cadastro_usuario_blueprint = Blueprint('cadastro_usuario', __name__)

@cadastro_usuario_blueprint.route("/usuario", methods=['GET'])
def listarUsuarios():
    try:
        usuarios = user_model.getUsuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        print(f"Erro ao listar usuarios: {e}") 
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/usuario", methods=['POST'])
def cadastrarUsuarios():
    dados = request.get_json(silent=True)   
    r, erro = user_model.postUsuarios(dados)
    if erro:
        return jsonify({'erro': erro}), 400
        
    return jsonify({"message":"Usuário cadastrado com sucesso", "statusDB" : r}), 201

@cadastro_usuario_blueprint.route("/usuario/<int:id_usuario>", methods=['PUT'])
def atualizarUsuariosId(id_usuario):
    dados = request.get_json(silent=True)
    try:
        atualizado = user_model.putUsuarioPorId(id_usuario, dados)
        if atualizado:
            return jsonify({'mensagem': 'Usuario atualizado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Usuario não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@cadastro_usuario_blueprint.route("/usuario/<int:id_usuario>", methods=['DELETE'])
def apagarUsuariosId(id_usuario):
    try:
        deletado = user_model.deleteUsuarioPorId(id_usuario)
        if deletado:
            return jsonify({'mensagem': 'Usuario deletadO com sucesso'}), 200
        else:
            return jsonify({'erro': 'Usuario não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@cadastro_usuario_blueprint.route("/usuario/login", methods=['POST'])
def login():
    dados = request.get_json()    
    try:
        response = user_model.verificaSenhaEmail(dados)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/usuario/mudancasenha", methods=['POST'])
def mudarSenha():
    return jsonify({"message": "redirecionar senha aqui"})
