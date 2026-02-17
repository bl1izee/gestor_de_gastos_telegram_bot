import sqlite3 as sql
from datetime import datetime

def start_db():
    # Nos conectamos a la base de datos
    conn = sql.connect('pagos.db')

    # Creamos el cursor con el que interactuar con la tabla
    cursor = conn.cursor()

    # Creamos la tabla de pagos
    cursor.execute("""CREATE TABLE IF NOT EXISTS pagos (
        id_pagos INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        id_user INTEGER NOT NULL,
        importe INTEGER NOT NULL,
        motivo TEXT,
        fecha TEXT NOT NULL);
    """)  
    conn.commit()
    cursor.close()
    conn.close()

def insert_pago(id_user: int, importe: float, motivo: str):
    conn = sql.connect('pagos.db')
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d")  # toma la fecha de hoy
    importe = int(importe * 100)

    cursor.execute("""
INSERT INTO pagos (id_user, importe, motivo, fecha)
VALUES (?, ?, ?, ?)
""", (id_user, importe, motivo, fecha))
    
    conn.commit() 
    cursor.close()
    conn.close()


def imprimir_db():
    conn = sql.connect('pagos.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pagos")

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultado
 
