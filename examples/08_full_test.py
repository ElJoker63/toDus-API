"""
Script de prueba completa para verificar todas las funciones corregidas.
"""
import os
import time
from todus import ToDusClient2, FileType

# Recomiendo configurar estas variables en tu sistema o aquí directamente para la prueba
PHONE = os.getenv("TODUS_PHONE") or "5350000000"
PASSWORD = os.getenv("TODUS_PASSWORD") or "TU_CONTRASEÑA"
DEST = os.getenv("TODUS_DEST") or "5351111111"

def run_tests():
    print("--- Iniciando pruebas de toDus-API ---")
    client = ToDusClient2(phone_number=PHONE, password=PASSWORD)
    
    try:
        print(f"1. Login para {PHONE}...")
        client.login()
        print("   ¡OK!")

        print(f"2. Enviando mensaje de texto a {DEST}...")
        mid = client.send_message(DEST, "Test integral de la API")
        print(f"   ¡Enviado! ID: {mid}")

        print("3. Editando mensaje...")
        time.sleep(1)
        client.edit_message(DEST, "Test integral (EDITADO)", mid)
        print("   ¡Editado!")

        print("4. Enviando estado de chat (Escribiendo...)...")
        client.send_chat_state(DEST, "composing")
        time.sleep(2)
        client.send_chat_state(DEST, "paused")
        print("   ¡OK!")

        print("5. Prueba de perfil (Bio)...")
        client.update_profile(bio=f"Último test: {time.ctime()}")
        print("   ¡Bio actualizada!")

        print("6. Solicitando privacidad...")
        p = client.get_profile_privacy()
        print(f"   Ajustes: {p}")

        print("7. Enviando ubicación...")
        client.send_location_message(DEST, 23.1136, -82.3666, text="La Habana, Cuba")
        print("   ¡Ubicación enviada!")

        print("\n--- Pruebas básicas completadas con éxito ---")
        print("Usa los scripts individuales (01-07) para pruebas más específicas.")

    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")

if __name__ == "__main__":
    if PASSWORD == "TU_CONTRASEÑA":
        print("Por favor, configura tu contraseña en el script o variable de entorno TODUS_PASSWORD")
    else:
        run_tests()
