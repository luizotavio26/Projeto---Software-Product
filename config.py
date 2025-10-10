from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://software_product_user:zXFrTtfRy6axGTP214ljH8IpHSgaZ3Hb@dpg-d3km73a4d50c73ddhm50-a.oregon-postgres.render.com/software_product"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)