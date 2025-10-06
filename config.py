from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://softwareproduct_user:MTgr4L632k0Aj2ShsOh7Ec0swJSouQ9w@dpg-d3036sripnbc73fpqrsg-a.oregon-postgres.render.com/softwareproduct"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)