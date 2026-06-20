import os
import time
from todus.client import ToDusClient2

PHONE = os.getenv("TODUS_PHONE")
PASSWORD = os.getenv("TODUS_PASSWORD")

def on_message(msg):
    if msg.get("type") == "result" and msg.get("query") is not None:
        print("\n=== Resultado de IQ de Canal ===")
        print(msg["query"])

def main():
    if not PHONE or not PASSWORD:
        print("Set TODUS_PHONE and TODUS_PASSWORD env vars.")
        return
        
    client = ToDusClient2(PHONE, PASSWORD)
    print("Iniciando login...")
    client.login()
    print("Conectado con token:", client.token[:10] + "...")

    client.listen_messages(on_message)
    time.sleep(1)
    
    print("\n1. Obteniendo mis canales...")
    client.get_my_channels()
    time.sleep(3)
    
    print("\n2. Creando canal de prueba...")
    # Link debe ser unico, usamos el tiempo
    link = f"canal_bot_{int(time.time())}"
    client.create_channel(
        name="Canal de Prueba Bot",
        link=link,
        public=1,
        desc="Este es un canal creado desde toDus-API"
    )
    time.sleep(3)
    
    print("\n3. Obteniendo información del canal creado...")
    client.get_channel_info(link)
    time.sleep(3)
    
    channel_jid = f"{link}@ch.todus.cu"
    print("\n4. Publicando en el canal...")
    # Crear un simple mensaje en XML
    msg_xml = "<message><b>Hola desde el nuevo canal!</b></message>"
    client.publish_to_channel(channel_jid, msg_xml)
    time.sleep(3)
    
    print("\n5. Leyendo las publicaciones del canal...")
    client.get_channel_publications(channel_jid)
    time.sleep(3)

if __name__ == "__main__":
    main()
