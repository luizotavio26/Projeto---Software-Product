from config import db
from sqlalchemy.exc import IntegrityError
import secrets
import jwt
import datetime
from model.manifesto_model import ManifestoCarga
from model.motorista_model import Motoristas
from model.cliente_model import Clientes
from model.veiculos_model import Veiculos

class Usuarios(db.Model):

    __tablename__ = "Usuarios"   
     
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(50), nullable=False)

    motorista = db.relationship("Motoristas", back_populates="usuario")
    veiculo = db.relationship("Veiculos", back_populates="usuario")
    cliente = db.relationship("Clientes", back_populates="usuario")
    manifestos = db.relationship("ManifestoCarga", back_populates="usuario")
    
    
    

    def __init__(self, nome_usuario, email, senha):
        self.nome_usuario = nome_usuario
        self.email = email
        self.senha = senha


    def to_dict(self): 
        return {
                "id": self.id,
                "nome_usuario": self.nome_usuario ,
                "email" : self.email,
                "senha" : self.senha}

class UsuarioNaoEncontrado(Exception):
    pass

class ErroValidacao(Exception):
    pass

def getUsuarios():
    usuarios  = Usuarios.query.all()   
    return [usuario.to_dict() for usuario in usuarios]

def getUsuarioId(id_usuario):
    usuario = Usuarios.query.get(id_usuario)
    if not usuario:
        raise UsuarioNaoEncontrado
    
    return usuario.to_dict()

def postUsuario(dados):
    try:
        if Usuarios.query.filter_by(email=dados.get('email')).first():
            return None, "E-mail já cadastrado no sistema."
        
        if Usuarios.query.filter_by(nome_usuario=dados.get('nome_usuario')).first():
            return None, "Nome de usuário não disponível"


        novo_usuario = Usuarios(
            email = dados["email"],
            senha = dados["senha"],
            nome_usuario = dados["nome_usuario"],
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        return novo_usuario.id, None
    
    except IntegrityError as e:
        db.session.rollback()
        
        if 'usuarios_email_key' in str(e):
            return None, "Erro: E-mail já cadastrado no sistema."

        if "usuarios_nome_usuario_key" in str(e):
            return None, "Erro: Nome de Usuário ja existe no sistema."

        return None, "Erro de integridade dos dados."
        
    except Exception as e:
        db.session.rollback()
        return None, f"Erro interno ao cadastrar: {str(e)}"

def putUsuarioPorId(id_usuario, dados):
    usuario = Usuarios.query.get(id_usuario)

    if not usuario:
        raise UsuarioNaoEncontrado
    
    usuario.nome_usuario = dados.get("nome_usuario", usuario.nome_usuario)
    usuario.email = dados.get("email", usuario.email)
    usuario.senha = dados.get("senha", usuario.senha)
    
    
    db.session.commit()
    return {"message": "Usuário com ID {id_usuario} atualizado com sucesso."}

def deleteUsuarioPorId(id_usuario):
    usuario = Usuarios.query.get(id_usuario)
    
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return {"message":"Usuário com ID {id_usuario} deletado com sucesso."}
    
    return {"message":"Usuário com ID {id_usuario} não encontrado."}

def deleteTodosUsuario():
    usuarios = Usuarios.query.all()    
    for usuario in usuarios:
        db.session.delete(usuario)
    db.session.commit()
    return {'message':"Usuários deletados com sucesso!"}

def verificaSenhaEmail(dados):
    #consultando o usuario pelo email e pelo nome de usuario
    usuario = Usuarios.query.filter_by(email=dados["email"]).first()

    # SECRET_KEY
    SECRET_KEY = "trajetto_express"

    #vendo se o email ou nome de usuario é valido
    if usuario.email is None:
        return {"message": "registro não encontrado, faça seu cadastro"}

    elif usuario.nome_usuario is None:
        return {"message": "registro não encontrado"}
    
    else:
        #vendo se senha está correta
        if dados["senha"] != usuario.senha:
            return {"message": "senha invalida"}

        # se tudo estiver certo, vamos gerar o token para o login
        else:
            #Gerando o token
            token = jwt.encode(
            {"email": usuario.email, 
            "nome_usuario": usuario.nome_usuario,
            "id_usuario": usuario.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
            )
            
            # retornando a mensagem de sucesso e o token
            return ({"message": "Login realizado com sucesso", "token": token,"success": True})

def esqueciSenha(dados):
    usuario = Usuarios.query.filter_by(email=dados["email"]).first()

    if not usuario:
        raise UsuarioNaoEncontrado

    usuario.senha = dados.get("senha", usuario.senha)
    db.session.commit()

    return {"success": True, "message": "Senha alterada com sucesso"}

# ---------------------------------------------------------------------------------------------------
# ROTAS PARA O DASHBOARD
# ---------------------------------------------------------------------------------------------------

def cargasCadastradas(usuario_id):
    quantidade_cargas = ManifestoCarga.query.filter_by(usuario_id=usuario_id).count()
    return ({"Cargas": quantidade_cargas})

def motoristasCadastrados(usuario_id):
    quantidade_motoristas = Motoristas.query.filter_by(usuario_id=usuario_id).count()
    return ({"Motoristas": quantidade_motoristas})

def clientesCadastrados(usuario_id):
    quantidade_clientes = Clientes.query.filter_by(usuario_id=usuario_id).count()
    return ({"Clientes": quantidade_clientes})

def veiculosCadastrados(usuario_id):
    quantidade_veiculos = Veiculos.query.filter_by(usuario_id=usuario_id).count()
    return ({"Veiculos": quantidade_veiculos})

