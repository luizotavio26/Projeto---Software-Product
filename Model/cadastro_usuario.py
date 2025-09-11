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
      

def listarUsuarios():
    usuarios  = Usuarios.query.all()   
    return [{"id": u.id,
             "nome": u.name ,
             "idade": u.idade, 
             "email" : u.email, 
             "senha" : u.senha , 
             "cidade" : u.cidade, 
             "UF": u.uf,
             "pais" : u.pais, 
             "cpf" : u.cpf , 
             "CEP" : u.cep , 
             "Telefone" : u.telefone , 
             "genero": u.genero } 
            for u in usuarios]

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
    
    return {
        "id": novoUsuario.id,
        "nome": novoUsuario.name,
        "idade": novoUsuario.idade,
        "email": novoUsuario.email,
        "senha": novoUsuario.senha,
        "cidade": novoUsuario.cidade,
        "UF": novoUsuario.uf,
        "pais": novoUsuario.pais,
        "cpf": novoUsuario.cpf,
        "CEP": novoUsuario.cep,
        "Telefone": novoUsuario.telefone,
        "genero": novoUsuario.genero
    }

def deletarTudo():
    db.session.query(Usuarios).delete()
    db.session.commit()
    return "Todos os usuários deletados"
