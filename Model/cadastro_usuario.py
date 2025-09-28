from config import db

class Usuarios(db.Model):
    __tablename__ = "Usuarios"   
     
    id = db.Column(db.Integer, primary_key=True ,)
    name = db.Column(db.String(50), nullable=True)
    idade = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    senha = db.Column(db.String(50), nullable=True)
    cidade = db.Column(db.String(50), nullable=True)
    uf = db.Column(db.String(50), nullable=True)
    pais = db.Column(db.String(50), nullable=True)
    cpf = db.Column(db.String(50), nullable=True)
    cep = db.Column(db.String(50), nullable=True)
    telefone = db.Column(db.String(50), nullable=True)
    genero = db.Column(db.String(50), nullable=True)

    #documentos = db.relationship('Documentos', back_populates='Usuarios')
    def to_dict(self): 
        return {
                "id": self.id,
                "nome": self.name ,
                "idade": self.idade, 
                "email" : self.email,  
                "cidade" : self.cidade, 
                "UF": self.uf,
                "pais" : self.pais, 
                "cpf" : self.cpf , 
                "CEP" : self.cep , 
                "Telefone" : self.telefone , 
                "genero": self.genero } 

class ClienteNaoEncontrado(Exception):
    pass

def listarUsuarios():
    usuarios  = Usuarios.query.all()   
    return [usuario.to_dict() for usuario in usuarios], None



def cadastraUsuarioDB(dados):
    novoUsuario = Usuarios(
        name=dados.get("name"),
        idade=dados.get("idade"),
        email=dados.get("email"),
        senha=dados.get("senha"),
        cidade=dados.get("cidade"),
        uf=dados.get("uf"),
        pais=dados.get("pais"),
        cpf=dados.get("cpf"),
        cep=dados.get("cep"),
        telefone=dados.get("telefone"),
        genero=dados.get("genero")
        )
        
    db.session.add(novoUsuario)
    db.session.commit()
    return novoUsuario.to_dict(), None
    


def delete_cliente_id(id_cliente):
    cliente = Usuarios.query.get(id_cliente)
    if not cliente:
        return False  # Não encontrado
    db.session.delete(cliente)
    db.session.commit()
    return True  # Deletado


def deletarTudo():
    db.session.query(Usuarios).delete()
    db.session.commit()
    return "Todos os usuários deletados"

