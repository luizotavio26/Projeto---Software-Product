from flask import Flask 
from controller.controle import *
from controller.controle2 import url2
from controller.etx import db
import os
from dotenv import load_dotenv

load_dotenv()

url_bd = os.getenv("DB_URL")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url_bd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # necessário
app.register_blueprint(url)
app.register_blueprint(url2)

if __name__ == "__main__":
    app.run(debug=True)
