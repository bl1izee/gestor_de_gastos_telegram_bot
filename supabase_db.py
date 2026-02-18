from dotenv import load_dotenv # Cargar variables de entrono
from os import getenv
from supabase import create_client, Client

# Configuración de conexión
load_dotenv()
URL = getenv("SUPABASE_URL")
KEY = getenv("SUPABASE_KEY")
supabase: Client = create_client(URL, KEY)

def insert_db(tipo: str, id_user: int, cantidad: float, motivo: str):
    cantidad_centimos = int(cantidad * 100)

    data = {
        "id_usuario": id_user,
        "tipo": tipo,
        "cantidad": cantidad_centimos,
        "motivo": motivo,
    }
    
    return supabase.table("pagos").insert(data).execute()

# Como pasa de tupla a lista
def imprimir_db(id_user: int):
    
    response = supabase.table("pagos") \
        .select("*") \
        .eq("id_usuario", id_user) \
        .execute()
    
    # Convertimos a lista de tuplas para mantener compatibilidad con /report y /export
    # Formato: (id_pago, id_usuario, tipo, cantidad, motivo, fecha)
    resultado = []
    for r in response.data:
        resultado.append((
            r['id_pago'], 
            r['id_usuario'], 
            r['tipo'], 
            r['cantidad'], 
            r['motivo'], 
            r['fecha']
        ))
    return resultado

def editar_db(id_user: int, id_pago: int, cantidad_centimos: int, motivo: str):
    return supabase.table("pagos") \
        .update({"cantidad": cantidad_centimos, "motivo": motivo}) \
        .eq("id_pago", id_pago) \
        .eq("id_usuario", id_user) \
        .execute()

# Por que len > 0
def existe_pago(id_user: int, id_pago: int):
    response = supabase.table("pagos") \
        .select("id_pago") \
        .eq("id_pago", id_pago) \
        .eq("id_usuario", id_user) \
        .execute()
    
    return len(response.data) > 0