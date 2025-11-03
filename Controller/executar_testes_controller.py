from flask import Blueprint, request, jsonify
import sys
import os
from io import StringIO
import unittest
from model.testUnitario.test_cadastro_cliente import *
from model.testUnitario.test_cadastro_veiculos import *
from model.testUnitario.test_motorista_controle import *
from model.testUnitario.test_manifesto_carga import *

def padronizar(Classe):
      # 1️⃣ Cria a suite apenas com os testes da classe TestCadastroCliente
     suite = unittest.TestLoader().loadTestsFromTestCase(Classe)
     
      # 2️⃣ Usa StringIO para capturar a saída detalhada do runner
     output_stream = StringIO()
     runner = unittest.TextTestRunner(stream=output_stream, verbosity=2)
     
     # 3️⃣ Executa a suite
     result = runner.run(suite)

      # 4️⃣ Organiza resultados detalhados por teste
     detalhes_testes = []

     # Testes que falharam
     for teste, traceback in result.failures:
          detalhes_testes.append({
               "teste": str(teste),
               "status": "Falhou",
               "mensagem": traceback
          })

     # Testes que deram erro (exceção)
     for teste, traceback in result.errors:
          detalhes_testes.append({
               "teste": str(teste),
               "status": "Erro",
               "mensagem": traceback
          })

     # Testes que passaram
     nomes_testes_passaram = [
          str(teste) for teste in suite
          if all(str(teste) != str(f[0]) for f in result.failures)
          and all(str(teste) != str(e[0]) for e in result.errors)
     ]
     for teste in nomes_testes_passaram:
          detalhes_testes.append({
               "teste": teste,
               "status": "Sucesso",
               "mensagem": ""
          })

     # 5️⃣ Retorna o JSON completo
     return {
          "executados": result.testsRun,
          "falhas": len(result.failures),
          "erros": len(result.errors),
          "sucesso": result.wasSuccessful(),
          "detalhes": detalhes_testes,
          "saida_texto": output_stream.getvalue()  # saída completa do runner (opcional)
     }
     


testes_blueprint = Blueprint('testes', __name__)

@testes_blueprint.route('/executar_testes', methods=['GET'])
def executar_testes():
     return jsonify({"message": "Execução de testes iniciada"}), 200

@testes_blueprint.route('/executar_testes/clientes', methods=['GET'])
def executar_testes_clientes():
     return jsonify(padronizar(TestCadastroCliente))
    
@testes_blueprint.route('/executar_testes/veiculos', methods=['GET'])
def executar_testes_veiculos():      
    return jsonify(padronizar(TestCadastroVeiculos))
     
@testes_blueprint.route('/executar_testes/motoristas', methods=['GET'])
def executar_testes_motoristas():     
   return jsonify(padronizar(TestMotoristaControle))
     
@testes_blueprint.route('/executar_testes/manifesto', methods=['GET'])
def executar_testes_manifesto():
     return jsonify(padronizar(TestManifestoCarga))

@testes_blueprint.route('/executar_testes/geral', methods=['GET'])
def executar_testes_geral():
     return jsonify({
     "TesteClientes": padronizar(TestCadastroCliente),
     "TesteVeiculos": padronizar(TestCadastroVeiculos),
     "TesteMotoristas": padronizar(TestMotoristaControle),
     "TesteManifestoCarga": padronizar(TestManifestoCarga)
     })

@testes_blueprint.route('/executar_testes/geral_remoto', methods=['GET'])
def executar_testes_geral_remoto():
     url = "https://trajettoexpressfullstack.onrender.com"
     return jsonify({
     "TesteClientes": padronizar(TestCadastroCliente),
     "TesteVeiculos": padronizar(TestCadastroVeiculos),
     "TesteMotoristas": padronizar(TestMotoristaControle),
     "TesteManifestoCarga": padronizar(TestManifestoCarga)
     })

    