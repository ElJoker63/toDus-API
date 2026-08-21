# Eventos, Colas y Control de Tasa (v1.6.1+)

Esta sección describe las herramientas avanzadas introducidas en la v1.6.1 para construir bots robustos con arquitectura basada en eventos, colas con reintentos automáticos, almacenamiento persistente en SQLite, control de frecuencia y transporte WebSocket.

---

## Bus de Eventos (`EventBus`)

El `EventBus` permite suscribir múltiples controladores (handlers) a los eventos entrantes y filtrarlos utilizando reglas compuestas.

```python
from todus import ToDusClient2, PhoneFilter, TextFilter, CommandFilter

client = ToDusClient2("5350000000", password="tu_password")
client.login()

# Filtrar mensajes de un teléfono específico
@client.bus.on(PhoneFilter("5351234567"))
def handler_telefono(event):
    print("Mensaje recibido de 5351234567:", event.get("body"))

# Filtrar comandos que inicien con /ayuda
@client.bus.on(CommandFilter("ayuda"))
def handler_comando(event):
    client.send_message(event["from"], "Usa /start para iniciar el bot.")

# Iniciar escucha pasando el despachador del bus
client.listen_messages(client.bus.dispatch)
```

### Filtros Disponibles

| Filtro | Descripción | Ejemplo |
|--------|-------------|---------|
| `PhoneFilter(from_phone)` | Filtra por teléfono del remitente (normaliza JIDs completos `53...@im.todus.cu/resource`). | `PhoneFilter("5351234567")` |
| `GroupFilter(group_id=None)` | Filtra mensajes provenientes de grupos MUC Light. | `GroupFilter("group_123")` |
| `TextFilter(text, exact=False)` | Coincidencia de texto en el cuerpo del mensaje. | `TextFilter("hola", exact=True)` |
| `RegexFilter(pattern)` | Expresión regular sobre el cuerpo del mensaje. | `RegexFilter(r"^\d{6}$")` |
| `CommandFilter(command, prefix="/")` | Filtra comandos por prefijo. | `CommandFilter("start")` |

---

## Cola de Mensajes con Auto-Reintento (`MessageQueue`)

La clase `MessageQueue` persiste los mensajes salientes en SQLite y cuenta con un trabajador en segundo plano que los reintenta automáticamente si se pierden por caídas de red o desconexiones del servidor.

```python
# Añadir mensaje a la cola persistente
client.queue.enqueue(
    msg_id="msg_001",
    target="5351234567",
    body="Mensaje con auto-reintento",
    max_retries=5
)
```

- **Estados de Mensaje (`MessageStatus`):** `PENDING`, `SENDING`, `SENT`, `FAILED`.
- **Trabajador de Fondo:** Se inicia automáticamente al vincular un cliente autenticado (`client.queue.start_retry_worker()`).

---

## Caché y Persistencia en SQLite (`SQLiteCache`)

Gestión de almacenamiento local SQLite para mantener configuraciones, metadatos y la lista de **grupos unidos** (`joined_groups`) de forma persistente a través de reinicios del proceso.

```python
# Consultar grupos unidos guardados
grupos = client.cache.get_joined_groups()

# Guardar valor clave-valor genérico
client.cache.set("clave", "valor")
```

---

## Control de Tasa (`RateLimiter`)

Previene baneos por desbordamiento de peticiones asegurando un intervalo mínimo entre envíos consecutivos.

```python
# Configurar límite máximo de 2 mensajes por segundo (por defecto)
client.rate_limiter.set_rate(max_per_second=2.0)

# Espera automática en cada envío (integrado transparentemente en ToDusClientBase)
client.rate_limiter.wait()
```

---

## Transporte WebSocket (`WebSocketTransport`)

Proporciona una abstracción de conexión alternativa sobre WebSocket (`wss://im.todus.cu/ws`) para entornos corporativos o redes con proxies que bloquean puertos TCP directos.

```python
from todus import WebSocketTransport

ws = WebSocketTransport(ws_url="wss://im.todus.cu/ws", timeout=30)
ws.connect()
ws.send(b"<stream:stream ...>")
```

---

## Archivo de Mensajes XMPP MAM (`get_message_archive`)

Permite consultar el historial de mensajes guardados en el servidor mediante Message Archive Management (MAM).

```python
# Consultar historial reciente
query_id = client.get_message_archive(limit=50, since="2026-08-01T00:00:00Z")
```
