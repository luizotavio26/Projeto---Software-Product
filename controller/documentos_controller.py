from flask import Blueprint, request, jsonify
from model.documentos.documentos import *

documentos = Blueprint('documentos', __name__)

@documentos.route("/test", methods=['GET'])
def test():
    return jsonify({"message":"Documentos Blueprint funcionando!"}), 200


@documentos.route("/relatorio/motoristas", methods=['GET'])
def relatorio_motoristas():
    dados = request.args.get('token')
    try:
        return relatorioDeTodosMotoristas(token=dados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@documentos.route("/relatorio/veiculos", methods=['GET'])
def relatorio_veiculos():
    dados = request.args.get('token')
    try:
        return relatorioDeTodosVeiculos(token=dados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@documentos.route("/relatorio/cargas", methods=['GET'])
def relatorio_cargas():
    dados = request.args.get('token')
    try:
        return relatorioDeTodasCargas(token=dados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
