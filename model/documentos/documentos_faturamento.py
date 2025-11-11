import requests
import sys, os
from fpdf import FPDF
from flask import make_response
from datetime import datetime
from config import url  # ajuste se necessário

# garante que o Python ache o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

def relatorioEmpresa():

     class RelatorioCliente(FPDF):
     # Cabeçalho
          def header(self):
               self.set_font("Arial", "B", 16)
               self.cell(0, 10, "Relatório de Faturamento e Gastos", ln=True, align="C")
               self.ln(5)

          # Rodapé
          def footer(self):
               self.set_y(-15)
               self.set_font("Arial", "I", 8)
               self.cell(0, 10, "Relatório gerado automaticamente pelo sistema.")
               self.cell(0, 10, f"Página {self.page_no()}", align="C")

     # -------------------------------
     # DADOS DE EXEMPLO
     # -------------------------------
     dados = [
     {"mes": "Janeiro",   "faturamento": 125000.00, "gastos": 83000.00},
     {"mes": "Fevereiro", "faturamento": 98000.00,  "gastos": 72000.00},
     {"mes": "Março",     "faturamento": 140000.00, "gastos": 91000.00},
     {"mes": "Abril",     "faturamento": 117000.00, "gastos": 95000.00},
     ]

     # Cálculos de totais
     total_faturamento = sum(d["faturamento"] for d in dados)
     total_gastos = sum(d["gastos"] for d in dados)
     lucro_total = total_faturamento - total_gastos

     # -------------------------------
     # GERAÇÃO DO PDF
     # -------------------------------
     pdf = RelatorioCliente()
     pdf.add_page()
     pdf.set_font("Arial", "", 12)

     pdf.ln(5)
     pdf.cell(0, 10, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
     pdf.ln(5)
     pdf.cell(0, 10, "Relatório de Faturamento e Gastos da Companhia", ln=True, align="C")
     pdf.ln(10)

     # Cabeçalho da tabela
     pdf.set_font("Arial", "B", 11)
     pdf.set_fill_color(200, 220, 255)
     pdf.cell(50, 10, "Mês", border=1, align="C", fill=True)
     pdf.cell(60, 10, "Faturamento (R$)", border=1, align="C", fill=True)
     pdf.cell(60, 10, "Gastos (R$)", border=1, align="C", fill=True)
     pdf.ln()

     # Linhas da tabela
     pdf.set_font("Arial", "B", 11)
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

          # Lucro
          pdf.set_font("Arial", "B", 12)
          pdf.cell(0, 10, f"Lucro total: R$ {lucro_total:,.2f}", ln=True, align="C")

     # Gera o PDF em memória
     pdf_bytes = pdf.output(dest="S").encode("latin1")

     # Retorna o PDF para download
     response = make_response(pdf_bytes)
     response.headers["Content-Type"] = "application/pdf"
     response.headers["Content-Disposition"] = "attachment; filename=relatorio_Faturamento_Gastos.pdf"
     return response


