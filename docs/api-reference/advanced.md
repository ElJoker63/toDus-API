# Avanzado

Estas funcionalidades corresponden a elementos menos comunes o que actúan sobre sistemas paralelos de ToDus (Llamadas P2P, Geolocalización).

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

Aun sin voz real, puedes hacer que el teléfono de la otra persona "timbre" o reaccionar a llamadas entrantes a tu bot.

### `start_call(phone_number)`
Inicia una llamada. El dispositivo de la otra persona empezará a timbrar indicando que lo llamas.

### `pickup_call(phone_number)`
Responde una llamada entrante a nivel de señalización (el otro teléfono dejará de timbrar y se asumirá que la llamada conectó).

### `reject_call(phone_number)`
Rechaza o ignora activamente una llamada entrante (enviarás al destinatario la notificación de que declinaste).

### `end_call(phone_number)`
Finaliza una llamada en curso y cierra la conexión.
