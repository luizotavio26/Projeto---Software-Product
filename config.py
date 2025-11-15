from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://teste_t2tl_user:ApbeKIlHYqnhGizRKEayIpZsQ8IkurY0@dpg-d4cdk4bipnbc739de8d0-a.oregon-postgres.render.com/teste_t2tl"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

porta = app.config['PORT']
host = app.config['HOST']

if host == "0.0.0.0":
    host = "localhost"

url = f"http://{host}:{porta}"

# url = "https://trajettoexpressfullstack.onrender.com"

db = SQLAlchemy(app)