import requests
import sys, os
from fpdf import FPDF
from flask import make_response
from datetime import datetime
from config import url  # ajuste se necessário

# garante que o Python ache o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


def relatorioDeTodosMotoristas():
    class RelatorioMotoristas(FPDF):
        # Cabeçalho
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, "Relatório de Motoristas Colaboradores", ln=True, align="C")
            self.ln(5)

        # Rodapé
        def footer(self):
          self.set_y(-15)
          self.set_font("Arial", "I", 8)
          self.cell(0, 10 , "Relatório gerado automaticamente pelo sistema.")
          self.cell(0, 10, f"Página {self.page_no()}", align="C")

    # Cria o PDF
    pdf = RelatorioMotoristas()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    pdf.ln(5)
    pdf.cell(0, 10, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(5)
    pdf.cell(0 , 10, " Relatorio de custos mensais dos motoristas colaboradores " , ln=True, align="C")
    pdf.ln(10)

    # Cabeçalho da tabela
    pdf.set_font("Arial", "B",8)
    pdf.set_fill_color(200, 220, 255)
    colunas = ["Nome", "RG", "Categoria CNH", "Telefone", "Email","Salário",] 
    larguras = [40, 20, 25, 20, 50, 30]  # ajuste as larguras conforme o layout
    for titulo, largura in zip(colunas, larguras):
        pdf.cell(largura, 10, titulo, border=1, align="C", fill=True)
    pdf.ln()

    # Dados dos motoristas
    pdf.set_font("Arial", "", 8)
    response = requests.get(f"{url}/motoristas")
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

    # Total geral
    pdf.set_font("Arial", "B", 8)
    pdf.cell(sum(larguras) - larguras[-1]  , 10, "Total Geral:", border=1, align="R", fill=True)
    pdf.cell(larguras[-1], 10, f"R$ {salario_total:.2f}", border=1, align="C", fill=True)
    pdf.ln(15)

    # Gera o PDF em memória
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    # Retorna o PDF para download
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_motoristas.pdf"
    return response
