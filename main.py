import telebot
import supabase_db as db
import csv
from datetime import datetime
from dotenv import load_dotenv # Cargar variables de entrono
from os import remove, getenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

# Nos conectamos al bot a traves del TOKEN
bot = telebot.TeleBot(TOKEN)

# --- Funciones de Utilidad ---
def save_db(message, tipo: str):
    try:
        arg = message.text.split()
        pago = float(arg[1])

        if(pago <= 0):
            raise ValueError

        motivo = " ".join(arg[2:])
        
        db.insert_db(tipo, message.from_user.id, pago, motivo)

        bot.reply_to(message, f"Se ha añadido el pago {pago:.2f}€ con motivo {motivo}")
    except IndexError:
        menu_help(message)
    except ValueError:
        bot.reply_to(message, "ERROR, la cantidad debe ser un número válido y positivo")

# --- Handlers de Comandos ---
@bot.message_handler(commands=['help'])
def menu_help(message):
    bot.reply_to(message, """Comandos:
/help - Menú de ayuda
/pago - Guardar un pago, sintaxis: /pago <cantidad> <motivo>
/ingreso - Guarda un importe, sintaxis: /importe <cantidad> <motivo>
/dump - Imprime una lista de los pagos del mes actual
/export - Exporta la todos los pagos historicos en un csv
/report - Imprime estadisticas de los pagos e importes del mes actual
/edit - Permite editar un pago, sintaxis: /edit <id> <cantidad> <motivo>
""")

@bot.message_handler(commands=['pago'])
def save_pago(message):
    save_db(message, "pago")

@bot.message_handler(commands=['ingreso'])
def save_importe(message):
    save_db(message, "ingreso")

@bot.message_handler(commands=['dump'])
def dump_db(message):
    resultados = db.imprimir_db(message.from_user.id)

    if not resultados:
        bot.reply_to(message, "No tienes ningun importe/pago guardado")

    for dato in resultados:
        fecha_actual = dato[5]

        # Calculamos el primer día del mes actual para filtrar
        primer_dia_mes = datetime.now().replace(day=1).strftime("%Y-%m-%d")

        if (fecha_actual >= primer_dia_mes):
            bot.reply_to(message, f"ID: {dato[0]}\nTipo: {dato[2]}\nCantidad: {dato[3]/100:.2f}€\nMotivo: {dato[4]}\nDia: {dato[5]}")

@bot.message_handler(commands=['export'])
def create_exel(message):
    resultados = db.imprimir_db(message.from_user.id)
    file_path = 'pagos_export.csv'

    with open(file_path, 'w', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id_pago", "id_usuario", "tipo", "cantidad (centimos)", "motivo", "fecha"])
        for row in resultados:
            writer.writerow(row)
    
    with open(file_path, "rb") as archivo:
        bot.send_document(message.chat.id, archivo)
        
    remove(file_path)

@bot.message_handler(commands=['report'])
def report_db(message):
    resultados = db.imprimir_db(message.from_user.id)

    media=0
    total_pagos=0
    total_ingresos=0
    numero_pagos=0

    for data in resultados:
        if(data[2] == "pago"):
            numero_pagos+=1
            total_pagos+=data[3]
        else:
            total_ingresos+= data[3]

    media = (total_pagos / numero_pagos) if numero_pagos > 0 else 0
    bot.reply_to(message, f"Total de pagos {(total_pagos/100):.2f}€\nMedia de pagos {(media/100):.2f}€\nTotal de ingresos {(total_ingresos/100):.2f}€\nTotal este mes {(total_ingresos-total_pagos)/100:.2f}€")

@bot.message_handler(commands=['edit'])
def edit_db(message):
    try:
        arg = message.text.split()
        id_pago = int(arg[1])
        cantidad = int(float(arg[2]) * 100)
        motivo = " ".join(arg[3:])

        if not db.existe_pago(message.from_user.id, id_pago):
            bot.reply_to(message, "ERROR, el id no existe, usa /dump para ver la lista de pagos/ingresos")
            return

        if(cantidad <= 0):
            raise ValueError
        
        db.editar_db(message.from_user.id, id_pago, cantidad, motivo)
        bot.reply_to(message, f"Se ha editado correctamente, usa /dump para ver la lista")
    except IndexError:
        menu_help(message)
    except ValueError:
        bot.reply_to(message, "ERROR, la cantidad debe ser un número válido y positivo")

bot.infinity_polling()
