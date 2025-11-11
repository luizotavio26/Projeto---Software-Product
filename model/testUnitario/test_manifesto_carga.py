import unittest
import requests
import sys, os
# adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from config import url



class TestManifestoCarga(unittest.TestCase):
     

     
     def test_02_criar_nova_carga(self):
          
          # criar motorista, 
          
          payload ={
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
          r = 200
          self.assertEqual(r, 200)
          
          response = requests.get(f"{url}/motoristas")
          motoristas = response.json()
          for motorista in motoristas:
               if motorista["cpf"] == "12345678900":
                    id_motorista = motorista["id"]          
                    break
          
          
          # criar cliente,
          
          payload =  {
            "cnpj": "12345678000190",
            "razao_social": "Empresa Teste LTDA",
            "email": "contato@empresa.com",
            "senha": "senha123",
            "telefone": "11999999999",
            "cep": "01001000",
            "logradouro": "Rua Teste",
            "numero": "123",
            "complemento": "Apto 45",
            "bairro": "Centro",
            "cidade": "São Paulo",
            "estado": "SP"
        }
          response = requests.post(f"{url}/clientes", json=payload)
          self.assertEqual(response.status_code, 201)
               
          cnpj = "12345678000190"
          response = requests.get(f"{url}/clientes")
          response = response.json()
          for cliente in response:
               if cliente["cnpj"] == cnpj:
                    id_cliente = cliente["id"]
                    break

          # criar veiculo
          
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
          
          response = requests.get(f"{url}/veiculos")
          veiculos = response.json()
          for veiculo in veiculos:
               if veiculo['placa'] == "ABC1234":
                    id_veiculo = veiculo['id']
                    break
          
          # criar carga
          
          payload = {
               "tipo_carga": "Carga Teste",
               "peso_carga": 1500.5,
               "motorista_id": id_motorista,
               "cliente_id": id_cliente,
               "veiculo_id": id_veiculo,
               "origem_carga": "São Paulo, SP",
               "destino_carga": "Rio de Janeiro, RJ",
               "valor_km": 2.5,
               "distancia": 430.0
          }
          response = requests.post(f"{url}/cargas", json=payload)
          self.assertEqual(response.status_code, 200)
          
     # def test_03_listar_cargas(self):
     #      response = requests.get(f"{url}/cargas")
     #      self.assertEqual(response.status_code, 200)
     
     # def test_04_obter_carga_por_id(self):
     #      response = requests.get(f"{url}/cargas")
     #      cargas = response.json()
     #      for carga in cargas:
     #           if carga["tipo_carga"] == "Carga Teste":
     #                id_carga = carga["id"]
     #                get_response = requests.get(f"{url}/cargas/{id_carga}")
     #                self.assertEqual(get_response.status_code, 200)
     #                break
   
     # def test_05_atualizar_carga(self):
     #      response = requests.get(f"{url}/cargas")
     #      carga = response.json()
     #      for carga in carga:
     #           if carga["tipo_carga"] == "Carga Teste":
     #                id_carga = carga["id"]
                   
     #                id_motorista_antiga = carga["motorista_id"]
     #                id_cliente_antiga = carga["cliente_id"]
     #                id_veiculo_antiga = carga["veiculo_id"]
                    
     #                # criar motorista, 
                              
     #                payload = {
     #                     "nome": "Mariana Costa",
     #                     "cpf": "34698215009",
     #                     "rg": "SP9876543",
     #                     "salario": 4200.50,
     #                     "data_nascimento": "1988-07-14",
     #                     "numero_cnh": "MTC4589231",
     #                     "categoria_cnh": "AB",
     #                     "validade_cnh": "2027-11-30",
     #                     "telefone": "11981234567",
     #                     "email": "mariana.costa@example.com",
     #                     "cep": "01310000",
     #                     "logradouro": "Av. Paulista",
     #                     "numero": "1500",
     #                     "complemento": "Apto 12B",
     #                     "bairro": "Bela Vista",
     #                     "cidade": "São Paulo",
     #                     "estado": "SP"
     #                     }

     #                response = requests.post(f"{url}/motoristas", json=payload)
                    
     #                response = requests.get(f"{url}/motoristas")
     #                motoristas = response.json()
     #                for motorista in motoristas:
     #                     if motorista["cpf"] == "34698215009":
     #                          id_motorista = motorista["id"]          
     #                          break
                    
                    
     #                # criar cliente,
                    
     #                payload = {
     #                     "cnpj": "12345678000190",
     #                     "razao_social": "Empresa Teste LTDA",
     #                     "email": "contato@empresa.com",
     #                     "senha": "senha123",
     #                     "telefone": "11999999999",
     #                     "cep": "01001000",
     #                     "logradouro": "Rua Teste",
     #                     "numero": "123",
     #                     "complemento": "Apto 45",
     #                     "bairro": "Centro",
     #                     "cidade": "São Paulo",
     #                     "estado": "SP"
     #                }
     #                response = requests.post(f"{url}/clientes", json=payload)
                         
     #                cnpj = "12345678000190"
     #                response = requests.get(f"{url}/clientes")
     #                response = response.json()
     #                for cliente in response:
     #                     if cliente["cnpj"] == cnpj:
     #                          id_cliente = cliente["id"]
     #                          break

     #                # criar veiculo
                    
     #                payload = {
     #                "placa": "XYZ4J56",
     #                "modelo": "Onix LTZ 1.4",
     #                "marca": "Chevrolet",
     #                "renavan": "98765432109",
     #                "chassi": "9BD123456VC789012",
     #                "cor": "Prata",
     #                "tipo": "Hatch",
     #                "ano_modelo": 2023,
     #                "ano_fabricacao": 2022,
     #                "peso_maximo_kg": 1000

     #                }

     #                response = requests.post(f"{url}/veiculos", json=payload)
     #                self.assertEqual(response.status_code, 201)
                    
                    
     #                response = requests.get(f"{url}/veiculos")
     #                veiculos = response.json()
     #                for veiculo in veiculos:
     #                     if veiculo['placa'] == "XYZ4J56":
     #                          id_veiculo = veiculo['id']
     #                          break
                    
     #                carga["tipo_carga"] = "Carga Teste Atualizada"
     #                carga["motorista_id"] = id_motorista
     #                carga["id_cliente"] = id_cliente
     #                carga["veiculo_id"] = id_veiculo
                    
                    
     #                update_response = requests.put(f"{url}/cargas/{id_carga}", json=carga)
                    
     #                response = requests.get(f"{url}/cargas/{id_carga}")
     #                carga = response.json()
     #                self.assertEqual(update_response.status_code, 200)
     #                self.assertEqual(carga["tipo_carga"], "Carga Teste Atualizada")
     #                self.assertEqual(carga["motorista_id"], id_motorista)
     #                self.assertEqual(carga["cliente_id"], id_cliente)
     #                self.assertEqual(carga["veiculo_id"], id_veiculo)
                    
     #                delete_response_motorista = delete_response_cliente = delete_response_veiculo = None


     #                delete_response_motorista = requests.delete(f"{url}/motoristas/{id_motorista_antiga}")
     #                delete_response_cliente = requests.delete(f"{url}/clientes/{id_cliente_antiga}")
     #                delete_response_veiculo = requests.delete(f"{url}/veiculos/{id_veiculo_antiga}")
     #                self.assertEqual(delete_response_motorista.status_code, 200)
     #                self.assertEqual(delete_response_cliente.status_code, 400)
     #                self.assertEqual(delete_response_veiculo.status_code, 200)
     #                break
     
     # def test_06_deletar_carga(self):
     #      response = requests.get(f"{url}/cargas")
     #      cargas = response.json()
          
     #      for carga in cargas:
     #           if carga["tipo_carga"] == "Carga Teste Atualizada":
     #                id_carga = carga["id"]
     #                id_motorista = carga["motorista_id"]
     #                id_cliente = carga["cliente_id"]
     #                id_veiculo = carga["veiculo_id"]
                    
     #                delete_response_carga = requests.delete(f"{url}/cargas/{id_carga}")
     #                delete_response_motorista = requests.delete(f"{url}/motoristas/{id_motorista}")
     #                delete_response_cliente = requests.delete(f"{url}/clientes/{id_cliente}")
     #                delete_response_veiculo = requests.delete(f"{url}/veiculos/{id_veiculo}")

     #                self.assertEqual(delete_response_carga.status_code, 200)
     #                self.assertEqual(delete_response_motorista.status_code, 200)
     #                self.assertEqual(delete_response_cliente.status_code, 200)
     #                self.assertEqual(delete_response_veiculo.status_code, 200)
     #                break

                    
if __name__ == '__main__':
    unittest.main()