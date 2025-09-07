from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://banco_joao_user:zu6a9cux2GZBMS6GhE2OMf4s8lD8efgY@dpg-d2qp6fv5r7bs73b1qlt0-a.oregon-postgres.render.com/banco_joao"

db = SQLAlchemy(app)