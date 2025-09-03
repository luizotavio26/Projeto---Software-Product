# controle2.py
from flask import Blueprint, jsonify
from controller.etx import db  # <- agora importa só o db, sem precisar importar o app

url2 = Blueprint("run2", __name__)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    idade = db.Column(db.String(50))
    nome = db.Column(db.String(50))
    
class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    preco = db.Column(db.String(50))


@url2.route('/c2', methods=['GET'])
def get_clientes2():
    clientes = Cliente.query.all()
    resultado = []
    for c in clientes:
        resultado.append({"id": c.id, "idade": c.idade ,"nome": c.nome})
    return jsonify(resultado)


@url2.route('/deletar_tabela', methods=['DELETE','GET'])
def drop_clientes_table():
    try:
        Cliente.__table__.drop(db.engine)  # apaga a tabela 'clientes' do banco
        return jsonify({"message": "Tabela deletada com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@url2.route('/criar_tabela', methods=['GET'])
def criar_tabela_clientes():
    try:
        db.create_all()
        return jsonify({"mensagem": "Tabela criada com sucesso (se ainda não existia)."}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@url2.route('/inserir_dados_fake', methods=['POST','GET'])
def inserir_dados_ficticios():
    try:
        # Criar clientes fictícios
        cliente1 = Cliente(nome="Maria", idade="28")
        cliente2 = Cliente(nome="João", idade="35")
        cliente3 = Cliente(nome="Ana", idade="22")

        # Criar produtos fictícios
        produto1 = Produto(nome="Camiseta", preco="49.90")
        produto2 = Produto(nome="Tênis", preco="199.90")
        produto3 = Produto(nome="Calça Jeans", preco="129.90")

        # Adiciona todos à sessão
        db.session.add_all([cliente1, cliente2, cliente3, produto1, produto2, produto3])
        db.session.commit()

        return jsonify({"mensagem": "Dados fictícios inseridos com sucesso."}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500
