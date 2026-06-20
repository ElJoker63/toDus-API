# Mensajería

Esta sección cubre todas las funciones para enviar y administrar mensajes de chat privados.

## Enviar Mensajes de Texto

### `send_text_message(to, text, reply_to="")`

Envía un mensaje de texto normal a un usuario.

- **to**: El número de teléfono (ej. `"5350000000"`).
- **text**: El contenido del mensaje.
- **reply_to** *(opcional)*: El ID del mensaje al que quieres responder.

```python
client.send_text_message("5350000000", "Hola mundo")
```

## Borrar Mensajes

### `delete_message(msg_id, to_jid="")`

Borra un mensaje que hayas enviado previamente.

```python
client.delete_message("id_del_mensaje_hex")
```

## Reacciones

### `send_reaction(msg_id, to_user, reaction)`

Añade una reacción (emoji) a un mensaje.

```python
client.send_reaction("id_del_mensaje", "5350000000", "👍")
```

### `remove_reaction(msg_id, to_user)`

Quita tu reacción actual de un mensaje.

```python
client.remove_reaction("id_del_mensaje", "5350000000")
```

## Botones Interactivos (In-Line Keyboards)

Para enviar botones (como en Telegram), adjuntas la estructura JSON en el `text` del mensaje y le dices a la función que es de tipo botón.

```python
import json

botones = {
    "title": "¿Te gusta la librería?",
    "buttons": [
        {"id": "btn_yes", "text": "¡Sí!"},
        {"id": "btn_no", "text": "Un poco"}
    ]
}

client.send_text_message("5350000000", json.dumps(botones), msg_type="button")
```
