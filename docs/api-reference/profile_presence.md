# Perfil y Presencia

## Perfil del Usuario

Estas funciones te permiten actualizar la información de tu propia cuenta (o del bot).

### `update_profile(alias="", bio="", picture_url="", thumbnail_url="")`
Actualiza tu perfil con los campos especificados. Los campos vacíos no se modifican.

```python
client.update_profile(
    alias="Mi Bot",
    bio="Bot programado en Python con toDus-API",
    picture_url="https://s3.todus.cu/avatar.jpg",
    thumbnail_url="https://s3.todus.cu/avatar_thumb.jpg"
)
```

### `set_todus_id(new_id)`
Cambia tu @username (ToDus ID) mediante XMPP.

```python
client.set_todus_id("mi_nuevo_username")
```

### `upload_avatar(image_data, thumbnail_data=None)`
Sube una nueva foto de perfil gestionando automáticamente los thumbnails.

```python
with open("mi_logo.png", "rb") as f:
    image_data = f.read()

profile_url, thumbnail_url = client.upload_avatar(image_data)
```

### `upload_avatar_from_file(filepath, thumbnail_path=None)`
Sube una nueva foto de perfil desde un archivo.

```python
client.upload_avatar_from_file("mi_logo.png")
```

---

## Presencia XMPP

El estado de conectividad en el protocolo XMPP de ToDus.

### Estados de Chat (Typing)

```python
client.send_chat_state("5350000000", "composing")  # Escribiendo...
client.send_chat_state("5350000000", "paused")     # Dejó de escribir
client.send_chat_state("5350000000", "active")     # Activo
client.send_chat_state("5350000000", "gone")       # Desconectado
```

### Confirmaciones de Lectura

```python
# Confirmación de entrega
client.send_read_receipt("5350000000", "msg_id")

# Confirmación de lectura
client.send_read_receipt("5350000000", "msg_id")
```

### Last Seen (Última Conexión)

```python
last = client.get_last_seen("5350000000")
# Output: {"seconds": "1718841234"}
```
