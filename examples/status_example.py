import os
import time
from todus.client import ToDusClient2

PHONE = os.getenv("TODUS_PHONE")
PASSWORD = os.getenv("TODUS_PASSWORD")

def on_message(msg):
    # Imprimir todos los resultados IQ del servidor
    if msg.get("type") == "result" and msg.get("query") is not None:
        print("\n=== Resultado de IQ ===")
        print(msg["query"])

def main():
    if not PHONE or not PASSWORD:
        print("Configura las variables de entorno TODUS_PHONE y TODUS_PASSWORD.")
        return
        
    client = ToDusClient2(PHONE, PASSWORD)
    print("Iniciando login...")
    client.login()
    print("Conectado con éxito.")

    client.listen_messages(on_message)
    time.sleep(1)
    
    print("\n1. Obteniendo lista de seguidores...")
    client.get_followers(limit=10)
    time.sleep(3)
    
    print("\n2. Publicando un nuevo estado...")
    # Estructura JSON de prueba básica
    status_content = {
        "text": "¡Probando la nueva API de Estados desde Python!",
        "bg_color": "#ff0000",
        "font": 1
    }
    client.publish_status(status_content)
    time.sleep(3)
    
    # Reemplaza por un número de alguien que siga tus estados para probar follow/unfollow
    # target_user = "535XXXXXXX"
    # print(f"\n3. Empezando a seguir los estados de {target_user}...")
    # client.follow_user(target_user)
    # time.sleep(3)

    print("\n¡Ejemplo finalizado! Puedes revisar la app ToDus oficial para ver tu estado publicado.")

if __name__ == "__main__":
    main()
