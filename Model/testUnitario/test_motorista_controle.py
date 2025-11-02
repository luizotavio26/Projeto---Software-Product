import unittest
import requests
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from config import url


class TestMotoristaControle(unittest.TestCase):
     def test_01_criar_motorista(self):

     
          payload = {
          "nome": "João Silva",
          "cpf": "12345678900",
          "rg": "MG1234567",
          "salario": 3000.00,
          "data_nascimento": "1990-01-01",
          "numero_cnh": "1234567890",
          "categoria_cnh": "B",
          "validade_cnh": "2025-01-01",
          "telefone": "31999999999",
          "email": "joao.silva@example.com",
          "cep": "01001000",
          "logradouro": "Rua das Flores",
          "numero": "123",
          "complemento": "Casa",
          "bairro": "Centro",
          "cidade": "São Paulo",
          "estado": "SP"
          }
          response = requests.post(f"{url}/motoristas", json=payload)
          self.assertEqual(response.status_code, 200)
     
     def test_02_listar_motoristas(self):
          response = requests.get(f"{url}/motoristas")
          self.assertEqual(response.status_code, 200)
     
     def test_03_obter_motorista_por_id(self):
          response = requests.get(f"{url}/motoristas")
          motoristas = response.json()
          for motorista in motoristas:
               if motorista["cpf"] == "12345678900":
                    id_motorista = motorista["id"]
                    get_response = requests.get(f"{url}/motoristas/{id_motorista}")
                    self.assertEqual(get_response.status_code, 200)
                    break
               
     def test_04_atualizar_motorista(self):
          response = requests.get(f"{url}/motoristas")
          motoristas = response.json()
          for motorista in motoristas:
               if motorista["cpf"] == "12345678900":
                    id_motorista = motorista["id"]
                    motorista["nome"] = "João Pereira"
                    update_response = requests.put(f"{url}/motoristas/{id_motorista}", json=motorista)
                    break
               
               
          get_response = requests.get(f"{url}/motoristas/{id_motorista}")
          motorista_atualizado = get_response.json()
          self.assertEqual(motorista_atualizado["nome"], "João Pereira")
      
     def test_06_deletar_motorista(self):
          response = requests.get(f"{url}/motoristas")
          motoristas = response.json()
          for motorista in motoristas:
               if motorista["cpf"] == "12345678900":
                    id_motorista = motorista["id"]
                    delete_response = requests.delete(f"{url}/motoristas/{id_motorista}")
                    self.assertEqual(delete_response.status_code, 200)
                    break
           
     
if __name__ == '__main__':
    unittest.main()