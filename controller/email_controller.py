from flask import Blueprint, request, jsonify
from model.envioEmail.enviarEmail import enviarEmailGmail

emailBuleprint = Blueprint('email', __name__)

@emailBuleprint.route("/envia/Email", methods=['POST'])
def enviaEmail():
    try:
        dados = request.get_json()
        
        destinatario = dados.get('destinatario')
        assunto = dados.get('assunto')
        mensagem = dados.get('mensagem')
        arquivo_base64 = dados.get('arquivo_base64')
        nome_arquivo = dados.get('arquivo_nome', 'documento.pdf')

        if not destinatario or not arquivo_base64:
            return jsonify({"erro": "Destinatário ou arquivo ausente"}), 400

        # 🔹 Decodifica o Base64 e salva o PDF temporariamente
        import base64, os

        os.makedirs("uploads", exist_ok=True)
        caminho_pdf = os.path.join("uploads", nome_arquivo)

        with open(caminho_pdf, "wb") as f:
            f.write(base64.b64decode(arquivo_base64))

        response = enviarEmailGmail(destinatario, assunto, mensagem, caminho_pdf)

        # Retorna sucesso
        return jsonify({
            "mensagem": "E-mail enviado com sucesso!",
            "arquivo_salvo": caminho_pdf,
            "resposta": response
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
