from config import db
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
import secrets
import jwt
import datetime
from model.manifesto_model import ManifestoCarga
from model.motorista_model import Motoristas
from model.cliente_model import Clientes
from model.veiculos_model import Veiculos
from model.user_model import Usuarios
from math import floor

#Classe admin
class Administradores(db.Model):

    __tablename__ = "Administradores"   
     
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(50), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)

    '''
    motorista = db.relationship("Motoristas", back_populates="usuario")
    veiculo = db.relationship("Veiculos", back_populates="usuario")
    cliente = db.relationship("Clientes", back_populates="usuario")
    manifestos = db.relationship("ManifestoCarga", back_populates="usuario")
    '''
    
    
    def __init__(self, nome_usuario, email, senha, isAdmin):
        self.nome_usuario = nome_usuario
        self.email = email
        self.senha = senha
        self.isAdmin = isAdmin


    def to_dict(self): 
        return {
                "id": self.id,
                "nome_usuario": self.nome_usuario ,
                "email" : self.email,
                "senha" : self.senha}

class AdminNaoEncontrado(Exception):
    pass

class ErroValidacao(Exception):
    pass

#-------------------------
# ROTAS DA ENTIDADE ADMIN
#-------------------------
def getAdmin():
    admin  = Administradores.query.all()   
    return [admin.to_dict() for admin in admin]

def getAdminId(admin):
    admin = Administradores.query.get(admin)
    if not admin:
        raise AdminNaoEncontrado
    
    return admin.to_dict()

def putAdminPorId(adminId, dados):
    admin = Administradores.query.get(adminId)

    if not admin:
        raise AdminNaoEncontrado
    
    admin.nome_usuario = dados.get("nome_usuario", admin.nome_usuario)
    admin.email = dados.get("email", admin.email)
    admin.senha = dados.get("senha", admin.senha)
    
    
    db.session.commit()
    return {"message": "admin com ID {adminId} atualizado com sucesso."}

def deleteAdminPorId(adminId):
    admin = Administradores.query.get(adminId)
    
    if admin:
        db.session.delete(admin)
        db.session.commit()
        return {"message":"admin com ID {adminId} deletado com sucesso."}
    
    return {"message":"admin com ID {adminId} não encontrado."}

# CADASTRO E LOGIN DE ADMIN COM TOKEN
def postAdmin(dados):
    try:
        if Administradores.query.filter_by(email=dados.get('email')).first():
            return None, "E-mail já cadastrado no sistema."
        
        if Administradores.query.filter_by(nome_usuario=dados.get('nome_usuario')).first():
            return None, "Nome de admin não disponível"

        novo_admin = Administradores(
            email = dados["email"],
            senha = dados["senha"],
            nome_usuario = dados["nome_usuario"],
            isAdmin=True
        )
        
        db.session.add(novo_admin)
        db.session.commit()
        
        return novo_admin.id, None
    
    except IntegrityError as e:
        db.session.rollback()
        
        if 'usuarios_email_key' in str(e):
            return None, "Erro: E-mail já cadastrado no sistema."

        if "usuarios_nome_usuario_key" in str(e):
            return None, "Erro: Nome de admin ja existe no sistema."

        return None, "Erro de integridade dos dados."
        
    except Exception as e:
        db.session.rollback()
        return None, f"Erro interno ao cadastrar: {str(e)}"

def verificaSenhaEmail(dados):
    admin = Administradores.query.filter_by(email=dados["email"]).first()

    # SECRET_KEY
    SECRET_KEY = "ytskryo"

# verifica se o admin existe
    if not admin:
        return {
            "message": "registro não encontrado",
            "success": False
        }

    # verifica senha
    if dados["senha"] != admin.senha:
        return {
            "message": "senha inválida",
            "success": False
        }

    # gera token
    token = jwt.encode(
        {
            "email": admin.email,
            "nome_usuario": admin.nome_usuario,
            "id_usuario": admin.id,
            "isAdmin": True,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "message": "Login realizado com sucesso",
        "token": token,
        "success": True
    }

def esqueciSenha(dados):
    admin = Administradores.query.filter_by(email=dados["email"]).first()

    if not admin:
        raise AdminNaoEncontrado

    admin.senha = dados.get("senha", admin.senha)
    db.session.commit()

    return {"success": True, "message": "Senha alterada com sucesso"}

#------------------------------------------------------------------------
# ROTAS PARA ACESSAR OUTRAS ENTIDADES
#------------------------------------------------------------------------
def getClientes():
    clientes  = Clientes.query.all()   
    return [cliente.to_dict() for cliente in clientes]

def read_todas_cargas():
    cargas = ManifestoCarga.query.all()
    print(cargas)
    return [carga.to_dict() for carga in cargas], None

def read_todos_motorista():
    motoristas  = Motoristas.query.all()   
    return [motorista.to_dict() for motorista in motoristas], None

# def getUsuarios():
#     usuarios  = usuarios.query.all()   
#     return [usuario.to_dict() for usuario in usuarios]

def getUsuarios():
    usuarios = Usuarios.query.all()
    return [usuario.to_dict() for usuario in usuarios]

def getVeiculos():
    veiculos  = Veiculos.query.all()   
    return [v.to_dict() for v in veiculos], None 





# DASHBOARD ADMIN - Totais do sistema

def totalCargasSistema():
    total = ManifestoCarga.query.count()
    return {
        "Cargas": total
    }

def totalClientesSistema():
    total = Clientes.query.count()
    return {
        "Clientes": total
    }

def totalMotoristasSistema():
    total = Motoristas.query.count()
    return {
        "Motoristas": total
    }

def totalVeiculosSistema():
    total = Veiculos.query.count()
    return {
        "Veiculos": total
    }


