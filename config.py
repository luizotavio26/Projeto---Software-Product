from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://new_bd_user:hICfEeEPi3AHPt95qeFnj2zKaMBbPnGa@dpg-d3hvssh5pdvs73fkak00-a.oregon-postgres.render.com/new_bd"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)