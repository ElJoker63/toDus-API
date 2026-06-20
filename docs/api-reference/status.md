# Estados (Historias)

Soporte completo para visualizar y publicar historias/estados de 24 horas al estilo de ToDus.

## Publicar un Estado

Los estados en ToDus viajan empaquetados como JSON en Base64. La librería convierte diccionarios de Python a este formato automáticamente.

```python
estado = {
    "text": "¡Hola mundo desde la API de Python!",
    "bg_color": "#ff0000",
    "font": 1
}

# La librería convierte esto a Base64 y lo sube
client.publish_status(estado)
```

## Interacción con Usuarios

- `follow_user(phone_number)`: Comienza a seguir las historias de alguien. Te empezarán a llegar por medio del decorador `@client.on_status` si lo defines.
- `unfollow_user(phone_number)`: Deja de seguir las historias de un usuario.
- `get_followers()`: Pide a la API de ToDus la lista de personas que pueden ver tus historias publicadas.
- `get_following()`: Pide a la API la lista de personas a las que sigues.
