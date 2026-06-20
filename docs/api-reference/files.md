# Archivos y Medios

Subir y descargar archivos multimedia en ToDus requiere generar URLs firmadas (Upload/Download query) y luego realizar la petición HTTP. La API de Python hace todo esto por ti en un solo paso.

## Subir Archivos

### `upload_file(file_path)`
Sube cualquier archivo genérico al servidor de ToDus.
```python
file_url, file_size = client.upload_file("documento.pdf")
client.send_file_message("5350000000", file_url, file_size, "application/pdf", "documento.pdf")
```

### `upload_image(file_path)`
Sube una imagen. Devuelve la URL original y la URL del thumbnail.
```python
img_url, thumb_url = client.upload_image("foto.jpg")
client.send_image_message("5350000000", img_url, thumb_url)
```

## Enviar Mensajes Multimedia

Una vez subidos, se envían usando las funciones:
- `send_image_message(to, image_url, thumbnail_url, width, height)`
- `send_video_message(to, video_url, thumbnail_url, duration, size, ...)`
- `send_audio_message(to, audio_url, duration, size, ...)`
- `send_file_message(to, url, size, mimetype, filename)`
