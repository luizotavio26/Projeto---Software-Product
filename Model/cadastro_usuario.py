from config import db

class Usuarios(db.Model):
<<<<<<< HEAD
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
=======
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
          
      


def listarUsuarios():
    usuarios  = Usuarios.query.all()   
    return [{"id": u.id,
             "nome": u.name ,
             "idade": u.idade, 
             "email" : u.email,  
             "cidade" : u.cidade, 
             "UF": u.uf,
             "pais" : u.pais, 
             "cpf" : u.cpf , 
             "CEP" : u.cep , 
             "Telefone" : u.telefone , 
             "genero": u.genero } 
            for u in usuarios]

def listarUsuarioId(id_usuario):
    u = Usuarios.query.get(id_usuario)
    if u:
        return {
            "id": u.id,
            "nome": u.name,
            "idade": u.idade,
            "email": u.email,
            "cidade": u.cidade,
            "UF": u.uf,
            "pais": u.pais,
            "cpf": u.cpf,
            "CEP": u.cep,
            "Telefone": u.telefone,
            "genero": u.genero
        }
    return {"message": "Usuário não encontrado"}

def cadastraUsuarioDB(dados):
     
>>>>>>> bedc018fbe2e0c1a482aba2d5bb209e3a41f16e1
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
<<<<<<< HEAD
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

=======
    )
    
    db.session.add(novoUsuario)
    db.session.commit()
    
    return {
        "id": novoUsuario.id,
        "nome": novoUsuario.name,
        "idade": novoUsuario.idade,
        "email": novoUsuario.email,
        "cidade": novoUsuario.cidade,
        "UF": novoUsuario.uf,
        "pais": novoUsuario.pais,
        "cpf": novoUsuario.cpf,
        "CEP": novoUsuario.cep,
        "Telefone": novoUsuario.telefone,
        "genero": novoUsuario.genero
    }

def atualizaUsuarioPorId(id_usuario, dados):
    usuario = Usuarios.query.get(id_usuario)
    
    if usuario:
        usuario.name = dados.get("name", usuario.name)
        usuario.idade = dados.get("idade", usuario.idade)
        usuario.email = dados.get("email", usuario.email)
        usuario.senha = dados.get("senha", usuario.senha)
        usuario.cidade = dados.get("cidade", usuario.cidade)
        usuario.uf = dados.get("uf", usuario.uf)
        usuario.pais = dados.get("pais", usuario.pais)
        usuario.cpf = dados.get("cpf", usuario.cpf)
        usuario.cep = dados.get("cep", usuario.cep)
        usuario.telefone = dados.get("telefone", usuario.telefone)
        usuario.genero = dados.get("genero", usuario.genero)
        
        db.session.commit()
        return f"Usuário com ID {id_usuario} atualizado com sucesso."
    
    return f"Usuário com ID {id_usuario} não encontrado."


def deletaUsuarioPorId(id_usuario):
    usuario = Usuarios.query.get(id_usuario)
    
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return f"Usuário com ID {id_usuario} deletado com sucesso."
    
    return f"Usuário com ID {id_usuario} não encontrado."
>>>>>>> bedc018fbe2e0c1a482aba2d5bb209e3a41f16e1
