
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail
from flask_cors import CORS

app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5036
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://trajetto_e29t_user:JHSE8jRaGAWFmUCydqLzHCoPvApdgDLP@dpg-d85pg6rbc2fs73f1vngg-a.oregon-postgres.render.com/trajetto_e29t"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

porta = app.config['PORT']
host = app.config['HOST']


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'trajetto.contato@gmail.com'
app.config['MAIL_PASSWORD'] = 'qnlgiytnkjpovrlg'
app.config['MAIL_DEFAULT_SENDER'] = 'trajetto.contato@gmail.com'

mail = Mail(app)


app.config["SECRET_KEY"] = "trajetto_express"

if host == "0.0.0.0":
    host = "localhost"

url = f"http://{host}:{porta}"


db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5036)))