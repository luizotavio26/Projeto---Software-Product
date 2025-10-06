from flask import Blueprint, request, jsonify
from Model import cadastro_cliente_model
from Model.cadastro_cliente_model import *

cadastro_clientes_blueprint = Blueprint('cadastro_clientes', __name__)


@cadastro_clientes_blueprint.route("/clientes", methods=['GET'])
def listarClientes():
    try:
        clientes = cadastro_cliente_model.getClientes()
        return jsonify(clientes), 200
    except Exception as e:
        print(f"Erro ao listar clientes: {e}") 
        return jsonify({'erro': str(e)}), 500
    

@cadastro_clientes_blueprint.route("/clientes/<int:id_cliente>", methods=['GET'])
def listarClienteId(id_cliente):
    try:
        cliente = cadastro_cliente_model.getClienteId(id_cliente)
        if cliente:
            return jsonify(cliente), 200
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@cadastro_clientes_blueprint.route("/clientes", methods=['POST'])
def cadastrarClientes():
    dados = request.get_json(silent=True)   
    r, erro = cadastro_cliente_model.postClientes(dados)
    if erro:
        return jsonify({'erro': erro}), 400
        
    return jsonify({"message":"Usuário cadastrado com sucesso", "statusDB" : r}), 201


@cadastro_clientes_blueprint.route("/clientes/<int:id_clientes>", methods=['PUT'])
def atualizarClientesId(id_clientes):
    dados = request.get_json(silent=True)
    try:
        atualizado = cadastro_cliente_model.putClientePorId(id_clientes, dados)
        if atualizado:
            return jsonify({'mensagem': 'Carga atualizada com sucesso'}), 200
        else:
            return jsonify({'erro': 'Carga não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@cadastro_clientes_blueprint.route("/clientes/<int:id_clientes>", methods=['DELETE'])
def apagarClientesId(id_clientes):
    try:
        deletado = cadastro_cliente_model.deleteClientePorId(id_clientes)
        if deletado:
            return jsonify({'mensagem': 'Carga deletada com sucesso'}), 200
        else:
            return jsonify({'erro': 'Carga não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@cadastro_clientes_blueprint.route("/clientes", methods=['DELETE'])
def apagarTodosClientes():
    try:
        resposta,erro = cadastro_cliente_model.deleteTodosClientes()
        return jsonify(resposta), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400