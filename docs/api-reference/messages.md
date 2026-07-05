# Mensajería

Esta sección cubre todas las funciones para enviar y administrar mensajes de chat privados.

## Enviar Mensajes de Texto

### `send_message(to, body, reply_to="")`

Envía un mensaje de texto normal a un usuario.

- **to**: El número de teléfono (ej. `"5350000000"`).
- **body**: El contenido del mensaje.
- **reply_to** *(opcional)*: El ID del mensaje al que quieres responder.

```python
client.send_message("5350000000", "Hola mundo")
```

## Borrar Mensajes

### `delete_message(to, msg_id)`

Borra un mensaje que hayas enviado previamente.

```python
client.delete_message("5350000000", "id_del_mensaje_hex")
```

## Edición de Mensajes

### `edit_message(to, new_body, msg_id)`

Cambia el contenido de un mensaje ya enviado.

```python
client.edit_message("5350000000", "Nuevo texto", "id_del_original")
```

## Reenviar Mensajes

### `forward_message(to, original_from, original_id, reply_to="")`

Reenvía un mensaje existente de otro usuario a un contacto o grupo.

- **to**: Destino (número o group_id).
- **original_from**: JID del remitente original del mensaje.
- **original_id**: ID del mensaje original a reenviar.

```python
client.forward_message("5350000000", "5351111111@im.todus.cu", "abc123")
```

## Eliminar Propio (deletedowner)

### `send_deleted_owner_message(to, message_id)`

Envía una notificación de eliminación de mensaje propio usando el namespace `deletedowner:n`.

```python
client.send_deleted_owner_message("5350000000", "msg_id_a_eliminar")
```

## Fragmentos de Mensajes (Chunk)

### `chunk_message(to, body, chunk_msg, chunk_index, chunk_total)`

Envía un fragmento de un mensaje grande. Útil para mensajes que exceden el límite de 8192 bytes.

```python
# Ejemplo: enviar un mensaje de 20000 bytes en 3 fragmentos
client.send_message("5350000000", chunk1, chunk_msg=msg_id, chunk_index=1, chunk_total=3)
```

## Botones Interactivos

```python
buttons = [
    {"text": "Web", "command": "cmd_type_url", "data": "https://google.com"},
    {"text": "Enviar", "command": "cmd_type_send", "data": "Dato"},
    {"text": "Copiar", "command": "cmd_copy_to_clipboard", "data": "Texto a copiar"},
    {"text": "Abrir App", "command": "cmd_open_app_screen", "data": ""},
]
client.send_button_message("5350000000", "Elige una opción", buttons)
```

**Comandos disponibles:**
| Comando | Descripción |
|---------|-------------|
| `cmd_type_send` | Envía el dato como mensaje |
| `cmd_type_url` | Abre una URL |
| `cmd_type_copy` | Copia texto al portapapeles |
| `cmd_type_call` | Realiza una llamada |
| `cmd_copy_to_clipboard` | Copia al portapapeles |
| `cmd_open_app_screen` | Abre una pantalla de la app |
| `cmd_open_web` | Abre un navegador web |
| `cmd_placeholder` | Placeholder genérico |

## Mensajes Multimedia

### Notas de Voz

### `send_voice_message(to, url, voice_id, file_size, duration, wave_sample="", reply_to="")`

Envía una nota de voz con datos de onda (wave sample) para previsualización.

```python
client.send_voice_message(
    "5350000000",
    url="https://s3.todus.cu/voice.opus",
    voice_id="voice_abc123",
    file_size=15000,
    duration=12,
    wave_sample="AAAA..."
)
```

### Audio

### `send_audio_message(to, url, audio_id, file_name, file_size, duration, reply_to="")`

Envía un archivo de audio con nombre y duración.

```python
client.send_audio_message(
    "5350000000",
    url="https://s3.todus.cu/song.mp3",
    audio_id="audio_abc123",
    file_name="cancion.mp3",
    file_size=3500000,
    duration=210
)
```

### GIFs

### `send_gif_message(to, url, gif_id, file_name, file_size, width=0, height=0, thumbnail="", reply_to="")`

Envía un GIF animado con dimensiones y miniatura.

```python
client.send_gif_message(
    "5350000000",
    url="https://s3.todus.cu/funny.gif",
    gif_id="gif_abc123",
    file_name="funny.gif",
    file_size=500000,
    width=480,
    height=360,
    thumbnail="U6688O?Hr=xu^-w2sp..."
)
```

### Imágenes

```python
client.send_image_message(
    "5350000000",
    url="https://s3.todus.cu/foto.jpg",
    file_name="foto.jpg",
    file_size=250000,
    width=1920,
    height=1080,
    thumbnail="U6688O?Hr=xu^-w2sp..."
)
```

### Videos

```python
client.send_video_message(
    "5350000000",
    url="https://s3.todus.cu/video.mp4",
    video_id="video_abc123",
    file_name="video.mp4",
    file_size=15000000,
    duration=65,
    width=1280,
    height=720,
    thumbnail="U6688O?Hr=xu^-w2sp..."
)
```

### Archivos

```python
client.send_file_message(
    "5350000000",
    url="https://s3.todus.cu/doc.pdf",
    file_type=FileType.FILE,
    file_name="documento.pdf",
    file_size=500000
)
```

### Contactos

```python
client.send_contact_message(
    "5350000000",
    contact_id="5351111111",
    contact_name="Juan Pérez",
    contact_phone="5351111111"
)
```

### Stickers

```python
client.send_sticker_message(
    "5350000000",
    sticker_id="sticker_123",
    sticker_name="Gatito Feliz",
    sticker_pack="pack_animales",
    sticker_hash="abc123hash"
)
```

### Ubicación

```python
client.send_location_message(
    "5350000000",
    lat=23.1136,
    lon=-82.3666,
    zoom=15.0,
    text="La Habana, Cuba"
)
```

### Eventos / Calendario

```python
client.send_event_message(
    "5350000000",
    title="Reunión de equipo",
    start=1720000000000,
    end=1720003600000,
    all_day=False,
    ics_data="BEGIN:VCALENDAR\nSUMMARY:Reunión\nEND:VCALENDAR"
)
```

## Estado de Chat (Typing)

```python
client.send_chat_state("5350000000", "composing")  # Escribiendo...
client.send_chat_state("5350000000", "paused")     # Dejó de escribir
```

## Confirmaciones

```python
# Confirmación de entrega
client.send_read_receipt("5350000000", "msg_id")

# Confirmación de lectura
client.send_read_receipt("5350000000", "msg_id")
```
