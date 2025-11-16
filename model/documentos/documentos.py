import requests
import sys
import os
from fpdf import FPDF
from flask import make_response
from datetime import datetime
from config import url

# Garante que o Python ache o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

#--------------------------------------------------------------------------------------------------
# DOCUMENTOS DAS CARGAS
#--------------------------------------------------------------------------------------------------
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
    pdf.set_font("Arial", "B", 7)
    pdf.set_fill_color(200, 220, 255)
    colunas = [ "Motorista", "Veículo", "Distância", "Origem", "Destino", "Valor KM", "Tipo de Carga"]
    larguras = [ 28, 22,15, 40, 45, 15, 20]

    for titulo, largura in zip(colunas, larguras):
        pdf.cell(largura, 10, titulo, border=1, align="C", fill=True)
    pdf.ln()

    # Corpo da tabela
    pdf.set_font("Arial", "", 7)
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

    # Gera o PDF em memória
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    # Retorna o PDF para download
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_de_cargas.pdf"
    return response

#--------------------------------------------------------------------------------------------------
# DOCUMENTOS DAS EMPRESAS - FATURAMENTO
#--------------------------------------------------------------------------------------------------
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

#--------------------------------------------------------------------------------------------------
# DOCUMENTOS DOS MOTORISTAS - RELATÓRIO
#--------------------------------------------------------------------------------------------------
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

#--------------------------------------------------------------------------------------------------
# DOCUMENTOS DOS VEÍCULOS - RELATÓRIO
#--------------------------------------------------------------------------------------------------
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

#--------------------------------------------------------------------------------------------------
# DOCUMENTOS DA EMPRESA  - RELATÓRIO
#--------------------------------------------------------------------------------------------------
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






