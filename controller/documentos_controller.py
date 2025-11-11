from flask import Blueprint, request, jsonify
from model.documentos.documentos_motorista import relatorioDeTodosMotoristas
from model.documentos.documentos_veiculos import relatorioDeTodosVeiculos
from model.documentos.documentos_cargas import relatorioDeTodasCargas
from model.documentos.documentos_faturamento import relatorioEmpresa
from model.documentos.relatorio_empresa import gerarRelatorioEmpresa


documentos = Blueprint('documentos', __name__)

@documentos.route("/test", methods=['GET'])
def test():
    return jsonify({"message":"Documentos Blueprint funcionando!"}), 200


@documentos.route("/relatorio/motoristas", methods=['GET'])
def relatorio_motoristas():
    try:
        return relatorioDeTodosMotoristas(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@documentos.route("/relatorio/veiculos", methods=['GET'])
def relatorio_veiculos():
    try:
        return relatorioDeTodosVeiculos(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@documentos.route("/relatorio/cargas", methods=['GET'])
def relatorio_cargas():
    try:
        return relatorioDeTodasCargas(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@documentos.route("/relatorio/faturamento", methods=['GET'])
def relatorio_faturamento():
    try:
        return relatorioEmpresa(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@documentos.route("/relatorio/empresa", methods=['GET'])
def relatorio_empresa():
    try:
        return gerarRelatorioEmpresa(),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500