"""
Ejemplo de Listener: Recibir y procesar mensajes en tiempo real.
"""
from todus import ToDusClient2
import logging

# Configurar logs para ver qué pasa internamente
logging.basicConfig(level=logging.INFO)

PHONE = "5350000000"
PASSWORD = "TU_CONTRASEÑA"

client = ToDusClient2(phone_number=PHONE, password=PASSWORD)
client.login()

def on_new_message(msg: dict):
    """
    Este callback se ejecuta cada vez que llega una stanza <m> (mensaje).
    El diccionario 'msg' contiene todos los campos parseados por parser.py
    """
    sender = msg.get("from", "Desconocido")
    body = msg.get("body", "")
    is_group = msg.get("is_group", False)
    
    prefix = "[GRUPO]" if is_group else "[PRIVADO]"
    print(f"{prefix} Mensaje de {sender}: {body}")
    
    # Responder solo si es un mensaje de texto y no es nuestro
    if body and sender != client.jid:
        if body.lower() == "hola":
            client.send_message(sender, "¡Hola! Soy un bot funcionando con la API corregida.")

if __name__ == "__main__":
    print("Iniciando listener... Presiona Ctrl+C para salir.")
    try:
        client.listen_messages(on_new_message)
    except KeyboardInterrupt:
        print("\nListener detenido por el usuario.")
