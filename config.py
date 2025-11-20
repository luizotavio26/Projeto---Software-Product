from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://trajetto_04ep_user:g4ijPopj5IyvlDYBbzSb41RfXzUXtSKh@dpg-d4f6jsq4d50c73e0o980-a.oregon-postgres.render.com/trajetto_04ep"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

porta = app.config['PORT']
host = app.config['HOST']

# para o token
app.config["SECRET_KEY"] = "trajetto_express"

if host == "0.0.0.0":
    host = "localhost"

url = f"http://{host}:{porta}"

# url = "https://trajettoexpressfullstack.onrender.com"

db = SQLAlchemy(app)