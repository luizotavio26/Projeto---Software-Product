from flask import Blueprint, request, jsonify
from Model import upload_doc
from Model.upload_doc import *

upload_bp = Blueprint('upload_bp', __name__)

app = upload_bp

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    try:
        arquivo = request.files.get("arquivo")
        if not arquivo:
            return {"erro": "Arquivo não enviado"}, 400

        print(f"Nome do arquivo: {arquivo.filename}")  # Debug
        data = arquivo.read()
        print(f"Tamanho do arquivo: {len(data)} bytes")  # Debug

        doc = Documentos(
            arquivo=arquivo.read()
        )

        db.session.add(doc)
        db.session.commit()
        return jsonify({"mensagem": "Upload realizado com sucesso"}), 200

    except Exception as e:
        print(e)  # vai aparecer no terminal do Flask
        return jsonify({"erro": str(e)}), 500


# Especificar o ID do usuario, não do arquivo
@upload_bp.route("/arquivos/<int:doc_id>", methods=["GET"])
def listar(doc_id):
    arquivos = listar_arquivos_id(doc_id)
    return ({"arquivos": arquivos}), 200

# Baixar arquivo
@upload_bp.route("/download/<int:doc_id>", methods=["GET"])
def download(doc_id):
    return baixar_arquivo(doc_id)

