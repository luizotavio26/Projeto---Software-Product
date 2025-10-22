from flask import render_template
from config import app,db
from Controller.manifesto_carga_controller import manifesto_cargas_blueprint
from Controller.cadastro_cliente_controller import cadastro_clientes_blueprint
from Controller.cadastro_veiculos_controller import cadastro_veiculos_blueprint
from Controller.motorista_controller import motoristas_blueprint
from Controller.documentos_controller import documentos as documentos_blueprint
from flask_cors import CORS
import os

CORS(app)

app.register_blueprint(manifesto_cargas_blueprint)
app.register_blueprint(cadastro_clientes_blueprint)
app.register_blueprint(cadastro_veiculos_blueprint)
app.register_blueprint(motoristas_blueprint)
app.register_blueprint(documentos_blueprint)


@app.route("/manifesto")
def manifesto():
    return render_template("manifesto_carga.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro_cliente.html")

@app.route("/veiculo")
def veiculo():
    return render_template("cadastro_veiculo.html")

@app.route("/")
@app.route("/motorista")
def motorista():
    return render_template("cadastro_motorista.html")



if __name__ == "__main__":
    with app.app_context():
        if app.config['DEBUG']:
            db.create_all()


    app.run(
        
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )
    