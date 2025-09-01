import psycopg2
from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
load_dotenv()

try:
    conn = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()
    print("Conexão bem-sucedida ao PostgreSQL remoto!")
    
    response = cursor.execute("SELECT version();")
    print("\n Versão do PostgreSQL:", cursor.fetchone())
    
    response = cursor.execute("SELECT * FROM clientes")
    for row in cursor.fetchall():
         print(row)

    

except psycopg2.Error as e:
    print(f"Erro ao conectar ao PostgreSQL: {e}")

finally:
    if conn:
        cursor.close()
        conn.close()
        print("Conexão encerrada.")
