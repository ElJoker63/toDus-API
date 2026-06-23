"""
Ejemplo para obtener los JIDs de todos tus canales.
"""
from todus import ToDusClient2

PHONE = "5350000000"
PASSWORD = "TU_CONTRASEÑA"

client = ToDusClient2(phone_number=PHONE, password=PASSWORD)
client.login()

def get_my_channels():
    print("Obteniendo lista de mis canales...")
    try:
        channels = client.get_my_channels()
        if not channels:
            print("No estás suscrito a ningún canal o no eres administrador de ninguno.")
        else:
            print(f"Has obtenido {len(channels)} canales:")
            for jid in channels:
                print(f" - JID: {jid}")
                
    except Exception as e:
        print(f"Error obteniendo canales: {e}")

if __name__ == "__main__":
    get_my_channels()
