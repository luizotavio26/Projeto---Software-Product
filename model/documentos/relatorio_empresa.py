import sys, os
from fpdf import FPDF
from flask import make_response
from datetime import datetime

# garante que o Python ache o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


def gerarRelatorioEmpresa():
    class RelatorioEmpresa(FPDF):
        # Cabeçalho do PDF
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "Relatório Financeiro da Empresa", ln=True, align="C")
            self.ln(5)

        # Rodapé do PDF
        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, "Gerado automaticamente pelo sistema TrajettoExpress.", align="L")
            self.cell(0, 10, f"Página {self.page_no()}", align="R")

    # -------------------------------
    # DADOS DE EXEMPLO
    # -------------------------------
    dados = [
        {"mes": "Janeiro", "faturamento": 120000.00, "gastos": 85000.00},
        {"mes": "Fevereiro", "faturamento": 98000.00, "gastos": 72000.00},
        {"mes": "Março", "faturamento": 134000.00, "gastos": 93000.00},
        {"mes": "Abril", "faturamento": 142000.00, "gastos": 87000.00},
        {"mes": "Maio", "faturamento": 150000.00, "gastos": 91000.00},
    ]

    total_faturamento = sum(item["faturamento"] for item in dados)
    total_gastos = sum(item["gastos"] for item in dados)
    lucro_total = total_faturamento - total_gastos

    # -------------------------------
    # GERAÇÃO DO PDF
    # -------------------------------
    pdf = RelatorioEmpresa()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 10, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, "Resumo de desempenho financeiro por mês", ln=True, align="C")
    pdf.ln(10)

    # Cabeçalho da tabela
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(50, 10, "Mês", border=1, align="C", fill=True)
    pdf.cell(60, 10, "Faturamento (R$)", border=1, align="C", fill=True)
    pdf.cell(60, 10, "Gastos (R$)", border=1, align="C", fill=True)
    pdf.ln()

    # Linhas da tabela
    pdf.set_font("Arial", "", 11)
    for item in dados:
        pdf.cell(50, 10, item["mes"], border=1, align="C")
        pdf.cell(60, 10, f"{item['faturamento']:,.2f}", border=1, align="R")
        pdf.cell(60, 10, f"{item['gastos']:,.2f}", border=1, align="R")
        pdf.ln()

    # Totais
    pdf.set_font("Arial", "B", 11)
    pdf.cell(50, 10, "Totais", border=1, align="C", fill=True)
    pdf.cell(60, 10, f"{total_faturamento:,.2f}", border=1, align="R", fill=True)
    pdf.cell(60, 10, f"{total_gastos:,.2f}", border=1, align="R", fill=True)
    pdf.ln(10)

    # Lucro total
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, f"Lucro Total: R$ {lucro_total:,.2f}", ln=True, align="C")

    # -------------------------------
    # EXPORTAÇÃO E RETORNO
    # -------------------------------
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_empresa.pdf"

    return response



