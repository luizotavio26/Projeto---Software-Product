from flask import render_template
from config import app,db
from Controller.manifesto_carga_controller import manifesto_cargas_blueprint
from Controller.cadastro_usuario_controller import cadastro_usuarios_blueprint
from Controller.upload_controller import upload_bp
from flask_cors import CORS
import os

CORS(app)

app.register_blueprint(manifesto_cargas_blueprint)
app.register_blueprint(cadastro_usuarios_blueprint)
app.register_blueprint(upload_bp)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload")
def pagina_upload():
    return render_template("upload_doc.html")


@app.route("/manifestocargas")
def manifesto():
    return render_template("manifesto_carga.html")


@app.route("/clientes")
def clientes():
    return render_template("cadastro_cliente.html")


if __name__ == "__main__":
    with app.app_context():
        if app.config['DEBUG']:
            db.create_all()


    app.run(
        
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )
    