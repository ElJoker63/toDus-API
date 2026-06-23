"""
Ejemplo de autenticación: Registro, Validación de código y Login.
"""
import os
from todus import ToDusClient2

# Configuración
PHONE = "5350000000"  # Reemplaza con tu número
PASSWORD = ""        # Se obtendrá tras validar el código

client = ToDusClient2(phone_number=PHONE)

def auth_flow():
    # 1. Solicitar código de registro (SMS)
    print(f"Solicitando código para {PHONE}...")
    client.request_code()
    
    # 2. Validar código recibido
    code = input("Introduce el código de 6 dígitos recibido por SMS: ")
    print("Validando código...")
    password = client.validate_code(code)
    print(f"¡Éxito! Tu contraseña es: {password}")
    print("Guarda esta contraseña para futuros inicios de sesión.")

def login_only():
    # Si ya tienes contraseña
    print(f"Iniciando sesión para {PHONE}...")
    password = os.getenv("TODUS_PASSWORD") or "TU_CONTRASEÑA_AQUI"
    client.password = password
    
    token = client.login()
    print(f"Login exitoso. Token obtenido: {token[:20]}...")

if __name__ == "__main__":
    # Elige una opción comentando la otra
    # auth_flow()
    login_only()
