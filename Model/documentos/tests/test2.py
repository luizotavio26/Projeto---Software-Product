from flask import Flask, make_response
from fpdf import FPDF
from datetime import datetime

app = Flask(__name__)

class RelatorioPDF(FPDF):
    # Cabeçalho do PDF
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Relatório de Motoristas", ln=True, align="C")
        self.ln(5)
        self.set_font("Arial", "", 10)
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(0, 10, f"Gerado em: {data}", ln=True, align="R")
        self.ln(5)
        self.line(10, 30, 200, 30)  # linha horizontal

    # Rodapé do PDF
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

@app.route("/relatorio")
def gerar_relatorio():
    # Dados simulados (você pode substituir por dados reais do banco)
    motoristas = [
        {"nome": "João Silva", "cpf": "123.456.789-00", "cidade": "São Paulo"},
        {"nome": "Maria Souza", "cpf": "987.654.321-00", "cidade": "Rio de Janeiro"},
        {"nome": "Pedro Santos", "cpf": "111.222.333-44", "cidade": "Belo Horizonte"},
        {"nome": "Ana Costa", "cpf": "555.666.777-88", "cidade": "Curitiba"},
    ]

    # Criação do PDF
    pdf = RelatorioPDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    # Cabeçalhos da tabela
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(60, 10, "Nome", border=1, align="C", fill=True)
    pdf.cell(60, 10, "CPF", border=1, align="C", fill=True)
    pdf.cell(60, 10, "Cidade", border=1, align="C", fill=True)
    pdf.ln()

    # Linhas de dados
    for m in motoristas:
        pdf.cell(60, 10, m["nome"], border=1)
        pdf.cell(60, 10, m["cpf"], border=1)
        pdf.cell(60, 10, m["cidade"], border=1)
        pdf.ln()

    # Gera o PDF em memória
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    # Retorna para download
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_motoristas.pdf"
    return response

if __name__ == "__main__":
    app.run(debug=True)
