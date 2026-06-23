"""
Ejemplo de canales: Creación y Publicación (ahora con JSON/Base64).
"""
from todus import ToDusClient2

PHONE = "5350000000"
PASSWORD = "TU_CONTRASEÑA"

client = ToDusClient2(phone_number=PHONE, password=PASSWORD)
client.login()

def test_channels():
    # 1. Crear un canal
    # link: único, sin @
    # print("Creando canal...")
    # ch_id = client.create_channel("Mi Canal API", "micanalapi", public=1, desc="Canal de prueba")
    # print(f"Petición de creación enviada. ID: {ch_id}")
    
    # 2. Publicar en un canal
    CHANNEL_JID = "micanalapi@ch.todus.cu"
    print(f"Publicando en {CHANNEL_JID}...")
    
    # Formato de publicación esperado por ToDus (JSON)
    publ_data = {
        "body": "Este es un mensaje publicado desde la API corregida.",
        "type": "text"
    }
    
    msg_id = client.publish_to_channel(CHANNEL_JID, publ_data)
    print(f"Publicación enviada. ID: {msg_id}")

    # 3. Obtener información del canal
    print("Obteniendo info del canal...")
    client.get_channel_info("micanalapi")

if __name__ == "__main__":
    test_channels()
