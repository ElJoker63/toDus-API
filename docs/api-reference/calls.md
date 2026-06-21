# API de Llamadas (WebRTC)

ToDus soporta llamadas de audio y videollamadas mediante la integración de **WebRTC** de manera P2P (Peer-to-Peer) o utilizando sus servidores TURN (relays).

A diferencia de muchos clientes XMPP que utilizan la extensión Jingle estándar (XEP-0166) para la señalización, ToDus ha implementado su propio mecanismo de señalización con las etiquetas personalizadas `<query xmlns='todus:turn:cred'/>` y `<query xmlns='todus:call:status'/>`.

> [!WARNING]  
> **Esta API provee exclusivamente la SEÑALIZACIÓN (Signaling).** 
> 
> Para realizar una llamada completa con audio/video en Python, necesitarás usar la librería `aiortc` (u otra equivalente) para capturar tus medios, generar la oferta SDP (Session Description Protocol) y los candidatos ICE, y empaquetarlos en formato JSON para enviarlos con la API de `toDus-API`.

## Obtener Credenciales TURN

Para que WebRTC pueda traspasar routers y firewalls NAT estrictos, se necesitan servidores **STUN** y **TURN**. ToDus no tiene estos servidores fijos en su código; se deben pedir de manera dinámica al servidor principal antes de llamar.

```python
# Esto pedirá las credenciales TURN y la contraseña temporal.
turn_response = client.request_turn_credentials()
print(turn_response)
```

## Enviar eventos de Llamada (Call Status)

Para llamar a alguien o responder, se utiliza el método `send_call_status()`. 

La API tiene varios métodos de conveniencia que utilizan internamente `send_call_status()`:

```python
# 1. Iniciar llamada (Enviar oferta SDP)
target_phone = "5350000000"
offer_sdp = '{"type": "offer", "sdp": "..."}' 
client.start_call(target_phone, content=offer_sdp)

# 2. Contestar una llamada entrante (PICKED)
answer_sdp = '{"type": "answer", "sdp": "..."}' 
client.pickup_call(target_phone, content=answer_sdp)

# 3. Rechazar una llamada entrante
client.reject_call(target_phone)

# 4. Finalizar / Colgar llamada activa
client.end_call(target_phone)
```

## Estructura de `send_call_status`

Si deseas enviar un estado personalizado o negociaciones ICE intermedias (Trickle ICE), puedes usar el método base:

```python
client.send_call_status(
    to_phone="5350000000",
    status="ice-candidate", # o el estado correspondiente
    content='{"candidate": "...", "sdpMid": "0", "sdpMLineIndex": 0}'
)
```

### Tabla de Estados Identificados
Durante las llamadas de ToDus, típicamente se intercambian los siguientes estados en el parámetro `status`:

| Estado | Descripción |
| ------ | ----------- |
| `CALL` | Inicia la llamada. El `content` suele llevar el SDP offer. |
| `PICKED` | El destinatario contesta. El `content` lleva el SDP answer. |
| `END` | Cualquiera de las partes termina la llamada (Cuelga). |
| `REJECTED` | El destinatario rechazó la llamada entrante. |

Para observar y responder automáticamente a llamadas entrantes, debes usar `listen_messages()` y procesar los IQ de señalización.
