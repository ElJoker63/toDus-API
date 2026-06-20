# Cliente Core

La clase `ToDusClient` es el punto de entrada principal para interactuar con la API.

## `ToDusClient`

```python
class ToDusClient(phone: str, password: str = "", token: str = "", proxy: dict = None)
```

Inicializa el cliente de ToDus.

**Parámetros:**
- `phone` *(str)*: El número de teléfono con o sin código de país (ej. `"5350000000"`).
- `password` *(str, opcional)*: La contraseña si usas la API no oficial de ToDus (legacy).
- `token` *(str, opcional)*: El token JWT si lo extrajiste de la app oficial. Se requiere uno de los dos (password o token).
- `proxy` *(dict, opcional)*: Diccionario con credenciales SOCKS5 para conectarse a través de un proxy corporativo (útil en Cuba).

**Ejemplo de Proxy:**
```python
proxy = {
    "ip": "10.0.0.1",
    "port": 1080,
    "user": "tu_usuario",
    "password": "tu_password"
}
client = ToDusClient("5350000000", token="...", proxy=proxy)
```

---

## Decoradores (Handlers)

El cliente usa decoradores para registrar funciones que se ejecutarán asíncronamente cuando ocurran eventos.

### `@client.on_message`

Se dispara cuando recibes un mensaje nuevo (texto, imagen, archivo, etc) o cuando se modifica uno.

```python
@client.on_message
def mi_funcion(client, msg):
    print(f"Nuevo mensaje de {msg.sender}")
```

### `@client.on_terminal_event`

Se dispara cuando ocurren eventos de sistema en el cliente (como cuando se conecta con éxito, o recibe un error).

```python
@client.on_terminal_event
def en_evento(client, evt):
    if evt.type == "ready":
        print("¡Conectado a ToDus!")
```

## Métodos de Ejecución

### `run()`

Bloquea el hilo actual y mantiene el cliente en ejecución perpetua (o hasta que se pierda la conexión irrecuperablemente o el usuario pulse Ctrl+C).

```python
client.run()
```
