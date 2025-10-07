from config import db

class Veiculos(db.Model):

    __tablename__ = "Veiculos"   
     
    id = db.Column(db.Integer, primary_key=True ,)
    placa = db.Column(db.String(7), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    renavan = db.Column(db.String(11), nullable=False)
    chassi = db.Column(db.String(17), nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    ano_modelo = db.Column(db.String(4), nullable=False)
    ano_fabricacao = db.Column(db.String(4), nullable=False)


    def to_dict(self): 
        return {
                "id": self.id,
                "placa": self.placa ,
                "modelo": self.modelo, 
                "marca" : self.marca,  
                "renavan" : self.renavan, 
                "chassi": self.chassi,
                "cor" : self.cor, 
                "tipo" : self.tipo , 
                "ano_modelo" : self.ano_modelo , 
                "ano_fabricacao" : self.ano_fabricacao } 


class VeiculoNaoEncontrado(Exception):
    pass


def getVeiculos():
    veiculos  = Veiculos.query.all()   
    return [v.to_dict() for v in veiculos], None


def getVeiculosId(id_veiculo):
    veiculo = Veiculos.query.get(id_veiculo)
    if veiculo:
        return veiculo.to_dict()
    return {"message": "Veículo não encontrado"}, None


def postVeiculos(dados):
    novo_veiculo = Veiculos(
        placa=dados.get("placa"),
        modelo=dados.get("modelo"),
        marca=dados.get("marca"),
        renavan=dados.get("renavan"),
        chassi=dados.get("chassi"),
        cor=dados.get("cor"),
        tipo=dados.get("tipo"),
        ano_modelo=dados.get("ano_modelo"),
        ano_fabricacao=dados.get("ano_fabricacao")
    )
    
    db.session.add(novo_veiculo)
    db.session.commit()
    
    return f"Veículo {novo_veiculo.modelo} cadastrado com sucesso."


def putVeiculoPorId(id_veiculo, dados):
    veiculo = Veiculos.query.get(id_veiculo)
    
    if veiculo:
        veiculo.placa = dados.get("placa", veiculo.placa)
        veiculo.modelo = dados.get("modelo", veiculo.modelo)
        veiculo.marca = dados.get("marca", veiculo.marca)
        veiculo.renavan = dados.get("renavan", veiculo.renavan)
        veiculo.chassi = dados.get("chassi", veiculo.chassi)
        veiculo.cor = dados.get("cor", veiculo.cor)
        veiculo.tipo = dados.get("tipo", veiculo.tipo)
        veiculo.ano_modelo = dados.get("ano_modelo", veiculo.ano_modelo)
        veiculo.ano_fabricacao = dados.get("ano_fabricacao", veiculo.ano_fabricacao)

        
        db.session.commit()
        return f"Veículo com ID {id_veiculo} atualizado com sucesso."
    
    return f"Veículo com ID {id_veiculo} não encontrado."


def deleteVeiculoPorId(id_veiculo):
    veiculo = Veiculos.query.get(id_veiculo)
    
    if veiculo:
        db.session.delete(veiculo)
        db.session.commit()
        return f"veículo com ID {id_veiculo} deletado com sucesso."
    
    return f"Veículo com ID {id_veiculo} não encontrado."
