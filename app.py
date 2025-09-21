from config import app,db, render_template
from Controller.manifesto_carga_controller import manifesto_cargas_blueprint
from Controller.cadastro_usuario_controleler import cadastro_usuarios
from Controller.upload_controller import upload_bp
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

CORS(app)

app.register_blueprint(manifesto_cargas_blueprint)
app.register_blueprint(cadastro_usuarios)
app.register_blueprint(upload_bp)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload")
def pagina_upload():
    return render_template("upload_doc.html")

@app.route("/")
def home():
    return render_template("manifesto_carga.html") 

if __name__ == "__main__":
    with app.app_context():
        if app.config['DEBUG']:
            db.create_all()


    app.run(
        
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )
    