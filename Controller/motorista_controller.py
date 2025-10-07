from flask import Blueprint, request, jsonify
from Model import motorista_model
from Model.motorista_model import *
from config import db

motoristas_blueprint = Blueprint('motorista', __name__)

# Create
@motoristas_blueprint.route("/motoristas", methods=['POST'])
def criar_motoristas():
    dados = request.get_json()
    try:
        novo_motorista, erro = motorista_model.create_motorista(dados)
        if erro:
            return jsonify({"erro": erro}), 400
        else:
            return jsonify(novo_motorista), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Read Tudo
@motoristas_blueprint.route("/motoristas", methods=['GET'])
def listar_motoristas():
    try:
        motoristas,erro = motorista_model.read_todos_motorista()
        return jsonify(motoristas), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# Read por id
@motoristas_blueprint.route("/motoristas/<int:id_motorista>", methods=['GET'])
def le_motoristas_id(id_motorista):
    try:
        motorista = motorista_model.read_motorista_id(id_motorista)
        return jsonify(motorista), 200
    except MotoristaNaoEncontrado():
        return jsonify({"erro": "Motorista não encontrado"}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# Update Cargas
@motoristas_blueprint.route("/motoristas/<int:id_motorista>", methods=['PUT'])
def atualizar_motoristas(id_motorista):
    dados = request.get_json()
    try:
        atualizado = motorista_model.update_motorista(id_motorista, dados)
        if atualizado:
            return jsonify(motorista_model.read_motorista_id(id_motorista)), 200
        else:
            return jsonify({'erro': 'Motorista não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@motoristas_blueprint.route("/motoristas/<int:id_motorista>", methods=['DELETE'])
def apagar_motoristas_id(id_motorista):
    try:
        deletado = motorista_model.delete_motorista_id(id_motorista)
        if deletado:
            return jsonify({'mensagem': 'Motorista deletado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Motorista não encontrado'}), 404
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@motoristas_blueprint.route("/motoristas", methods=['DELETE'])
def deletar_motorista():
    try:
        deletado, erro = motorista_model.delete_todos_motoristas()
        if erro:
            return jsonify({'erro': erro}), 400
        return jsonify({'mensagem': 'Todos os motoristas foram deletados com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500



