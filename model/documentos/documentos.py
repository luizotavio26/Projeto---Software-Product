import requests
import sys
import os
from fpdf import FPDF
from flask import make_response
from datetime import datetime
from config import url
import base64
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

def decode_jwt(token: str):
    try:
        header, payload, signature = token.split('.')

        def pad(b):
            return b + '=' * (-len(b) % 4)

        header_decoded = json.loads(base64.urlsafe_b64decode(pad(header)))
        payload_decoded = json.loads(base64.urlsafe_b64decode(pad(payload)))

        return {
            "header": header_decoded,
            "payload": payload_decoded,
            "signature": signature
        }
    except Exception as e:
        return {"error": str(e)}

def visualizarToken(token):
    print(json.dumps(token, indent=4))

def pegaID(token):
    id_usuario = token["payload"]["id_usuario"]
    return id_usuario


def visualizarToken(token):
    print(json.dumps(token, indent=4))

#--------------------------------------------------------------------------------------------------
# DOCUMENTOS DAS CARGAS
#--------------------------------------------------------------------------------------------------
def relatorioDeTodasCargas(token):
    class RelatorioDeTodasCargas(FPDF):
        def header(self):
            """Cabeçalho"""
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "Relatório de Todas as Cargas", ln=True, align="C")
            self.ln(5)

        def footer(self):
            """Rodapé"""
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, "Relatório gerado automaticamente pelo sistema.", align="L")
            self.cell(0, 10, f"Página {self.page_no()}", align="R")

    pdf = RelatorioDeTodasCargas()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 10, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, "Relatório de Cargas Existentes", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 7)
    pdf.set_fill_color(200, 220, 255)
    colunas = [ "Motorista", "Veículo", "Distância", "Origem", "Destino", "Valor KM", "Tipo de Carga"]
    larguras = [ 28, 22,15, 40, 45, 15, 20]

    for titulo, largura in zip(colunas, larguras):
        pdf.cell(largura, 10, titulo, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Arial", "", 7)
    try:
        dados = decode_jwt(token)
        id_usuario = pegaID(dados)
        response = requests.get(f"{url}/cargas/cargasCadastradas/{id_usuario}")
        response.raise_for_status()
        dados = response.json()
        cargas = dados.get("Cargas", [])
    except requests.RequestException as e:
        pdf.cell(0, 10, f"Erro ao obter cargas: {e}", ln=True)
        cargas = []

    if not cargas:
        pdf.cell(0, 10, "Nenhuma carga encontrada.", ln=True)
    else:
        for carga in cargas:
            try:
                motorista_nome = carga["motorista"]
                placa_veiculo = carga["veiculo"]

                pdf.cell(larguras[0], 10, motorista_nome, border=1, align="C")
                pdf.cell(larguras[1], 10, placa_veiculo, border=1, align="C")
                pdf.cell(larguras[2], 10, str(carga.get("distancia", "")), border=1, align="C")
                pdf.cell(larguras[3], 10, carga.get("origem_carga", ""), border=1, align="C")
                pdf.cell(larguras[4], 10, carga.get("destino_carga", ""), border=1, align="C")
                pdf.cell(larguras[5], 10, str(carga.get("valor_km", "")), border=1, align="C")
                pdf.cell(larguras[6], 10, carga.get("tipo_carga", ""), border=1, align="C")
                pdf.ln()

            except Exception as e:
                pdf.cell(0, 10, f"Erro ao processar carga: {e}", ln=True)

    pdf_bytes = pdf.output(dest="S").encode("latin1")

    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_de_cargas.pdf"
    return response


   
#--------------------------------------------------------------------------------------------------
# DOCUMENTOS DOS MOTORISTAS - RELATÓRIO
#--------------------------------------------------------------------------------------------------
def relatorioDeTodosMotoristas(token):
    class RelatorioMotoristas(FPDF):
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "Relatório de Motoristas Colaboradores", ln=True, align="C")
            self.ln(5)

        def footer(self):
          self.set_y(-15)
          self.set_font("Arial", "I", 8)
          self.cell(0, 10 , "Relatório gerado automaticamente pelo sistema.")
          self.cell(0, 10, f"Página {self.page_no()}", align="C")

    pdf = RelatorioMotoristas()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    pdf.ln(5)
    pdf.cell(0, 10, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(5)
    pdf.cell(0 , 10, " Relatorio de custos mensais dos motoristas colaboradores " , ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B",8)
    pdf.set_fill_color(200, 220, 255)
    colunas = ["Nome", "RG", "Categoria CNH", "Telefone", "Email","Salário",] 
    larguras = [40, 20, 25, 20, 50, 30]  # ajuste as larguras conforme o layout
    for titulo, largura in zip(colunas, larguras):
        pdf.cell(largura, 10, titulo, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Arial", "", 8)
    dados = decode_jwt(token)
    id_usuario = pegaID(dados)
    response = requests.get(f"{url}/cargas/motoristasCadastrados/{id_usuario}")
    motoristas = response.json()
    salario_total = 0

    for motorista in motoristas:
        salario_total += float(motorista["salario"])

        pdf.cell(larguras[0], 10, motorista["nome"], border=1, align="C")
        pdf.cell(larguras[1], 10, motorista["rg"], border=1, align="L")
        pdf.cell(larguras[2], 10, motorista["categoria_cnh"], border=1 , align="L")
        pdf.cell(larguras[3], 10, motorista["telefone"], border=1 , align="L")
        pdf.cell(larguras[4], 10, motorista["email"], border=1 , align="L")
        pdf.cell(larguras[5], 10, f"R$ {motorista['salario']}", border=1, align="C" )
        pdf.ln()

    pdf.set_font("Arial", "B", 8)
    pdf.cell(sum(larguras) - larguras[-1]  , 10, "Total Geral:", border=1, align="R", fill=True)
    pdf.cell(larguras[-1], 10, f"R$ {salario_total:.2f}", border=1, align="C", fill=True)
    pdf.ln(15)

    pdf_bytes = pdf.output(dest="S").encode("latin1")

    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_motoristas.pdf"
    return response

#--------------------------------------------------------------------------------------------------
# DOCUMENTOS DOS VEÍCULOS - RELATÓRIO
#--------------------------------------------------------------------------------------------------
def relatorioDeTodosVeiculos(token):
    class RelatorioVeiculos(FPDF):
        def header(self):
            """Cabeçalho do PDF"""
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "Relatório de Veículos", ln=True, align="C")
            self.ln(5)

        def footer(self):
            """Rodapé do PDF"""
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, "Relatório gerado automaticamente pelo sistema.", align="L")
            self.cell(0, 10, f"Página {self.page_no()}", align="R")

    pdf = RelatorioVeiculos()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 10, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, "Relatório de Todos os Veículos Existentes", ln=True, align="C")
    pdf.ln(10)

    colunas = ["ID", "Placa", "Modelo", "Marca", "Tipo", "Ano Modelo"]
    larguras = [15, 30, 35, 35, 35, 30]

    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(200, 220, 255)
    for titulo, largura in zip(colunas, larguras):
        pdf.cell(largura, 10, titulo, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    try:
        dados = decode_jwt(token)
        id_usuario = pegaID(dados)
        response = requests.get(f"{url}/cargas/veiculosCadastrados/{id_usuario}")
        response.raise_for_status()
        veiculos = response.json()
        
    except requests.RequestException as e:
        pdf.cell(0, 10, f"Erro ao obter dados: {e}", ln=True)
        veiculos = []

    if not veiculos:
        pdf.cell(0, 10, "Nenhum veículo encontrado.", ln=True)
    else:
        for veiculo in veiculos:
            pdf.cell(larguras[0], 10, str(veiculo.get("id", "")), border=1, align="C")
            pdf.cell(larguras[1], 10, veiculo.get("placa", ""), border=1, align="C")
            pdf.cell(larguras[2], 10, veiculo.get("modelo", ""), border=1, align="C")
            pdf.cell(larguras[3], 10, veiculo.get("marca", ""), border=1, align="C")
            pdf.cell(larguras[4], 10, veiculo.get("tipo", ""), border=1, align="C")
            pdf.cell(larguras[5], 10, str(veiculo.get("ano_modelo", "")), border=1, align="C")
            pdf.ln()

    pdf_bytes = pdf.output(dest="S").encode("latin1")

    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_veiculos.pdf"
    return response



#--------------------------------------------------------------------------------------------------
# DOCUMENTOS DOS CLIENTES - RELATÓRIO
#--------------------------------------------------------------------------------------------------


def relatorioDeTodosClientes(token):
    class RelatorioClientes(FPDF):
        def header(self):
            """Cabeçalho do PDF"""
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "Relatório de Clientes Cadastrados", ln=True, align="C")
            self.ln(5)

        def footer(self):
            """Rodapé do PDF"""
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, "Relatório gerado automaticamente pelo sistema.", align="L")
            self.cell(0, 10, f"Página {self.page_no()}", align="R")

    pdf = RelatorioClientes()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 10, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, "Relatório de Todos os Clientes Existentes", ln=True, align="C")
    pdf.ln(10)

    colunas = ["Razão Social", "CNPJ", "Telefone", "Email", "Cidade", "Estado"]
    larguras = [50, 30, 25, 45, 25, 15]

    pdf.set_font("Arial", "B", 8)
    pdf.set_fill_color(200, 220, 255)
    for titulo, largura in zip(colunas, larguras):
        pdf.cell(largura, 10, titulo, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Arial", "", 8)
    try:
        dados = decode_jwt(token)
        id_usuario = pegaID(dados)
        response = requests.get(f"{url}/cargas/clientesCadastrados/{id_usuario}")
        response.raise_for_status()
        
        clientes = response.json()


    except requests.RequestException as e:
        pdf.cell(0, 10, f"Erro ao obter dados dos clientes: {e}", ln=True)
        clientes = []

    if not clientes:
        pdf.cell(0, 10, "Nenhum cliente encontrado.", ln=True)
    else:
        for cliente in clientes:
            pdf.cell(larguras[0], 10, cliente.get("razao_social", ""), border=1, align="L")
            pdf.cell(larguras[1], 10, cliente.get("cnpj", ""), border=1, align="C")
            pdf.cell(larguras[2], 10, cliente.get("telefone", ""), border=1, align="C")
            pdf.cell(larguras[3], 10, cliente.get("email", ""), border=1, align="L")
            pdf.cell(larguras[4], 10, cliente.get("cidade", ""), border=1, align="C")
            pdf.cell(larguras[5], 10, cliente.get("estado", ""), border=1, align="C")
            pdf.ln()

    pdf_bytes = pdf.output(dest="S").encode("latin1")

    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_clientes.pdf"
    return response







