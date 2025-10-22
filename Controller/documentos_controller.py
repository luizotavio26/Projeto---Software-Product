from flask import Blueprint, request, jsonify
from Model.documentos import documentos_model


documentos = Blueprint('documentos', __name__)

@documentos.route("/test", methods=['GET'])
def test():
    return jsonify({"message":"Documentos Blueprint funcionando!"}), 200


