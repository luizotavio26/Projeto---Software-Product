from config import db

class Documento(db.Model):
    __tablename__ = "Arquivos"
    id = db.Column(db.Integer, primary_key=True)
    arquivo = db.Column(db.LargeBinary, nullable=True)

def anexar_arquivo(arquivo):
    db.session.add(arquivo)
    db.session.commit()
    return {"message":"Arquivo anexado"}