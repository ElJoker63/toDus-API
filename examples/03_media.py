"""
Ejemplo de multimedia: Subida y envío de imágenes y archivos.
"""
from todus import ToDusClient2, FileType
import os

PHONE = "5350000000"
PASSWORD = "TU_CONTRASEÑA"
DEST_PHONE = "5351111111"

client = ToDusClient2(phone_number=PHONE, password=PASSWORD)
client.login()

def test_media():
    # 1. Enviar una imagen
    img_path = "avatar.png"
    if os.path.exists(img_path):
        print(f"Subiendo y enviando imagen: {img_path}")
        with open(img_path, "rb") as f:
            data = f.read()
        
        # Subir y obtener URL
        url = client.upload_file(data, file_type=FileType.PICTURE, file_name="prueba.png")
        print(f"Imagen subida. URL: {url}")
        
        # Enviar mensaje de imagen
        mid = client.send_image_message_simple(DEST_PHONE, url, "prueba.png", len(data))
        print(f"Mensaje de imagen enviado. ID: {mid}")
    else:
        print(f"No se encontró la imagen en {img_path}")

    # 2. Enviar un archivo genérico
    file_content = b"Contenido de prueba para archivo"
    print("Subiendo archivo genérico...")
    file_url = client.upload_file(file_content, file_type=FileType.FILE, file_name="test.txt")
    mid_file = client.send_file_message(DEST_PHONE, file_url, FileType.FILE, caption="Aquí tienes el archivo", file_name="test.txt", file_size=len(file_content))
    print(f"Archivo enviado. ID: {mid_file}")

if __name__ == "__main__":
    test_media()
