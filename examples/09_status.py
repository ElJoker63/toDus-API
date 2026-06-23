"""
Ejemplo de Estados (Historias): Publicar, Ver y Seguidores.
"""
from todus import ToDusClient2

PHONE = "5350000000"
PASSWORD = "TU_CONTRASEÑA"
TARGET_PHONE = "5351111111"

client = ToDusClient2(phone_number=PHONE, password=PASSWORD)
client.login()

def test_status():
    # 1. Publicar un estado (JSON con fondo y texto)
    print("Publicando nuevo estado...")
    status_content = {
        "body": "¡Hola ToDus desde mi script Python!",
        "background": "#ff5722",
        "type": "text"
    }
    status_id = client.publish_status(status_content)
    print(f"Estado publicado. ID: {status_id}")
    
    # 2. Obtener seguidores (síncrono)
    print("Obteniendo mis seguidores...")
    followers = client.get_followers()
    print(f"Tienes {len(followers)} seguidores: {followers}")
    
    # 3. Seguir a alguien
    print(f"Siguiendo a {TARGET_PHONE}...")
    client.follow_user(TARGET_PHONE)
    
    # 4. Obtener info de seguidor
    print(f"Info de relación con {TARGET_PHONE}:")
    info = client.get_follower_info(TARGET_PHONE)
    print(info)

if __name__ == "__main__":
    test_status()
