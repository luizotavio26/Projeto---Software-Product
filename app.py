from flask import Flask 
from controle import *
# from bancoS import banco2


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(url)

# banco2(app)


if __name__ == "__main__":
    app.run(debug=True)