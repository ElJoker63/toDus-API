"""
Ejemplo de perfil: Actualización de datos y Avatar.
"""
from todus import ToDusClient2
import os

PHONE = "5350000000"
PASSWORD = "TU_CONTRASEÑA"

client = ToDusClient2(phone_number=PHONE, password=PASSWORD)
client.login()

def test_profile():
    # 1. Actualizar Alias y Bio
    print("Actualizando alias y descripción...")
    client.update_profile(alias="Python Master", bio="Programando en las sombras")
    
    # 2. Subir Avatar
    img_path = "avatar.png"
    if os.path.exists(img_path):
        print(f"Subiendo avatar desde: {img_path}")
        img_url, thumb_url = client.upload_avatar_from_file(img_path)
        print(f"Avatar subido. Imagen: {img_url}, Miniatura: {thumb_url}")
        
        # Aplicar el avatar al perfil
        client.update_profile(picture_url=img_url, thumbnail_url=thumb_url)
    
    # 3. Cambiar ToDus ID (@username)
    print("Cambiando ToDus ID...")
    client.set_todus_id("python_dev_63")

if __name__ == "__main__":
    test_profile()
