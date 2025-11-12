from config import db
from sqlalchemy.exc import IntegrityError
import secrets
import datetime
from model.envioEmail.esqueciSenha import emailSenhaEsquecida
class Usuarios(db.Model):

    __tablename__ = "Usuarios"   
     
    id = db.Column(db.Integer, primary_key=True ,)
    nome_usuario = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(50), nullable=False)

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
    usuario  = Usuarios.query.all()   
    return [usuario.to_dict() for usuario in usuarios]

def getUsuarioId(id_usuario):
    usuario = Usuarios.query.get(id_usuario)
    if not usuario:
        raise UsuarioNaoEncontrado
    
    return usuario.to_dict()

def postUsuario(dados):
    try:
        if usuarios.query.filter_by(email=dados.get('email')).first():
                return None, "E-mail já cadastrado no sistema."

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
    
    usuario.nome_usuario = dados.get("nome_usuario", usuario.cnpj)
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

def secretKet():
    # essa biblioteca vai gerar uma sequencia de 16 digitos 0-9 e a-z.
    # o numero passado como parametro vai ser multiplicado por 2 -> 2*8 = 16
    secret_key = secrets.token_hex(8)
    return secret_key

def verificaSenhaEmail(dados):
    #consultando o usuario pelo email e pelo nome de usuario
    email_usuario = Usuarios.query.filter_by(email=dados["email"]).first()
    usuario_nome = Usuarios.query.filter_by(email=dados["nome_usuario"]).first()

    # gerando o SECRET_KEY
    SECRET_KEY = secretKet()

    #vendo se o email ou nome de usuario é valido
    if email_usuario is None:
        return {"message": "registro não encontrado, faça seu cadastro"}
    
    elif usuario_nome is None:
        return {"message": "registro não encontrado, faça seu cadastro"}

    else:
        #vendo se senha está correta
        if dados["senha"] != usuario.senha:
            return {"message": "senha invalida"}

        # se tudo estiver certo, vamos gerar o token para o login
        else:
            #Gerando o token
            token = jwt.encode(
            {"email": dados["email"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
            )
            
            # retornando a mensagem de sucesso e o token
            return ({"message": "Login realizado com sucesso", "token": token,"success": True})

def esqueciSenha(email_user):
    #acessando dados do usuario pelo email passado pelo parametro
    # não vamos usar nome de usuario para isso, só o email
    usuario = Usuarios.query.filter_by(email=email_user).first()

    # avaliando se o email realmente está no banco de dados
    if usuario is none:
        return {"message": "nenhum registro encontrado"}

    # chamando a função que envia e-mail para redirecionar para a página de mudança de senha
    emailSenhaEsquecida(usuario.nome_usuario, usuario.email)
    return {"message": "e-mail para a troca de senha enviado, cheque sua caixa de e-mail"}


