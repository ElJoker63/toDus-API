<h1 align="center">📱 toDus-API</h1>
<center><img src="https://raw.githubusercontent.com/ElJoker63/todus-API/main/examples/avatar.png" width="20%" height="20%"></center>

<p align="center">
  <a href="https://pypi.org/project/todus-api/"><img src="https://img.shields.io/pypi/v/todus-api" alt="PyPI"></a>
  <a href="https://pypi.org/project/todus-api/"><img src="https://img.shields.io/pypi/pyversions/todus-api" alt="Python"></a>
  <a href="https://github.com/ElJoker63/toDus-API/actions/workflows/ci.yml"><img src="https://github.com/ElJoker63/todus-api/actions/workflows/ci.yml/badge.svg?branch=main" alt="Tests"></a>
  <a href="https://github.com/ElJoker63/todus-api/actions/workflows/pypi-publish.yml"><img src="https://github.com/ElJoker63/todus-api/actions/workflows/pypi-publish.yml/badge.svg?branch=main" alt="Publish"></a>
  <a href="https://eljoker63.github.io/todus-api"><img src="https://img.shields.io/badge/docs-MkDocs-blueviolet" alt="Docs"></a>
  <a href="https://github.com/ElJoker63/todus-api/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="License"></a>
</p>

<p align="center"><strong>Cliente Python para ToDus</strong> — la plataforma de mensajería instantánea cubana.</p>

<p align="center">
  <a href="https://eljoker63.github.io/toDus-API"><b>📖 LEER LA DOCUMENTACIÓN COMPLETA AQUÍ 📖</b></a>
</p>

---

## ⚡ ¿Qué es toDus-API?

Es una librería moderna, asíncrona y orientada a eventos para interactuar con la red de ToDus. Te permite crear bots interactivos, manejar grupos y canales, enviar contenido multimedia y ver o publicar historias, todo usando Python puro.

**Cobertura del protocolo:** 100% de las funciones de la app oficial.

---

## 📦 Instalación

```bash
pip install todus-API
```

---

## 🚀 Uso Rápido (Tu primer bot)

```python
from todus import ToDusClient2

# 1. Configura tus credenciales
client = ToDusClient2("5350000000", password="tu_password")
client.login()

# 2. Crea un callback para los mensajes
def responder_mensajes(msg):
    if msg.get("body"):
        print(f"Recibido: {msg['body']}")
        client.send_message(msg['from'], f"¡Hola! Recibí: {msg['body']}")

# 3. Empieza a escuchar
print("Bot en ejecución...")
client.listen_messages(responder_mensajes)
```

---

## 📚 Documentación y Recursos

Toda la información detallada sobre **autenticación, subida de archivos, historias, canales, grupos, bloqueos y más** la encontrarás en nuestro sitio web oficial de documentación:

👉 **[https://eljoker63.github.io/toDus-API](https://eljoker63.github.io/toDus-API)**

- **ToDus oficial:** [ToDus Web](https://web.todus.cu)
- **PyPI:** [toDus-API](https://pypi.org/project/toDus-API/)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Contribuir:** [CONTRIBUTING.md](CONTRIBUTING.md)

---
<p align="center">Desarrollado con ❤️ por ElJoker63.</p>
