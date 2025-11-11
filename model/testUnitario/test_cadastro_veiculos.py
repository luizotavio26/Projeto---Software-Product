import unittest
import requests
import sys, os
# adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from config import url


class TestCadastroVeiculos(unittest.TestCase):
     
     def test_01_listar_todos_veiculos(self):
         response = requests.get(f"{url}/veiculos")
         self.assertEqual(response.status_code, 200)
     
     def test_02_cadastrar_novo_veiculo(self):

         payload = {
             "placa": "ABC1234",
             "modelo": "Modelo Teste",
             "marca": "Marca Teste",
             "renavan": "12345678901",
             "chassi": "9BWZZZ377VT004251",
             "cor": "Azul",
             "tipo": "Carro",
             "ano_modelo": 2022,
             "ano_fabricacao": 2021,
             "peso_maximo_kg": 1000
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
                        "ano_fabricacao": 2022,
                        "peso_maximo_kg": 1000
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
