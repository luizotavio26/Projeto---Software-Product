from flask import Blueprint, request, jsonify
from Model import upload_doc
from Model.upload_doc import *

upload_bp = Blueprint('upload_bp', __name__)

app = upload_bp

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'arquivo' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    file = request.files['arquivo']
    file.save(f"uploads/{file.filename}")
    return jsonify({"mensagem": "Upload realizado com sucesso"}),200