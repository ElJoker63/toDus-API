import logging
import time
import os
from todus import ToDusClient2

# Configurar logging para ver la salida de depuración
logging.basicConfig(level=logging.DEBUG)

def main():
    # Obtener credenciales desde variables de entorno
    phone_number = os.environ.get("TODUS_PHONE")
    password = os.environ.get("TODUS_PASSWORD")

    if not phone_number or not password:
        print("Asegúrate de definir TODUS_PHONE y TODUS_PASSWORD en tus variables de entorno.")
        return

    # Iniciar sesión y autenticar al cliente
    client = ToDusClient2(phone_number, password)
    
    try:
        print("Conectando a ToDus...")
        client.login()
        print("Login exitoso.")
        
        # 1. Obtener credenciales TURN
        # Esto pedirá al servidor de ToDus los STUN/TURN necesarios para WebRTC
        print("Solicitando credenciales TURN...")
        turn_response = client.request_turn_credentials()
        print("Respuesta de credenciales TURN:", turn_response)
        
        # Opcional: Pausar para visualizar logs antes de intentar la llamada
        time.sleep(2)
        
        target_phone = input("Ingresa el número al que deseas llamar (ej. 535xxxxxxx): ")
        if target_phone:
            print(f"Iniciando llamada a {target_phone}...")
            
            # Aquí podrías usar una librería como 'aiortc' para generar tu SDP (Offer)
            # Ejemplo simplificado de payload JSON SDP:
            mock_sdp_offer = '{"type": "offer", "sdp": "v=0\\r\\no=..."}'
            
            # 2. Iniciar llamada
            client.start_call(target_phone, content=mock_sdp_offer)
            print("Petición de llamada (offer) enviada.")
            
            time.sleep(3)
            
            # 3. Finalizar la llamada
            print(f"Finalizando llamada con {target_phone}...")
            client.end_call(target_phone, reason='{"reason": "terminada por el usuario"}')
            print("Llamada finalizada.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
