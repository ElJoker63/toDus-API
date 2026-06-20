import os
import time
from todus.client import Client

# Configura tu número (ej: "5350000000") y el número de destino
MY_PHONE = os.environ.get("TODUS_PHONE", "5350000000")
DEST_PHONE = os.environ.get("TODUS_DEST", "5351111111")

client = Client(MY_PHONE)

def main():
    if not client.logged():
        print("Inicia sesión primero con login_example.py")
        return

    print("Conectando...")
    # Enviamos un mensaje original
    original_msg_id = client.send_message(DEST_PHONE, "Hola, este es un mensaje original de prueba.")
    print(f"Mensaje original enviado con ID: {original_msg_id}")
    
    time.sleep(2)
    
    # Enviamos una respuesta a ese mensaje
    reply_msg_id = client.send_message(
        DEST_PHONE, 
        "Y esta es mi respuesta usando el nuevo sistema de stanzas!",
        reply_to=original_msg_id
    )
    print(f"Respuesta enviada con ID: {reply_msg_id}")

if __name__ == "__main__":
    main()
