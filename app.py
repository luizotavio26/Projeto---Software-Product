from config import app,db, render_template
from flask_restx import Api
from Controller.manifesto_carga_controller import manifesto_cargas_blueprint
from flask_cors import CORS

CORS(app)

app.register_blueprint(manifesto_cargas_blueprint)

@app.route("/")  # quando acessar http://localhost:5036/
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
    