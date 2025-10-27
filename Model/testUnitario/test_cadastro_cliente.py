import unittest
import requests

url = "http://127.0.0.1:5036"

class TestCadastroCliente(unittest.TestCase):
     
    def test_01_listar_clientes(self):
        response = requests.get(f"{url}/clientes")
        self.assertEqual(response.status_code, 200)

    def test_02_post_cadastro_cliente(self):
        payload = {
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

    def test_03_buscar_cliente_por_cnpj(self):
        cnpj = "12345678000190"
        response = requests.get(f"{url}/clientes")
        response = response.json()
        for cliente in response:
            if cliente["cnpj"] == cnpj:
                self.assertEqual(cliente["razao_social"], "Empresa Teste LTDA")

    def test_04_atualizar_cliente(self):
        cnpj = "12345678000190"
        response = requests.get(f"{url}/clientes")
        for cliente in response.json():
            if cliente["cnpj"] == cnpj:
                id_cliente = cliente["id"]
                cliente["razao_social"] = "Empresa Atualizada LTDA"
                response = requests.put(f"{url}/clientes/{id_cliente}", json=cliente)
                self.assertEqual(response.status_code, 200)

    def test_05_deletar_cliente(self):
        cnpj = "12345678000190"
        response = requests.get(f"{url}/clientes")
        for cliente in response.json():
            if cliente["cnpj"] == cnpj:
                id_cliente = cliente["id"]
                del_response = requests.delete(f"{url}/clientes/{id_cliente}")
                self.assertEqual(del_response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
