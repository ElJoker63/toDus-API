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

# Trying to set toDus ID (username)
new_id = "botnext_api"

print(f"Cambiando el @todus_id a: {new_id}...")
mid = client.set_todus_id(new_id)

print(f"Petición enviada con msg_id: {mid}")
