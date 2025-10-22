from flask import Flask, make_response
from fpdf import FPDF

app = Flask(__name__)

@app.route("/download-pdf")
def download_pdf():
    # Cria o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Olá João! Este é seu PDF gerado com FPDF.", ln=True, align="C")

    # Gera o PDF como bytes (sem salvar)
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    # Cria a resposta HTTP para download
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=meu_documento.pdf"
    return response

if __name__ == "__main__":
    app.run(debug=True)
