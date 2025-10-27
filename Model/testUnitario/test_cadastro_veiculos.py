import unittest
import requests

url = "http://127.0.0.1:5036"

class TestCadastroVeiculos(unittest.TestCase):
     
     def test_01_listar_todos_veiculos(self):
         response = requests.get(f"{url}/veiculos")
         self.assertEqual(response.status_code, 200)
     
     def test_02_cadastrar_novo_veiculo(self):
#              placa = db.Column(db.String(7), nullable=False)
#     modelo = db.Column(db.String(50), nullable=False)
#     marca = db.Column(db.String(50), nullable=False)
#     renavan = db.Column(db.String(11), nullable=False)
#     chassi = db.Column(db.String(17), nullable=False)
#     cor = db.Column(db.String(50), nullable=False)
#     tipo = db.Column(db.String(50), nullable=False)
#     ano_modelo = db.Column(db.String(4), nullable=False)
#     ano_fabricacao = db.Column(db.String(4), nullable=False)
          
         payload = {
             "placa": "ABC1234",
             "modelo": "Modelo Teste",
             "marca": "Marca Teste",
             "renavan": "12345678901",
             "chassi": "9BWZZZ377VT004251",
             "cor": "Azul",
             "tipo": "Carro",
             "ano_modelo": 2022,
             "ano_fabricacao": 2021
         }
         response = requests.post(f"{url}/veiculos", json=payload)
         self.assertEqual(response.status_code, 201)
         
     def test_03_listar_veiculo_por_id(self):
          response = requests.get(f"{url}/veiculos")
          veiculos = response.json()
          for veiculo in veiculos:
               if veiculo['placa'] == "ABC1234":
                    id_veiculo = veiculo['id']
                    get_response = requests.get(f"{url}/veiculos/{id_veiculo}")
                    self.assertEqual(get_response.status_code, 200)
     
     def test_04_atualizar_veiculo_por_id(self):  
          response = requests.get(f"{url}/veiculos")
          veiculos = response.json()
          for veiculo in veiculos:
               if veiculo['placa'] == "ABC1234":
                    id_veiculo = veiculo['id']
                    payload = {
                        "placa": "ABC1234",
                        "modelo": "Modelo Atualizado",
                        "marca": "Marca Atualizada",
                        "renavan": "12345678901",
                        "chassi": "9BWZZZ377VT004251",
                        "cor": "Vermelho",
                        "tipo": "Carro",
                        "ano_modelo": 2023,
                        "ano_fabricacao": 2022
                    }
                    put_response = requests.put(f"{url}/veiculos/{id_veiculo}", json=payload)
          
          response = requests.get(f"{url}/veiculos")
          veiculos = response.json()
          for veiculo in veiculos:
               if veiculo['placa'] == "ABC1234":
                    self.assertEqual(veiculo['modelo'], "Modelo Atualizado")
     
     def test_05_deletar_veiculo(self):
          response = requests.get(f"{url}/veiculos")
          veiculos = response.json()
          for veiculo in veiculos:
               if veiculo['placa'] == "ABC1234":
                    id_veiculo = veiculo['id']
                    delete_response = requests.delete(f"{url}/veiculos/{id_veiculo}")
                    self.assertEqual(delete_response.status_code, 200)
     

         
     

if __name__ == '__main__':
    unittest.main()
