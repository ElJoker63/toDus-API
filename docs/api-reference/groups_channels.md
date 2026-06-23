# Grupos y Canales

ToDus usa la extensión MUC Light para sus grupos, y una variante avanzada para canales.

## Grupos MUC Light

La clase `ToDusClient2` provee acceso a la gestión de grupos a través del atributo `.groups`.

### `join(group_id)`
Te unes a un grupo existente mediante su ID.
```python
client.groups.join("ID_DEL_GRUPO")
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
