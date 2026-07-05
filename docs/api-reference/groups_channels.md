# Grupos y Canales

ToDus usa la extensión MUC Light para sus grupos, y una variante avanzada para canales.

## Grupos MUC Light

La clase `ToDusClient2` provee acceso a la gestión de grupos a través del atributo `.groups`.

### `join(group_id)`
Te unes a un grupo existente mediante su ID.
```python
client.groups.join("ID_DEL_GRUPO")
```

### Enviar Mensajes a Grupo
```python
client.send_message("ID_DEL_GRUPO", "Hola grupo")
```

### Administrar Miembros
- `get_members(group_id)`: Solicita la lista de miembros (la respuesta llega por el listener).
- `set_member_role(group_id, user_phone, role)`: Cambia el rol (`participant`, `moderator`, `owner`, `none` para expulsar).
- `kick_member(group_id, phone)`: Expulsa a un miembro.
- `leave(group_id)`: Abandonas el grupo formalmente.

### Modificar Grupo
- `set_name(group_id, name)`: Cambia el nombre del grupo.
- `set_subject(group_id, desc)`: Cambia la descripción.
- `set_avatar(group_id, url, thumb_url="")`: Actualiza la imagen del grupo.

### Información del Grupo
- `get_group_info_by_id(group_id)`: Obtiene información completa del grupo por su ID.
- `get_group_info_by_link(invite_link)`: Obtiene información del grupo por su enlace de invitación.
- `get_group_list_paginated(limit=20, offset=0)`: Lista paginada de todos tus grupos.

### Administradores
- `promote_admin(group_id, user_phone)`: Promueve un miembro a administrador.
- `demote_admin(group_id, user_phone)`: Degradar un administrador a participante.

### Multimedia en Grupos
```python
# Nota de voz
client.send_voice_message("ID_DEL_GRUPO", url, voice_id, file_size, duration)

# Audio
client.send_audio_message("ID_DEL_GRUPO", url, audio_id, "song.mp3", file_size, duration)

# GIF
client.send_gif_message("ID_DEL_GRUPO", url, gif_id, "funny.gif", file_size)

# Reenviar mensaje
client.forward_message("ID_DEL_GRUPO", original_from, original_id)
```

---

## Canales

Los canales en ToDus requieren un formato de publicación específico (JSON en Base64), el cual la librería maneja automáticamente.

### `get_my_channels()`
Retorna de forma síncrona una lista con los JIDs de los canales donde eres administrador o suscriptor.
```python
canales = client.get_my_channels()
# Output: ['canal1@ch.todus.cu', 'noticias@ch.todus.cu']
```

### `publish_to_channel(channel_jid, publ_data)`
Publica contenido en un canal. `publ_data` debe ser un diccionario con la estructura del mensaje.

```python
data = {
    "body": "¡Hola canal!",
    "type": "text"
}
client.publish_to_channel("micanal@ch.todus.cu", data)
```

### Gestión de Membresía
- `subscribe_channel(channel_jid)`: Suscribirse a un canal público.
- `leave_channel(channel_jid)`: Desuscribirse de un canal.
- `get_channel_info(link)`: Obtener metadatos de un canal mediante su enlace corto.
- `get_channel_publications(channel_jid, last_id="", limit=25)`: Obtener historial de publicaciones.

### Administración de Canales
```python
from todus.stanzas.channel_admin import (
    get_channel_admins_iq,
    add_channel_admin_iq,
    remove_channel_admin_iq,
    edit_channel_publication_iq,
    delete_channel_publication_iq,
)

# Obtener administradores
iq = get_channel_admins_iq("canal@ch.todus.cu")
result = client.send_iq_and_wait(iq)

# Añadir administrador
iq = add_channel_admin_iq("canal@ch.todus.cu", "5350000000@im.todus.cu")
client.send_stanza(iq)

# Editar publicación
iq = edit_channel_publication_iq("canal@ch.todus.cu", "pub_id", {"body": "editado"})
client.send_stanza(iq)

# Eliminar publicación
iq = delete_channel_publication_iq("canal@ch.todus.cu", "pub_id")
client.send_stanza(iq)
```
