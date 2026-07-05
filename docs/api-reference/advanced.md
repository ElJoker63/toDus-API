# Avanzado

Estas funcionalidades corresponden a elementos menos comunes o que actúan sobre sistemas paralelos de ToDus (Contactos, REST API, Geolocalización).

## Roster (Contactos)

Gestiona tu lista de contactos directamente desde la API.

### `get_roster(limit=50, offset=0)`
Obtiene la lista de contactos del usuario de forma paginada.
```python
contacts = client.get_roster()
# Output: [{"jid": "5351111111@im.todus.cu", "phone": "5351111111", "name": "Juan"}]
```

### `add_contact(phone, name="")`
Añade un contacto al roster.
```python
client.add_contact("5351111111", "Juan Pérez")
```

### `delete_contact(phone)`
Elimina un contacto del roster.
```python
client.delete_contact("5351111111")
```

### `get_todus_id(phone)`
Obtiene el ToDus ID (@username) de un usuario.
```python
username = client.get_todus_id("5351111111")
# Output: "juan_perez"
```

### `edit_todus_id(new_id)`
Cambia tu propio ToDus ID (@username).
```python
client.edit_todus_id("mi_nuevo_username")
```

### `get_users_info(phones)`
Obtiene información de múltiples usuarios.
```python
info = client.get_users_info(["5351111111", "5352222222"])
```

---

## REST API (Stickers, Certificados, Dispositivos)

La librería incluye acceso a los endpoints REST oficiales de ToDus.

### Stickers

```python
# Listar packs de stickers
packs = client.get_sticker_packs(limit=20, offset=0)

# Información de un pack específico
info = client.get_sticker_pack_info("pack_animales")
```

### Usuarios Certificados (Cards)

```python
# Obtener info de usuario certificado
info = client.get_certified_info("5351111111")

# Suscribirse a actualizaciones
client.subscribe_certified("5351111111")

# Desuscribirse
client.unsubscribe_certified("5351111111")
```

### Dispositivos Vinculados

```python
# Listar dispositivos vinculados
devices = client.get_linked_devices()

# Cerrar sesión de un dispositivo
client.logout_linked_device("session_id_aqui")
```

### Reportar Mensajes

```python
client.report_message("msg_id", reason="spam", description="Contenido no deseado")
```

### Previsualización de Enlaces

```python
preview = client.get_link_preview("https://ejemplo.com/articulo")
# Output: {"title": "...", "description": "...", "image": "...", ...}
```

### Verificar Versión de App

```python
version_info = client.check_app_version()
```

---

## Última Conexión (Last Seen)

### `get_last_seen(phone_number)`
Envía una petición al servidor y espera síncronamente la respuesta para averiguar la marca de tiempo de la última vez que un usuario estuvo en línea. Devuelve un diccionario con el valor, por ejemplo: `{"seconds": "1718841234"}`.

## Ubicación (Personas Cerca)

El sistema de geolocalización o *Near* de ToDus permite a los usuarios encontrarse basándose en su ubicación geográfica.

### `set_location(lat, lon)`
Publica tus coordenadas en la red.
```python
client.set_location(23.1136, -82.3666)  # Coordenadas de La Habana
```

### `hide_location()`
Revoca temporalmente tu visibilidad geográfica.

### `get_people_near(limit, offset)`
Pide a ToDus la lista de personas que se encuentren físicamente cerca de tu posición reportada más reciente. Devuelve de forma síncrona una lista de diccionarios, cada uno conteniendo el número de teléfono y JID de las personas cercanas.

---

## Señalización de Llamadas (P2P)

> [!WARNING]
> La transmisión de voz y video en tiempo real ocurre mediante WebRTC utilizando servidores TURN. **toDus-API** no incluye un motor WebRTC, pero sí provee toda la señalización XMPP necesaria por si decides integrar tu propio stack de WebRTC.

### `start_call(phone_number)`
Inicia una llamada. El dispositivo de la otra persona empezará a timbrar indicando que lo llamas.

### `pickup_call(phone_number)`
Responde una llamada entrante a nivel de señalización.

### `reject_call(phone_number)`
Rechaza o ignora activamente una llamada entrante.

### `end_call(phone_number)`
Finaliza una llamada en curso y cierra la conexión.

### `request_turn_credentials()`
Solicita credenciales temporales de STUN/TURN para WebRTC.

---

## Push (Firebase)

```python
from todus.stanzas.push import register_push, unregister_push

# Registrar token de Firebase
iq = register_push("firebase_token_aqui")
client.send_stanza(iq)

# Des-registrar
iq = unregister_push()
client.send_stanza(iq)
```

## Verificar Versión del Servidor

```python
from todus.stanzas.version import get_update_info

iq = get_update_info()
result = client.send_iq_and_wait(iq)
```
