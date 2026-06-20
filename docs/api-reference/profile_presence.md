# Perfil y Presencia

## Perfil del Usuario

Estas funciones te permiten actualizar la información de tu propia cuenta (o del bot).

### `set_alias(alias)`
Cambia tu nombre público para mostrar (el nombre que ven los demás al agregarte).

### `set_about(bio)`
Cambia tu información (biografía).
```python
client.set_about("Bot programado en Python con toDus-API")
```

### `upload_avatar_from_file(path)`
Sube una nueva foto de perfil automáticamente gestionando los thumbnails requeridos por ToDus.
```python
client.upload_avatar_from_file("mi_logo.png")
```

---

## Presencia XMPP

El estado de conectividad en el protocolo XMPP de ToDus.

### `set_presence(status, show)`
Cambia tu estado de conectividad visible por los demás (En línea, Ausente, Ocupado).

```python
# Mostrar como "En línea"
client.set_presence("online")
```

Valores comunes para `show`: `chat`, `away`, `xa`, `dnd`.
