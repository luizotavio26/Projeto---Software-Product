from flask import Blueprint, request, jsonify
from Model import manifesto_carga_model
from Model.manifesto_carga_model import CargaNaoEncontrada
from config import db

manifesto_cargas_blueprint = Blueprint('manifesto_carga', __name__)


@manifesto_cargas_blueprint.route("/conexao", methods=['GET'])
def testa_conexao():
    return jsonify({"message":"conexao com api"}), 200

		
@manifesto_cargas_blueprint.route('/cargas', methods=['POST'])
def cria_cargas():
    dados = request.get_json()
    try:
        novo_carga, erro = manifesto_carga_model.create_carga(dados)
        if erro:
            return jsonify({'erro': erro}), 400
        return jsonify(novo_carga), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
 

@manifesto_cargas_blueprint.route('/cargas', methods=['GET'])
def le_cargas():
    try:
        cargas,erro = manifesto_carga_model.read_todas_cargas()
        return jsonify(cargas), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@manifesto_cargas_blueprint.route('/cargas/<int:id_cargas>', methods =['GET'])
def le_cargas_id(id_cargas):
    try:
        carga = manifesto_carga_model.read_cargas_id(id_cargas)
        return jsonify(carga), 200
    except CargaNaoEncontrada():
        return jsonify({'erro': 'Carga não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@manifesto_cargas_blueprint.route('/cargas/<int:id_cargas>', methods=['PUT'])
def atualiza_cargas(id_cargas):
    dados = request.get_json()
    try:
        atualizado = manifesto_carga_model.update_carga(id_cargas, dados)
        if atualizado:
            return jsonify(manifesto_carga_model.read_cargas_id(id_cargas)), 200
        else:
            return jsonify({'erro': 'Carga não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
                

@manifesto_cargas_blueprint.route('/cargas/<int:id_cargas>', methods = ['DELETE'])
def deleta_cargas_id(id_cargas):
    try:
        deletado = manifesto_carga_model.delete_carga_id(id_cargas)
        if deletado:
            return jsonify({'mensagem': 'Carga deletada com sucesso'}), 200
        else:
            return jsonify({'erro': 'Carga não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

    
@manifesto_cargas_blueprint.route('/cargas', methods = ['DELETE'])
def deleta_cargas():
    try:
        deletado, erro = manifesto_carga_model.delete_todas_cargas()
        if erro:
            return jsonify({'erro': erro}), 400
        return jsonify({'mensagem': 'Todos as cargas foram deletados com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500