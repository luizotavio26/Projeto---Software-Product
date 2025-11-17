import unittest
import requests
import unittest
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from test_cadastro_cliente import TestCadastroCliente
from test_cadastro_veiculos import TestCadastroVeiculos
from test_motorista_controle import TestMotoristaControle
from test_manifesto_carga import TestManifestoCarga
import sys, os
# adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from config import url


class Test(unittest.TestCase):
        
    def test_viacep(self):
        cep = "01001000"
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        
        self.assertEqual(response.status_code, 200)  # Código HTTP 200 OK
        data = response.json()
        self.assertIn("logradouro", data)            # Campo deve existir
        self.assertEqual(data["bairro"], "Sé") 
     
    # def test_database_connection(self):
    #     db_uri = "postgresql://software_product_user:zXFrTtfRy6axGTP214ljH8IpHSgaZ3Hb@dpg-d3km73a4d50c73ddhm50-a.oregon-postgres.render.com/software_product"
        
    #     try:
    #         engine = create_engine(db_uri)
    #         connection = engine.connect()
    #         connection.close()
    #         connected = True
    #     except OperationalError:
    #         connected = False
        
    #     self.assertTrue(connected, "Falha ao conectar ao banco de dados")
        
if __name__ == '__main__':
    unittest.main()
