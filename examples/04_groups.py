"""
Ejemplo de grupos: Unirse, Enviar mensajes, Miembros y Salir.
"""
from todus import ToDusClient2

PHONE = "5350000000"
PASSWORD = "TU_CONTRASEÑA"
GROUP_ID = "XXXXXXXX" # ID del grupo sin @muclight...

client = ToDusClient2(phone_number=PHONE, password=PASSWORD)
client.login()

def test_groups():
    # 1. Unirse a un grupo (si no estás unido)
    print(f"Uniéndose al grupo {GROUP_ID}...")
    client.groups.join(GROUP_ID)
    
    # 2. Enviar mensaje al grupo
    print("Enviando mensaje al grupo...")
    msg_id = client.send_message(GROUP_ID, "Hola grupo, este mensaje es desde la API corregida")
    print(f"Mensaje grupal enviado. ID: {msg_id}")
    
    # 3. Obtener miembros (El resultado llegará por el listener)
    print("Solicitando lista de miembros...")
    client.groups.get_members(GROUP_ID)
    
    # 4. Obtener enlace de invitación
    print("Solicitando enlace de invitación...")
    client.groups.get_invite_link(GROUP_ID)
    
    # 5. Salir del grupo
    # print("Saliendo del grupo...")
    # client.groups.leave(GROUP_ID)

if __name__ == "__main__":
    test_groups()
