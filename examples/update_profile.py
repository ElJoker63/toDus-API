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

print("Actualizando perfil (alias y bio)...")
success = client.update_profile(
    alias="Python ToDus API Bot",
    bio="¡Hola! Soy un bot controlado por la librería ToDus-API.",
)

if success:
    print("¡Perfil actualizado con éxito!")
else:
    print("Hubo un error al actualizar el perfil.")

# --- Cambiar foto de perfil ---
# Requiere una imagen válida. Descomenta y ajusta la ruta.
# print("Subiendo nueva foto de perfil...")
# avatar_url, thumb_url = client.upload_avatar_from_file("avatar_bot.jpg")
# success_pic = client.update_profile(picture_url=avatar_url, thumbnail_url=thumb_url)
# if success_pic:
#     print("¡Foto de perfil actualizada!")

# --- Cambiar @username (todus_id) ---
# OJO: No debe tener espacios ni '@' inicial.
print("Cambiando el @username...")
msg_id = client.set_todus_id("BotNext_API_Python")
print(f"Petición para cambiar @ enviada con msg_id: {msg_id}")
