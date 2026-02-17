import telebot
import db
import csv
from os import remove

TOKEN = "8541016502:AAEtR7yqKfXUftrhcpKULp91sGENq3k-HnY"

# Nos conectamos al bot a traves del TOKEN
bot = telebot.TeleBot(TOKEN)

# Iniciamos la db
db.start_db()

@bot.message_handler(commands=['help'])
def menu_help(message):
    bot.reply_to(message, """Comandos posibles:
/help - Menú de ayuda
/save - Guardar pagos
/dump - Imprime una lista de los pagos
/export - Exporta la base de datos en un csv""")

@bot.message_handler(commands=['save'])
def save_pago(message):
    importe = None
    motivo = None
    try:
        arg = message.text.split()
        importe = float(arg[1])
        motivo = " ".join(arg[2:])
        bot.reply_to(message, f"Se ha añadido el importe {importe:.2f}€ con motivo {motivo}")

        db.insert_pago(message.from_user.id, importe, motivo)
    except ValueError, IndexError:
        bot.reply_to(message, "ERROR, debe ser /save imoprte motivo")

@bot.message_handler(commands=['dump'])
def dump_db(message):
    resultados = db.imprimir_db()

    if not resultados:
        bot.reply_to(message, "No tienes ningun pago guardado")

    for dato in resultados:
        bot.reply_to(message, f"ID: {dato[0]}\nImporte: {dato[2]/100:.2f}€\nMotivo: {dato[3]}\nDia: {dato[4]}")

@bot.message_handler(commands=['export'])
def create_exel(message):
    resultados = db.imprimir_db()

    with open('pagos.csv', 'w', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id_pago", "id_usuario", "importe (centimos)", "motivo", "fecha"])
        for row in resultados:
            writer.writerow(row)
    
    with open("pagos.csv", "rb") as archivo:
        bot.send_document(message.chat.id, archivo)
        
    remove("pagos.csv")

bot.infinity_polling()
