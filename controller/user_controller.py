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

@cadastro_usuario_blueprint.route("/usuario/<int:id_usuario>", methods=['GET'])
def listarUsuarioId(id_usuario):
    try:
        usuario = user_model.getUsuarioId(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/usuario", methods=['POST'])
def cadastrarUsuarios():
    dados = request.get_json(silent=True)   
    r, erro = user_model.postUsuario(dados)
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
            return jsonify({'mensagem': 'Usuario deletado com sucesso'}), 200
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

@cadastro_usuario_blueprint.route("/usuario/mudancaSenha", methods=['PUT'])
def mudarSenha():
    dados = request.get_json()
    try:
        response = user_model.esqueciSenha(dados)
        return jsonify(response), 200
    except Exception as e:
        return({'erro': str(e)}), 500

# --------------------------------- DASHBOARD ----------------------------------
@cadastro_usuario_blueprint.route("/dashboard/cargasCadastradas/<int:id_usuario>", methods=['GET'])
def cargas_cadastradas(id_usuario):
    try:
        usuario = user_model.cargasCadastradas(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/dashboard/motoristasCadastrados/<int:id_usuario>", methods=['GET'])
def motoristas_cadastradas(id_usuario):
    try:
        usuario = user_model.motoristasCadastrados(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/dashboard/clientesCadastrados/<int:id_usuario>", methods=['GET'])
def clientes_cadastradas(id_usuario):
    try:
        usuario = user_model.clientesCadastrados(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/dashboard/veiculosCadastrados/<int:id_usuario>", methods=['GET'])
def veiculos_cadastradas(id_usuario):
    try:
        usuario = user_model.veiculosCadastrados(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cadastro_usuario_blueprint.route("/dashboard/totaisCargas/<int:id_usuario>", methods=["GET"])
def totais_cargas(id_usuario):
    try:
        totais = user_model.totaisCargas(id_usuario)
        return jsonify(totais), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cadastro_usuario_blueprint.route("/dashboard/faturamento/<int:id_usuario>", methods=["GET"])
def faturamento(id_usuario):
    try:
        faturamento = user_model.faturamento(id_usuario)
        return jsonify(faturamento), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500