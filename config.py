from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://trajetto_user:L2fB20b5gJqQh8mdTP7YXgIS4ucbinEy@dpg-d4cda9gdl3ps73be9cf0-a.oregon-postgres.render.com/trajetto"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

porta = app.config['PORT']
host = app.config['HOST']

if host == "0.0.0.0":
    host = "localhost"

url = f"http://{host}:{porta}"

# url = "https://trajettoexpressfullstack.onrender.com"

db = SQLAlchemy(app)