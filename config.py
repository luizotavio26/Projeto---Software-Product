from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://softwareproduct_xrs3_user:WJsq91vv1YGPOsx9xsmZLxAPwuHzrdW9@dpg-d414ksruibrs73cubnr0-a.oregon-postgres.render.com/softwareproduct_xrs3"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)