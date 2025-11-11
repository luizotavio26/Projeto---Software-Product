import os
import requests
from cryptography.fernet import Fernet
from email.message import EmailMessage
import smtplib
from email.mime.application import MIMEApplication

remetente = "trajetoexpress04@gmail.com"

key = b'vG1Ku_8qA1bO-eXUJq2R7u5dglZdrZlK0RHVobkBGls='
f = Fernet(key)

def enviarEmailGmail(destinatario, assunto, mensagem, caminho_anexo=None):
    # 🔹 Busca a senha codificada do serviço remoto
    response = requests.get("https://enviodeemail-8mof.onrender.com/pega/senha")
    senha_codificada = response.json()["senha"]
    senha_decodificada = f.decrypt(senha_codificada.encode()).decode()  # <== IMPORTANTE: encode() aqui

    # 🔹 Monta o e-mail
    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario
    msg.set_content(mensagem)

    # 🔹 Se o PDF foi salvo, anexa ao e-mail
    if caminho_anexo and os.path.exists(caminho_anexo):
        with open(caminho_anexo, "rb") as f_anexo:
            anexo = MIMEApplication(f_anexo.read(), _subtype="pdf")
            anexo.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(caminho_anexo)
            )
            msg.add_attachment(anexo)

    # 🔹 Envia
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remetente, senha_decodificada)
        smtp.send_message(msg)

    return {"status": "E-mail enviado", "destinatario": destinatario}
