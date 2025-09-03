from config import app,db
from flask_restx import Api
from Controller.manifesto_carga_controller import manifesto_cargas_blueprint
app.register_blueprint(manifesto_cargas_blueprint)

if __name__ == "__main__":
    with app.app_context():
        if app.config['DEBUG']:
            db.create_all()


    app.run(
        
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )
    