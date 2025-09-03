from flask import Flask, jsonify
from sqlalchemy import create_engine, text 
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

def versaoBD(url):
     try:
          engine = create_engine(url)
          with engine.connect() as con:
               result = con.execute(text("SELECT version();"))
               version = result.fetchone()[0]
          return jsonify({"version": version})
     except Exception as e:
          return jsonify({"error": str(e)}), 500

def consulta(url):
     try:
          engine = create_engine(url)
          with engine.connect() as con:
               result = con.execute(text("SELECT * FROM clientes"))
               clientes = []
               for row in result.fetchall():
                    clientes.append({"id": row[0], "nome": row[1], "idade": row[2]})
          return jsonify(clientes)
     except Exception as e:
          return jsonify({"error": str(e)}), 500
