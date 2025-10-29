from config import db
from model.cadastro_cliente_model import Clientes
from model.cadastro_veiculos_model import Veiculos
from model.motorista_model import Motoristas

FAIXAS_KM = [40, 60, 100, 130, 160, 200, 280, 400, 480, 550, 620, 700]

PRECOS = {
    "seca": {
        # 
        "van":   [441, 470, 613, 656, 713, 850, 911, 1032, 1195, 1636, 1808, 1908],
        # 
        "leve":  [583, 625, 740, 797, 869, 999, 1073, 1179, 1404, 1987, 2144, 2273],
        # 
        "toco":  [780, 838, 894, 1010, 1082, 1235, 1311, 1447, 1597, 2377, 2491, 2679],
        # 
        "truck": [971, 1044, 1197, 1280, 1400, 1571, 1662, 1863, 2171, 3142, 3215, 3571]
    },
    "refrigerada": {
        # 
        "van":   [509, 542, 678, 787, 854, 911, 1049, 1204, 1388, 1897, 2066, 2242],
        # 
        "leve":  [604, 658, 800, 948, 1044, 1148, 1247, 1374, 1544, 2148, 2344, 2588],
        # 
        "toco":  [854, 918, 989, 1200, 1301, 1417, 1516, 1657, 1856, 2710, 2845, 2957],
        # 
        "truck": [1065, 1141, 1280, 1410, 1628, 1862, 1920, 2153, 2328, 3393, 3608, 3956]
    }
}

def get_tipo_veiculo(peso):
    # 
    if peso <= 1600:
        return "van"
    # 
    elif peso <= 2500:
        return "leve"
    # 
    elif peso <= 6800:
        return "toco"
    # 
    elif peso <= 12000:
        return "truck"
    else:
        return None


def get_distancia_api(origem, destino):
    """
    *** FUNÇÃO DE SIMULAÇÃO ***
    Aqui você deve implementar a chamada real a uma API como Google Maps Distance Matrix.
    
    PARA TESTE: Vamos simular uma distância com base no tamanho dos nomes das cidades
    para forçar o uso de diferentes faixas da tabela.
    """
    print(f"SIMULANDO DISTÂNCIA para {origem} -> {destino}")
    distancia_simulada = (len(origem) + len(destino)) * 5.3
    
    if distancia_simulada > 700:
        distancia_simulada = 650 
    
    return round(distancia_simulada, 2)


def get_valor_frete_tabelado(tipo_carga, tipo_veiculo, distancia):
    if tipo_carga not in PRECOS or tipo_veiculo not in PRECOS[tipo_carga]:
        return None

    for index, limite_km in enumerate(FAIXAS_KM):
        if distancia <= limite_km:
            return PRECOS[tipo_carga][tipo_veiculo][index]
    
    return None



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
                 destino_carga, valor_km, distancia, valor_frete):
        self.tipo_carga = tipo_carga
        self.peso_carga = peso_carga
        self.cliente_id = cliente_id
        self.motorista_id = motorista_id
        self.veiculo_id = veiculo_id
        self.origem_carga = origem_carga
        self.destino_carga = destino_carga
        self.valor_km = valor_km
        self.distancia = distancia
        self.valor_frete = valor_frete


    def to_dict(self): 
        return {
            "id": self.id,
            "tipo_carga": self.tipo_carga,
            "peso_carga": f"{self.peso_carga} kg",

            "cliente": self.cliente.razao_social if self.cliente else "Cliente não encontrado",
            "motorista": self.motorista.nome if self.motorista else "Motorista não encontrado",
            "veiculo": self.veiculo.placa if self.veiculo else "Veículo não encontrado", 

            "origem_carga": self.origem_carga,
            "destino_carga": self.destino_carga,
            
            "valor_frete": f"R$ {float(self.valor_frete):.2f}".replace(".", ","),
            "valor_km": f"R$ {float(self.valor_km):.2f}".replace(".", ","),
            "distancia": f"{self.distancia} km"
        }


class CargaNaoEncontrada(Exception):
    pass


def create_carga(carga):
    try:
        tipo_carga = carga["tipo_carga"] 
        origem = carga["origem_carga"]
        destino = carga["destino_carga"]
        
        peso_carga_str = carga.get("peso_carga", 0) 
        peso_carga = float(peso_carga_str)

        distancia_calculada = get_distancia_api(origem, destino) 
        
        if distancia_calculada <= 0:
             return None, f"Não foi possível calcular a distância entre {origem} e {destino}."

        tipo_veiculo = get_tipo_veiculo(peso_carga)
        if tipo_veiculo is None:
            return None, f"Peso da carga ({peso_carga}kg) excede o limite da tabela (12000kg)."

        valor_frete_tabelado = get_valor_frete_tabelado(tipo_carga, tipo_veiculo, distancia_calculada)
        
        if valor_frete_tabelado is None:
            msg_erro = f"Valor não encontrado na tabela para: Carga {tipo_carga}, Veículo {tipo_veiculo} (peso {peso_carga}kg), Distância {distancia_calculada}km."
            return None, msg_erro

        valor_km_calculado = valor_frete_tabelado / distancia_calculada

        nova_carga = ManifestoCarga(
            tipo_carga = tipo_carga,
            peso_carga = peso_carga,
            cliente_id = carga["cliente_id"],
            motorista_id = carga["motorista_id"],
            veiculo_id= carga["veiculo_id"],
            origem_carga = origem,
            destino_carga = destino,
            valor_km = round(valor_km_calculado, 2),  
            distancia = round(distancia_calculada, 2), 
            valor_frete = float(valor_frete_tabelado) 
        )

        db.session.add(nova_carga)
        db.session.commit()
        return nova_carga.to_dict(), None

    except KeyError as e:
        db.session.rollback()
        return None, f"Dado obrigatório faltando: {str(e)}. Verifique o JSON enviado pelo frontend."
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

    distancia_calculada = get_distancia_api(carga.origem_carga, carga.destino_carga)
    tipo_veiculo = get_tipo_veiculo(carga.peso_carga)
    valor_frete_tabelado = get_valor_frete_tabelado(carga.tipo_carga, tipo_veiculo, distancia_calculada)
    carga.valor_frete = float(valor_frete_tabelado)
    carga.valor_km = round(valor_frete_tabelado / distancia_calculada, 2)
    carga.distancia = round(distancia_calculada, 2)

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