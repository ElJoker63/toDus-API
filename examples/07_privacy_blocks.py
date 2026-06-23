"""
Ejemplo de privacidad, bloqueos y última conexión.
"""
from todus import ToDusClient2

PHONE = "5350000000"
PASSWORD = "TU_CONTRASEÑA"
TARGET_PHONE = "5351111111"

client = ToDusClient2(phone_number=PHONE, password=PASSWORD)
client.login()

def test_privacy():
    # 1. Obtener última conexión de alguien
    print(f"Obteniendo última conexión de {TARGET_PHONE}...")
    last_seen = client.get_last_seen(TARGET_PHONE)
    print(f"Datos recibidos: {last_seen}")
    
    # 2. Bloquear un usuario
    print(f"Bloqueando a {TARGET_PHONE}...")
    client.block_user(TARGET_PHONE)
    
    # 3. Obtener lista de bloqueados
    print("Obteniendo lista de bloqueados...")
    blocked = client.get_block_list()
    print(f"Bloqueados: {blocked}")
    
    # 4. Desbloquear
    print(f"Desbloqueando a {TARGET_PHONE}...")
    client.unblock_user(TARGET_PHONE)
    
    # 5. Privacidad de perfil
    print("Configurando privacidad de perfil...")
    # Solo mis contactos pueden ver mi foto y mi última conexión
    client.set_profile_privacy(profile_photo="contacts", last="contacts", info="everyone")
    
    # 6. Obtener privacidad actual
    print("Obteniendo ajustes de privacidad...")
    privacy = client.get_profile_privacy()
    print(f"Privacidad actual: {privacy}")

if __name__ == "__main__":
    test_privacy()
