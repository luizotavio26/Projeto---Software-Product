from flask import Blueprint, request, jsonify
from Model import cadastro_usuario
from Model.cadastro_usuario import *

cadastro_usuarios = Blueprint('cadastro_usuarios', __name__)

app = cadastro_usuarios

@app.route("/listUsuarios", methods=['GET'])
def listUsuarios():
    try:
        usuarios,erro = cadastro_usuario.listarUsuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route("/cadastroClientes", methods=['POST'])
def cadastro():
    dados = request.get_json(silent=True)   
    r = cadastraUsuarioDB(dados)
    return jsonify({"message":"Deu certo",
                    "statusDB" : r}), 200

@app.route("/cadastroClientes", methods=['GET'])
def listar_cargas():
    try:
        usuarios,erro = cadastro_usuario.listarUsuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route("/cadastroClientes/<int:id_clientes>", methods=['DELETE'])
def apagar_clientes_id(id_clientes):
    try:
        deletado = cadastro_usuario.delete_cliente_id(id_clientes)
        if deletado:
            return jsonify({'mensagem': 'Carga deletada com sucesso'}), 200
        else:
            return jsonify({'erro': 'Carga não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route("/deleta", methods=['DELETE']) # isso deleta a tabela em si
def deletar():
     response = deletarTudo()
     return jsonify({"status" : response}), 200



