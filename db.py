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
        tipo TEXT CHECK(tipo IN ('ingreso','pago')) NOT NULL,
        cantidad INTEGER NOT NULL,
        motivo TEXT,
        fecha TEXT NOT NULL);
    """) 

    conn.commit()
    cursor.close()
    conn.close()

def insert_db(tipo: str, id_user: int, cantidad: float, motivo: str):
    conn = sql.connect('pagos.db')
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d")  # toma la fecha de hoy
    cantidad = int(cantidad * 100)

    cursor.execute("""
INSERT INTO pagos (id_user, tipo, cantidad, motivo, fecha)
VALUES (?, ?, ?, ?, ?)
""", (id_user, tipo, cantidad, motivo, fecha))
    
    conn.commit() 
    cursor.close()
    conn.close()

def imprimir_db(id_user: int):
    ahora = datetime.now()
    mes_actual = ahora.strftime("%m")
    año_actual = ahora.strftime("%Y")

    conn = sql.connect('pagos.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM pagos 
        WHERE id_user = ?
        AND strftime('%m', fecha) = ?
        AND strftime('%Y', fecha) = ?
    """, (id_user, mes_actual, año_actual))

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultado

def editar_db(id_user: int, id_pagos: int, cantidad: float, motivo: str):
    conn = sql.connect('pagos.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pagos
        SET cantidad = ?, motivo = ?
        WHERE id_pagos = ?
        AND id_user = ?
    """, (cantidad, motivo, id_pagos, id_user))
    
    conn.commit()
    cursor.close()
    conn.close()

def existe_pago(id_user: int, id_pago: int):
    conn = sql.connect('pagos.db')
    cursor = conn.cursor()

    # Devuelve 1 si encuentra un pago que machee con la informacion y se limita a encontrar solo 1, para la ejecucion si lo encuentra
    cursor.execute("""
        SELECT 1
        FROM pagos
        WHERE id_pagos = ?
        AND id_user = ?
        LIMIT 1
    """, (id_pago, id_user))

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado is not None
