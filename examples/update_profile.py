import os
import sys
from todus.client import ToDusClient2

phone = os.environ.get("TODUS_PHONE")
auth_token = os.environ.get("TODUS_AUTH_TOKEN")

if not phone or not auth_token:
    print("Por favor, establece las variables de entorno TODUS_PHONE y TODUS_AUTH_TOKEN.")
    sys.exit(1)

client = ToDusClient2(phone_number=phone, password=auth_token)

print("Haciendo login...")
client.login()

print("Actualizando perfil...")
success = client.update_profile(
    alias="Python ToDus API Bot",
    bio="¡Hola! Soy un bot controlado por la librería ToDus-API.",
)

if success:
    print("¡Perfil actualizado con éxito!")
else:
    print("Hubo un error al actualizar el perfil.")

