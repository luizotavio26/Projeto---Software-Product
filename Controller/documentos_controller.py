from flask import Blueprint, request, jsonify
from Model.documentos import documentos_model
from Model.documentos.tests.test import download_pdf
from Model.documentos.tests.test2 import *
from Model.documentos.tests.test3 import *


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

    


