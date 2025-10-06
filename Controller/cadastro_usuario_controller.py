from flask import Blueprint, request, jsonify
from Model import cadastro_usuario
from Model.cadastro_usuario import *

cadastro_usuarios_blueprint = Blueprint('cadastro_usuarios', __name__)


@cadastro_usuarios_blueprint.route("/usuarios", methods=['GET'])
def listarUsuarios():
    try:
        usuarios,erro = cadastro_usuario.listarUsuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    

@cadastro_usuarios_blueprint.route("/usuarios/<int:id_usuario>", methods=['GET'])
def listarUsuarioId(id_usuario):
    try:
        usuario = cadastro_usuario.listarUsuarioId(id_usuario)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@cadastro_usuarios_blueprint.route("/usuarios", methods=['POST'])
def cadastrarUsuarios():
    dados = request.get_json(silent=True)   
    r = cadastrarUsuarios(dados)
    return jsonify({"message":"Usuário cadastrado com sucesso",
                    "statusDB" : r}), 200


@cadastro_usuarios_blueprint.route("/usuarios", methods=['GET'])
def listar_cargas():
    try:
        usuarios,erro = cadastro_usuario.listarUsuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@cadastro_usuarios_blueprint.route("/usuarios/<int:id_clientes>", methods=['PUT'])
def atualizar_clientes_id(id_clientes):
    dados = request.get_json(silent=True)
    try:
        atualizado = cadastro_usuario.atualizarUsuarioPorId(id_clientes, dados)
        if atualizado:
            return jsonify({'mensagem': 'Carga atualizada com sucesso'}), 200
        else:
            return jsonify({'erro': 'Carga não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@cadastro_usuarios_blueprint.route("/usuarios/<int:id_clientes>", methods=['DELETE'])
def apagar_clientes_id(id_clientes):
    try:
        deletado = cadastro_usuario.deletarUsuarioPorId(id_clientes)
        if deletado:
            return jsonify({'mensagem': 'Carga deletada com sucesso'}), 200
        else:
            return jsonify({'erro': 'Carga não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


