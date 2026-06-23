"""
Ejemplo de mensajería básica: Texto, Edición, Eliminación y Recibos.
"""
from todus import ToDusClient2
import time

PHONE = "5350000000"
PASSWORD = "TU_CONTRASEÑA"
DEST_PHONE = "5351111111"

client = ToDusClient2(phone_number=PHONE, password=PASSWORD)
client.login()

def test_messages():
    # 1. Enviar mensaje de texto
    print(f"Enviando mensaje a {DEST_PHONE}...")
    msg_id = client.send_message(DEST_PHONE, "Hola, esto es una prueba de la nueva API")
    print(f"Mensaje enviado. ID: {msg_id}")
    
    time.sleep(2)
    
    # 2. Editar el mensaje
    print("Editando el mensaje...")
    edit_id = client.edit_message(DEST_PHONE, "Hola, este mensaje HA SIDO EDITADO", msg_id)
    print(f"Mensaje editado. ID de edición: {edit_id}")
    
    time.sleep(2)
    
    # 3. Confirmar lectura (si recibimos un mensaje)
    # client.send_read_receipt(DEST_PHONE, "id_del_mensaje")
    
    # 4. Eliminar el mensaje
    print("Eliminando el mensaje...")
    del_id = client.delete_message(DEST_PHONE, msg_id)
    print(f"Mensaje eliminado. Confirmación: {del_id}")

if __name__ == "__main__":
    test_messages()
