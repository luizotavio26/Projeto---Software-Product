from config import db
from sqlalchemy.exc import IntegrityError


class Clientes(db.Model):

    __tablename__ = "Clientes"   
     
    id = db.Column(db.Integer, primary_key=True ,)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    razao_social = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(128), nullable=False)
    telefone = db.Column(db.String(20), nullable=False, unique=True)
    
    cep = db.Column(db.String(9), nullable=False)
    logradouro = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(50), nullable=True)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)

    manifestos = db.relationship("ManifestoCarga", back_populates="cliente")

    def __init__(self, cnpj, razao_social, email, senha, telefone, cep, logradouro, numero, complemento, bairro, cidade, estado):
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado

    def to_dict(self): 
        return {
                "id": self.id,
                "cnpj": self.cnpj ,
                "razao_social": self.razao_social,
                "email" : self.email,
                "senha" : self.senha,
                "telefone" : self.telefone,
                "cep" : self.cep ,
                "logradouro" : self.logradouro,
                "numero" : self.numero,
                "complemento" : self.complemento,
                "bairro" : self.bairro,
                "cidade" : self.cidade,
                "estado" : self.estado}


class ClienteNaoEncontrado(Exception):
    pass

class ErroValidacao(Exception):
    pass


def getClientes():
    clientes  = Clientes.query.all()   
    return [cliente.to_dict() for cliente in clientes]


def getClienteId(id_cliente):
    cliente = Clientes.query.get(id_cliente)
    if not cliente:
        raise ClienteNaoEncontrado
    
    return cliente.to_dict()


def postClientes(dados):
    try:
    
        if Clientes.query.filter_by(cnpj=dados.get('cnpj')).first():
                return None, "CNPJ já cadastrado no sistema."

        novo_cliente = Clientes(
            cnpj = dados["cnpj"],
            razao_social = dados["razao_social"],
            email = dados["email"],
            senha = dados["senha"],
            telefone = dados["telefone"],
            cep = dados["cep"],
            logradouro = dados["logradouro"],
            numero = dados["numero"],
            complemento = dados["complemento"],
            bairro = dados["bairro"],
            cidade = dados["cidade"],
            estado = dados["estado"]
        )
        
        db.session.add(novo_cliente)
        db.session.commit()
        
        return novo_cliente.id, None
    
    except IntegrityError as e:
        db.session.rollback()
        
        if 'clientes_cnpj_key' in str(e):
            return None, "Erro: CNPJ já cadastrado no sistema."

            
        return None, "Erro de integridade dos dados."
        
    except Exception as e:
        db.session.rollback()
        return None, f"Erro interno ao cadastrar: {str(e)}"




def putClientePorId(id_cliente, dados):
    cliente = Clientes.query.get(id_cliente)

    if not cliente:
        raise ClienteNaoEncontrado
    
    cliente.cnpj = dados.get("cnpj", cliente.cnpj)
    cliente.razao_social = dados.get("razao_social", cliente.razao_social)
    cliente.email = dados.get("email", cliente.email)
    cliente.senha = dados.get("senha", cliente.senha)
    cliente.telefone = dados.get("telefone", cliente.telefone)
    cliente.cep = dados.get("cep", cliente.cep)
    cliente.logradouro = dados.get("logradouro", cliente.logradouro)
    cliente.numero = dados.get("numero", cliente.numero)
    cliente.complemento = dados.get("complemento", cliente.complemento)
    cliente.bairro = dados.get("bairro", cliente.bairro)
    cliente.cidade = dados.get("cidade", cliente.cidade)
    cliente.estado = dados.get("estado", cliente.estado)
    
    db.session.commit()
    return {"message": "Usuário com ID {id_cliente} atualizado com sucesso."}



def deleteClientePorId(id_cliente):
    cliente = Clientes.query.get(id_cliente)
    
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        return {"message":"Usuário com ID {id_cliente} deletado com sucesso."}
    
    return {"message":"Usuário com ID {id_cliente} não encontrado."}


def deleteTodosClientes():
    clientes = Clientes.query.all()    
    for cliente in clientes:
        db.session.delete(cliente)
    db.session.commit()
    return {'message':"Usuários deletados com sucesso!"}

def verifica_senha_email(dados):
    #consultando o funcionario pelo email
    cliente = Clientes.query.filter_by(email=dados["email"]).first()

    #vendo se o email é valido
    if cliente is None:
        return {"message": "registro não encontrado, faça seu cadastro"}
    else:
        #vendo se senha está correta
        if dados["senha"] != cliente.senha:
            return {"message": "senha invalida"}

        # se tudo estiver certo
        else:
            #Gerando o token
            token = jwt.encode(
            {"email": dados["email"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )
            
            # retornando a mensagem de sucesso e o token
           return (
               {"message": "Login realizado com sucesso", 
                    "token": token, 
                    "success": True}
           )
