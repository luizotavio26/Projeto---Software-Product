from flask import Blueprint, request, jsonify
from model.documentos import documentos_model
from model.documentos.tests.test import download_pdf
from model.documentos.tests.test2 import *
from model.documentos.tests.test3 import *


documentos = Blueprint('documentos', __name__)

@documentos.route("/test", methods=['GET'])
def test():
    return jsonify({"message":"Documentos Blueprint funcionando!"}), 200

@documentos.route("/test/<int:id>", methods=['GET'])
def get_documento(id):
    if id == 1: 
        return download_pdf()
    elif id == 2:
        return gerar_relatorio()
    elif id == 3:
        return gerar_faturamento()
    else:
        return jsonify({"message": f"Documentos Blueprint funcionando! ID recebido: {id}"}), 200


    


