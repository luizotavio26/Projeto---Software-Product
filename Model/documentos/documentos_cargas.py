import requests
import sys
import os
from fpdf import FPDF
from flask import make_response
from datetime import datetime
from config import url

# Garante que o Python ache o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


def relatorioDeTodasCargas():
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

    # Cria o PDF
    pdf = RelatorioDeTodasCargas()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 10, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, "Relatório de Cargas Existentes", ln=True, align="C")
    pdf.ln(10)

    # Cabeçalho da tabela
    pdf.set_font("Arial", "B", 8)
    pdf.set_fill_color(200, 220, 255)
    colunas = ["Cliente", "Motorista", "Veículo", "Distância", "Origem", "Destino", "Valor KM", "Tipo de Carga"]
    larguras = [30, 30, 25, 25, 35, 35, 20, 25]

    for titulo, largura in zip(colunas, larguras):
        pdf.cell(largura, 10, titulo, border=1, align="C", fill=True)
    pdf.ln()

    # Corpo da tabela
    pdf.set_font("Arial", "", 8)
    try:
        response = requests.get(f"{url}/cargas")
        response.raise_for_status()
        cargas = response.json()
    except requests.RequestException as e:
        pdf.cell(0, 10, f"Erro ao obter cargas: {e}", ln=True)
        cargas = []

    if not cargas:
        pdf.cell(0, 10, "Nenhuma carga encontrada.", ln=True)
    else:
        for carga in cargas:
            # Busca os dados relacionados
            try:
                cliente_id = carga["cliente_id"]
                motorista_id = carga["motorista_id"]
                veiculo_id = carga["veiculo_id"]

                cliente = requests.get(f"{url}/clientes/{cliente_id}").json()
                motorista = requests.get(f"{url}/motoristas/{motorista_id}").json()
                veiculo = requests.get(f"{url}/veiculos/{veiculo_id}").json()

                nome_cliente = cliente.get("razao_social", "N/A")
                nome_motorista = motorista.get("nome", "N/A")
                placa_veiculo = veiculo.get("placa", "N/A")

                pdf.cell(larguras[0], 10, nome_cliente, border=1, align="C")
                pdf.cell(larguras[1], 10, nome_motorista, border=1, align="C")
                pdf.cell(larguras[2], 10, placa_veiculo, border=1, align="C")
                pdf.cell(larguras[3], 10, str(carga.get("distancia", "")), border=1, align="C")
                pdf.cell(larguras[4], 10, carga.get("origem_carga", ""), border=1, align="C")
                pdf.cell(larguras[5], 10, carga.get("destino_carga", ""), border=1, align="C")
                pdf.cell(larguras[6], 10, str(carga.get("valor_km", "")), border=1, align="C")
                pdf.cell(larguras[7], 10, carga.get("tipo_carga", ""), border=1, align="C")
                pdf.ln()

            except Exception as e:
                pdf.cell(0, 10, f"Erro ao processar carga: {e}", ln=True)

    # Gera o PDF em memória
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    # Retorna o PDF para download
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_de_cargas.pdf"
    return response
