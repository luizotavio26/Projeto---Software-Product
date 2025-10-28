from config import db
from model.cadastro_cliente_model import Clientes
from model.cadastro_veiculos_model import Veiculos
from model.motorista_model import Motoristas

class ManifestoCarga(db.Model):
    __tablename__ = "manifesto_carga"

    id = db.Column(db.Integer, primary_key=True)
    tipo_carga = db.Column(db.String(50), nullable=False)
    peso_carga = db.Column(db.Float, nullable=False)

    motorista_id = db.Column(db.Integer, db.ForeignKey("Motoristas.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("Clientes.id"), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey("Veiculos.id"), nullable=False)

    origem_carga = db.Column(db.String(200), nullable=False)
    destino_carga = db.Column(db.String(200), nullable=False)
    valor_frete = db.Column(db.Float, nullable=False)
    valor_km = db.Column(db.Float, nullable=False)
    distancia = db.Column(db.Float, nullable=False)

    motorista = db.relationship("Motoristas", back_populates="manifestos")
    cliente = db.relationship("Clientes", back_populates="manifestos")
    veiculo = db.relationship("Veiculos", back_populates="manifestos")



    def __init__(self, tipo_carga, peso_carga, motorista_id, cliente_id, veiculo_id, origem_carga,
                 destino_carga, valor_km, distancia):
        self.tipo_carga = tipo_carga
        self.peso_carga = peso_carga
        self.cliente_id = cliente_id
        self.motorista_id = motorista_id
        self.veiculo_id = veiculo_id
        self.origem_carga = origem_carga
        self.destino_carga = destino_carga
        self.valor_km = valor_km
        self.distancia = distancia
        self.valor_frete = self.calcular_frete()


    def calcular_frete(self):
        frete = self.valor_km * self.distancia
        return (f"{frete:.2f}")


    def to_dict(self): 
        return {
        "id": self.id,
        "tipo_carga": self.tipo_carga,
        "peso_carga": self.peso_carga,
        "motorista_id": self.motorista_id,
        "cliente_id": self.cliente_id,
        "veiculo_id": self.veiculo_id,
        "origem_carga":self.origem_carga,
        "destino_carga":self.destino_carga,
        "valor_frete":self.valor_frete,
        "valor_km":self.valor_km,
        "distancia":self.distancia}


class CargaNaoEncontrada(Exception):
    pass


def create_carga(carga):
    
    try:
        nova_carga = ManifestoCarga(
            tipo_carga = carga["tipo_carga"],
            peso_carga = carga["peso_carga"],
            cliente_id = carga["cliente_id"],
            motorista_id = carga["motorista_id"],
            veiculo_id= carga["veiculo_id"],
            origem_carga = carga["origem_carga"],
            destino_carga = carga["destino_carga"],
            valor_km = carga["valor_km"],
            distancia = carga["distancia"]
        )

        db.session.add(nova_carga)
        db.session.commit()
        return nova_carga.to_dict(), None

    except Exception as e:
        db.session.rollback()
        return None, str(e)

    
def read_todas_cargas():
    cargas = ManifestoCarga.query.all()
    print(cargas)
    return [carga.to_dict() for carga in cargas], None


def read_cargas_id(id_carga):
    carga = ManifestoCarga.query.get(id_carga)

    if not carga:
        return {'message':'Nenhuma carga encontrada.'}
    else:
        return carga.to_dict()


def update_carga(id_carga, dados_atualizados):
    carga = ManifestoCarga.query.get(id_carga)
    if not carga:
        return {'message':'Nenhuma carga encontrada.'}
    
    carga.tipo_carga = dados_atualizados["tipo_carga"]
    carga.peso_carga = dados_atualizados["peso_carga"]
    carga.cliente_id = dados_atualizados["cliente_id"]
    carga.motorista_id = dados_atualizados["motorista_id"]
    carga.veiculo_id = dados_atualizados["veiculo_id"]
    carga.origem_carga = dados_atualizados["origem_carga"]
    carga.destino_carga = dados_atualizados["destino_carga"]
    carga.valor_km = dados_atualizados["valor_km"]
    carga.distancia = dados_atualizados["distancia"]
    carga.valor_frete = carga.calcular_frete()

    db.session.commit()

    return {'message': "Informações sobre a carga atualizada com sucesso!"}, None


def delete_carga_id(id_carga):
    carga = ManifestoCarga.query.get(id_carga)
    if not carga:
        raise CargaNaoEncontrada(f'Informação sobre a carga não encontrada.')
    db.session.delete(carga)
    db.session.commit()
    return {"message":"Cargas deletadas com sucesso!"}, None


def delete_todas_cargas():
    cargas = ManifestoCarga.query.all()
    for carga in cargas:
        db.session.delete(carga)
    db.session.commit()
    return {'message':"Cargas deletadas com sucesso!"}, None