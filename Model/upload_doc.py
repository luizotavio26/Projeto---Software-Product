from config import db
from flask import send_file, abort
from io import BytesIO

class Documentos(db.Model):
    __tablename__ = "Documentos"
    __bind_key__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    arquivo = db.Column(db.LargeBinary, nullable=True)

    #user_id = db.Column(db.Integer, db.ForeignKey("Usuarios.id"), nullable=False)
    #user = db.relationship("Usuarios", back_populates="Arquivos") 

def anexar_arquivo(arquivo):
    # criar condição para que o arquivo só seja acessado se tiver o id de usuario
    db.session.add(arquivo)
    db.session.commit()
    return {"message":"Arquivo anexado"}

def listar_arquivos_id(doc_id):
    doc = Documentos.query.get(doc_id)
    if not doc:
        return abort(404, "Arquivo não encontrado")

    arquivo_em_memoria = BytesIO(doc.arquivo)

    # Gerar um nome genérico usando o id
    nome_arquivo = f"arquivo_{doc.id}"

    # Detectar o tipo do arquivo pelos bytes (opcional: aqui usamos PDF como default)
    tipo_mime = 'application/pdf'  # você pode mudar para image/png se souber que é imagem

    return send_file(
        arquivo_em_memoria,
        download_name=f"{nome_arquivo}.pdf",  # acrescenta extensão
        mimetype=tipo_mime,
        as_attachment=False  # False abre no navegador
    )


def baixar_arquivo(doc_id):
    arquivo = Documentos.query.get(doc_id)
    return send_file(BytesIO(arquivo.dados), download_name=arquivo.nome, as_attachment=True)