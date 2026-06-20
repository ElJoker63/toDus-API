# Bloqueos y Privacidad

ToDus proporciona controles de privacidad muy granulares y listas negras de contactos directamente accesibles desde su protocolo XMPP.

## Privacidad del Perfil

Configura quién puede acceder a información de tu perfil. En los parámetros de las siguientes funciones, los valores comunes suelen ser `"everyone"` (Todos), `"contacts"` (Mis Contactos), o `"nobody"` (Nadie).

### `set_profile_privacy(profile_photo, last, info)`
Define la privacidad global de tu perfil.
```python
# Nadie podrá ver tu foto, pero tus contactos podrán ver tu "última vez en línea"
client.set_profile_privacy(profile_photo="nobody", last="contacts", info="everyone")
```

### `set_group_privacy(who_can, exceptions)`
Establece quién puede añadirte a nuevos grupos sin tu permiso.
```python
# Solo los contactos pueden agregarte a grupos
client.set_group_privacy(who_can="contacts", exceptions="")
```

---

## Lista Negra (Bloqueos)

### `block_user(phone_number)`
Bloquea un usuario, prohibiéndole que te envíe mensajes directos o que acceda a tus estados.
```python
client.block_user("5350000000")
```

### `unblock_user(phone_number)`
Desbloquea a un usuario previamente bloqueado.

### `get_block_list()`
Obtiene la lista completa de todos los usuarios que tienes bloqueados.
