import os
import requests
from cryptography.fernet import Fernet
from email.message import EmailMessage
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

remetente = "trajetoexpress04@gmail.com"

key = b'vG1Ku_8qA1bO-eXUJq2R7u5dglZdrZlK0RHVobkBGls='
f = Fernet(key)

# link TESTE para enviar pelo email. Vai ser ele que vai redirecionar para mudança de senha
pagina_redefinir_senha = "http://localhost:3000/redefinirsenha"

def emailSenhaEsquecida(nome_cliente, email_user):
    response = requests.get("https://enviodeemail-8mof.onrender.com/pega/senha")
    senha_codificada = response.json()["senha"]
    senha_decodificada = f.decrypt(senha_codificada.encode()).decode()  # <== IMPORTANTE: encode() aqui

    email = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Redefinição de Senha - Trajetto Express</title>
    </head>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1e90ff;">Olá, {nome_cliente}!</h2>

        <p>
            Recebemos uma solicitação para redefinir a senha da sua conta
            <strong>Trajetto Express</strong>.
        </p>

        <p>
            Para criar uma nova senha, clique no botão abaixo. Este link é válido por
            <strong>15 minutos</strong>.
        </p>

        <p style="text-align: center; margin: 30px 0;">
            <a href="{pagina_redefinir_senha}"
            style="background-color: #1e90ff; color: white; padding: 12px 24px;
                    text-decoration: none; border-radius: 6px;">
            Redefinir minha senha
            </a>
        </p>

        <p>
            Se você não solicitou a redefinição, ignore este e-mail.
            Sua senha atual permanecerá a mesma.
        </p>

        <hr style="margin: 30px 0;">
        <p style="font-size: 14px; color: #777;">
            Este e-mail foi enviado automaticamente. Não responda.
            <br>
            © 2025 Trajetto Express. Todos os direitos reservados.
        </p>
        </div>
    </body>
    </html>
    """



    try:
        print("Preparando o e-mail, aguarde.")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remetente, senha_decodificada)
            smtp.send_message(email)

        return {"status": "E-mail enviado", "destinatario": destinatario}

    except Exception as e:
        print(f"Erro ao enviar email: {e}")