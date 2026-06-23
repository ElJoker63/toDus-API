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

## Botones Interactivos

```python
buttons = [
    {"text": "Web", "command": "cmd_type_url", "data": "https://google.com"},
    {"text": "Enviar", "command": "cmd_type_send", "data": "Dato"}
]
client.send_button_message("5350000000", "Elige una opción", buttons)
```
