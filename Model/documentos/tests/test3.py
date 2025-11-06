from flask import Flask, make_response
from fpdf import FPDF
from datetime import datetime

app = Flask(__name__)

class RelatorioFaturamento(FPDF):
    # Cabeçalho
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Relatório de Faturamento", ln=True, align="C")
        self.ln(5)

    # Rodapé
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10 , "Relatório gerado automaticamente pelo sistema.")
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

@app.route("/faturamento")
def gerar_faturamento():
    # 🏢 Dados da empresa (exemplo)
    empresa = {
        "nome": "Tech Solutions LTDA",
        "cnpj": "12.345.678/0001-99",
        "endereco": "Av. Paulista, 1000 - São Paulo/SP"
    }

    # 💰 Dados de faturamento (exemplo)
    vendas = [
        {"item": "Desenvolvimento Web", "quantidade": 3, "valor_unitario": 1500.00},
        {"item": "Manutenção de Sistema", "quantidade": 2, "valor_unitario": 800.00},
        {"item": "Consultoria Técnica", "quantidade": 1, "valor_unitario": 1200.00},
        {"item": "Hospedagem e Suporte", "quantidade": 12, "valor_unitario": 150.00},
    ]

    # Criação do PDF
    pdf = RelatorioFaturamento()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    # Cabeçalho da empresa
    pdf.cell(0, 10, f"Empresa: {empresa['nome']}", ln=True)
    pdf.cell(0, 10, f"CNPJ: {empresa['cnpj']}", ln=True)
    pdf.cell(0, 10, f"Endereço: {empresa['endereco']}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(10)

    # Cabeçalhos da tabela
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(80, 10, "Serviço / Produto", border=1, align="C", fill=True)
    pdf.cell(30, 10, "Qtd", border=1, align="C", fill=True)
    pdf.cell(40, 10, "Valor Unitário", border=1, align="C", fill=True)
    pdf.cell(40, 10, "Total (R$)", border=1, align="C", fill=True)
    pdf.ln()

    # Linhas de dados
    pdf.set_font("Arial", "", 12)
    total_geral = 0
    for v in vendas:
        total = v["quantidade"] * v["valor_unitario"]
        total_geral += total
        pdf.cell(80, 10, v["item"], border=1)
        pdf.cell(30, 10, str(v["quantidade"]), border=1, align="C")
        pdf.cell(40, 10, f"R$ {v['valor_unitario']:.2f}", border=1, align="R")
        pdf.cell(40, 10, f"R$ {total:.2f}", border=1, align="R")
        pdf.ln()

    # Total geral
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, "Total Geral:", border=1, align="R", fill=True)
    pdf.cell(40, 10, f"R$ {total_geral:.2f}", border=1, align="R", fill=True)
    pdf.ln(15)

    pdf.set_font("Arial", "I", 11)
    pdf.cell(0, 10, "Relatório gerado automaticamente pelo sistema.", ln=True, align="C")

    # Gera o PDF em memória
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    # Retorna para download
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_faturamento.pdf"
    return response

if __name__ == "__main__":
    app.run(debug=True)
