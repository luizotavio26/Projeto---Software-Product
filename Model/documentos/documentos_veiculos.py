import requests
import sys
import os
from fpdf import FPDF
from flask import make_response
from datetime import datetime
from config import url  # Certifique-se que esse import está correto

# Garante que o Python encontre o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


def relatorioDeTodosVeiculos():
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

    # Cria o PDF
    pdf = RelatorioVeiculos()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    # Informações iniciais
    pdf.cell(0, 10, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, "Relatório de Todos os Veículos Existentes", ln=True, align="C")
    pdf.ln(10)

    # Cabeçalho da tabela
    colunas = ["ID", "Placa", "Modelo", "Marca", "Tipo", "Ano Modelo"]
    larguras = [15, 30, 35, 35, 35, 30]

    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(200, 220, 255)
    for titulo, largura in zip(colunas, larguras):
        pdf.cell(largura, 10, titulo, border=1, align="C", fill=True)
    pdf.ln()

    # Corpo da tabela
    pdf.set_font("Arial", "", 10)
    try:
        response = requests.get(f"{url}/veiculos")
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

    # Gera o PDF em memória (fora do loop!)
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    # Retorna o PDF para download
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_veiculos.pdf"
    return response
