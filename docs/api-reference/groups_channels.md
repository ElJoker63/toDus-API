# Grupos y Canales

ToDus usa la extensión MUC Light para sus grupos, y una variante para canales.

## Grupos

### `create_group(name, users)`
Crea un nuevo grupo con un nombre y una lista de miembros iniciales.
```python
client.create_group("Mi Grupo Python", ["5350000000", "5351111111"])
```

### Administrar Miembros
- `add_users_to_group(group_jid, users)`: Añade nuevos participantes.
- `remove_user_from_group(group_jid, user)`: Elimina (expulsa) a un miembro.
- `leave_group(group_jid)`: Abandonas el grupo voluntariamente.
- `set_group_admin(group_jid, user)`: Promueve a un usuario a administrador.

### Modificar Grupo
- `set_group_name(group_jid, name)`
- `set_group_avatar(group_jid, avatar_url)`

## Canales

Los canales son similares a los grupos pero diseñados para difusión de un solo sentido (o pocos publicadores).

### `create_channel(name, description)`
Crea un canal público o privado.
```python
client.create_channel("Noticias ToDus", "Canal de prueba de la API")
```

### `subscribe_channel(channel_jid)`
Te suscribe a un canal existente para empezar a recibir sus actualizaciones.

### Administrar Canal
- `publish_channel_message(channel_jid, text)`: Envía un mensaje como administrador del canal.
- `get_channel_subscribers(channel_jid)`: Obtén la lista de suscriptores.
