from flask import Blueprint, request, jsonify
from Model import cadastro_veiculos
from Model.cadastro_veiculos import *

cadastro_veiculos_blueprint = Blueprint('cadastro_veiculos', __name__)


@cadastro_veiculos_blueprint.route("/veiculos", methods=['GET'])
def listarVeiculos():
    try:
        veiculos,erro = cadastro_veiculos.listarVeiculos()
        return jsonify(veiculos), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    

@cadastro_veiculos_blueprint.route("/veiculos/<int:id_veiculo>", methods=['GET'])
def listarVeiculoId(id_veiculo):
    try:
        veiculos = cadastro_veiculos.listarUsuarioId(id_veiculo)
        if veiculos:
            return jsonify(veiculos), 200
        else:
            return jsonify({'erro': 'Veiculo não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@cadastro_veiculos_blueprint.route("/veiculos", methods=['POST'])
def cadastrarVeiculos():
    dados = request.get_json(silent=True)   
    r = cadastrarVeiculos(dados)
    return jsonify({"message":"Veículo cadastrado com sucesso",
                    "statusDB" : r}), 200


@cadastro_veiculos_blueprint.route("/veiculos", methods=['GET'])
def listar_cargas():
    try:
        veiculos,erro = cadastro_veiculos.listarVeiculos()
        return jsonify(veiculos), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@cadastro_veiculos_blueprint.route("/veiculos/<int:id_veiculos>", methods=['PUT'])
def atualizar_veiculos_id(id_veiculos):
    dados = request.get_json(silent=True)
    try:
        atualizado = cadastro_veiculos.atualizarVeiculoPorId(id_veiculos, dados)
        if atualizado:
            return jsonify({'mensagem': 'Veículo atualizado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Veículo não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@cadastro_veiculos_blueprint.route("/veiculos/<int:id_veiculos>", methods=['DELETE'])
def apagar_veiculos_id(id_veiculos):
    try:
        deletado = cadastro_veiculos.deletarVeiculosPorId(id_veiculos)
        if deletado:
            return jsonify({'mensagem': 'Veículo deletado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Veículo não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


