from config import db
from datetime import datetime

class Motoristas(db.Model):
    __tablename__ = "Motoristas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(15), nullable=False)
    rg = db.Column(db.String(15), nullable=False)
    salario = db.Column(db.Float, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    numero_cnh = db.Column(db.String(20), nullable=False)
    categoria_cnh = db.Column(db.String(10), nullable=False)
    validade_cnh = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    uf = db.Column(db.String(50), nullable=False)
    cep = db.Column(db.String(50), nullable=False)
    
    #validar após a criação da tabela e CRUD de veiculos
    #veiculos = db.relationship("Veiculos", back_populates="motorista")

    
    def __init__(self,nome, cpf, rg, salario, data_nascimento, numero_cnh, categoria_cnh, validade_cnh, telefone, email, endereco, cidade, uf, cep):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.salario = salario
        self.data_nascimento = data_nascimento
        self.numero_cnh = numero_cnh
        self.categoria_cnh = categoria_cnh
        self.validade_cnh = validade_cnh
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.cidade = cidade
        self.uf = uf
        self.cep = cep
    

    def to_dict(self): 
        return {
                "id": self.id,
                "nome": self.nome,
                "cpf": self.cpf, 
                "rg" : self.rg,
                "salario": self.salario,
                "data_nascimento": self.data_nascimento,
                "numero_cnh" : self.numero_cnh,
                "categoria_cnh": self.categoria_cnh,
                "validade_cnh": self.validade_cnh,
                "telefone" : self.telefone, 
                "email": self.email,
                "endereco" : self.endereco,
                "cidade" : self.cidade, 
                "uf": self.uf,
                "cep": self.cep} 

class MotoristaNaoEncontrado(Exception):
    pass


def create_motorista(motorista):
    novo_motorista = Motoristas(
        nome = motorista["nome"],
        cpf = motorista["cpf"], 
        rg = motorista["rg"],
        salario = motorista["salario"],
        data_nascimento = datetime.strptime(motorista['data_nascimento'], "%Y-%m-%d").date(),
        numero_cnh = motorista["numero_cnh"],
        categoria_cnh = motorista["categoria_cnh"],
        validade_cnh = motorista["validade_cnh"], 
        telefone = motorista["telefone"],
        email = motorista["email"],
        endereco = motorista["endereco"],
        cidade = motorista["cidade"], 
        uf = motorista["uf"],
        cep = motorista["cep"]
    )

    db.session.add(novo_motorista)
    db.session.commit()
    return novo_motorista.to_dict(), None

def read_todos_motorista():
    motoristas  = Motoristas.query.all()   
    return [motorista.to_dict() for motorista in motoristas], None

def read_motorista_id(id_motorista):
    motorista = Motoristas.query.get(id_motorista)
    if not motorista:
        return {"message": "Nenhum motorista encontrado"}
    else:
        return motorista.to_dict()


def update_motorista(id_motorista, dados_atualizados):
    motorista = Motoristas.query.get(id_motorista)
    if not motorista:
        return {"message": "Nenhum motorista encontrado"}
    else:
        motorista.nome = dados_atualizados["nome"]
        motorista.cpf = dados_atualizados["cpf"]
        motorista.rg = dados_atualizados["rg"]
        motorista.salario = dados_atualizados["salario"]
        motorista.data_nascimento = dados_atualizados["data_nascimento"]
        motorista.numero_cnh = dados_atualizados["numero_cnh"]
        motorista.categoria_cnh = dados_atualizados["categoria_cnh"]
        motorista.validade_cnh = dados_atualizados["validade_cnh"]
        motorista.telefone = dados_atualizados["telefone"]
        motorista.email = dados_atualizados["email"]
        motorista.endereco = dados_atualizados["endereco"]
        motorista.cidade = dados_atualizados["cidade"]
        motorista.uf = dados_atualizados["uf"]
        motorista.cep = dados_atualizados["cep"]

        db.session.commit()
        return {"message": "Informações atualizadas com sucesso"}


def delete_motorista_id(id_motorista):
    motorista = Motoristas.query.get(id_motorista)
    if not motorista:
        return MotoristaNaoEncontrado(f"Motorista não encontrado")
    else:
        db.session.delete(motorista)
        db.session.commit()
        return {"message": "Motorista deletado com sucesso"}, None


def delete_todos_motoristas():
    db.session.query(Motoristas).delete()
    db.session.commit()
    return {"message": "Todos os motoristas deletados com sucesso"}, None

