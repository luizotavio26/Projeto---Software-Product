import unittest
import requests

url = "http://127.0.0.1:5036"

class TestMotoristaControle(unittest.TestCase):
     def test_01_criar_motorista(self):
     #              nome = motorista["nome"],
     #    cpf = motorista["cpf"], 
     #    rg = motorista["rg"],
     #    salario = motorista["salario"],
     #    data_nascimento = motorista['data_nascimento'],
     #    numero_cnh = motorista["numero_cnh"],
     #    categoria_cnh = motorista["categoria_cnh"],
     #    validade_cnh = motorista["validade_cnh"], 
     #    telefone = motorista["telefone"],
     #    email = motorista["email"],
     #    endereco = motorista["endereco"],
     #    cidade = motorista["cidade"], 
     #    uf = motorista["uf"],
     #    cep = motorista["cep"]
     
          payload ={
  "bairro": "Jardim das Acácias",
  "categoria_cnh": "E",
  "cep": "04567-123",
  "cidade": "São Paulo",
  "complemento": "Apartamento 302",
  "cpf": "123.456.789-10",
  "data_nascimento": "1988-05-14",
  "email": "mario.souza@example.com",
  "estado": "SP",
  "id": 1,
  "logradouro": "Rua Santa Beatriz",
  "nome": "Mário Souza",
  "numero": "455",
  "numero_cnh": "98765432100",
  "rg": "45.678.912-3",
  "salario": 4200.50,
  "telefone": "11987654321",
  "usuario_id": 1,
  "validade_cnh": "2028-09-10"
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
               if motorista["cpf"] == "123.456.789-10":
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