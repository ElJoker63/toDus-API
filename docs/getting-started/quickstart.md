# Primeros Pasos

Este tutorial te mostrará cómo crear un bot que responda automáticamente a mensajes en menos de 20 líneas de código.

## Tu primer Bot ("Eco")

El uso más común de la librería es a través del cliente `ToDusClient`. Simplemente lo instancias con tu número de teléfono y token (o contraseña), defines las funciones para manejar eventos con decoradores `@client.on...`, y llamas a `client.run()`.

```python
from todus import ToDusClient

# Configura tus credenciales
PHONE = "5350000000"
# Si tienes token de la app oficial:
TOKEN = "tu_token_aqui" 

# O si tienes un usuario/contraseña de la API de terceros (legacy):
# PASSWORD = "tu_password"

# Inicializar cliente
client = ToDusClient(PHONE, token=TOKEN)

# Crear manejador de mensajes usando decoradores (estilo Pyrogram)
@client.on_message
def on_new_message(client: ToDusClient, msg):
    # Ignorar nuestros propios mensajes
    if msg.is_own:
        return
        
    print(f"Mensaje de {msg.sender}: {msg.text}")
    
    # Responder de vuelta (Eco)
    if msg.text:
        client.send_text_message(msg.sender, f"Me dijiste: {msg.text}")

print("Iniciando Bot...")
# run() bloqueará el hilo principal y mantendrá el cliente escuchando
client.run()
```

## Ejecución

Guarda este archivo como `bot.py` y ejecútalo:

```bash
python bot.py
```

Si tus credenciales son correctas, el bot se conectará e imprimirá en consola cualquier mensaje que le envíen, respondiendo automáticamente a la persona con el mismo texto.

---

Para aprender a enviar botones, audios o subir historias, continúa explorando la **[Referencia de la API](../api-reference/client.md)**.
