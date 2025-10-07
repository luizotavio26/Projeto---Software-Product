from flask import Blueprint, request, jsonify
from Model import cadastro_veiculos
from Model.cadastro_veiculos import *

cadastro_veiculos_blueprint = Blueprint('cadastro_veiculos', __name__)


@cadastro_veiculos_blueprint.route("/veiculos", methods=['GET'])
def listarVeiculos():
    try:
        veiculos,erro = cadastro_veiculos.getVeiculos()
        return jsonify(veiculos), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'erro': str(e)}), 500
    

@cadastro_veiculos_blueprint.route("/veiculos/<int:id_veiculo>", methods=['GET'])
def listarVeiculoId(id_veiculo):
    try:
        veiculos = cadastro_veiculos.getVeiculosId(id_veiculo)
        if veiculos:
            return jsonify(veiculos), 200
        else:
            return jsonify({'erro': 'Veiculo não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@cadastro_veiculos_blueprint.route("/veiculos", methods=['POST'])
def cadastrar_veiculo():
    try:
        dados = request.get_json(silent=True)
        mensagem = cadastro_veiculos.postVeiculos(dados)
        return jsonify({"message": mensagem}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@cadastro_veiculos_blueprint.route("/veiculos/<int:id_veiculo>", methods=['PUT'])
def atualizar_veiculos_id(id_veiculo):
    dados = request.get_json(silent=True)
    try:
        atualizado = cadastro_veiculos.putVeiculoPorId(id_veiculo, dados)
        if atualizado:
            return jsonify({'mensagem': 'Veículo atualizado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Veículo não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@cadastro_veiculos_blueprint.route("/veiculos/<int:id_veiculo>", methods=['DELETE'])
def apagar_veiculos_id(id_veiculo):
    try:
        deletado = cadastro_veiculos.deleteVeiculoPorId(id_veiculo)
        if deletado:
            return jsonify({'mensagem': 'Veículo deletado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Veículo não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


