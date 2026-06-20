# toDus-API

Bienvenido a la documentación oficial de **toDus-API**, el cliente de Python para interactuar con el protocolo de mensajería instantánea cubana ToDus.

## ¿Qué es toDus-API?

Es una librería asíncrona (basada en eventos) que te permite crear bots y clientes automatizados para la plataforma ToDus. La librería maneja por debajo todo el complejo protocolo XMPP (Jabber) y las extensiones MUC Light que usa ToDus internamente.

![toDus-API Logo](https://raw.githubusercontent.com/ElJoker63/toDus-API/main/examples/avatar.png)

## Características Principales

- **Cobertura 100% de la API Oficial:** Todo lo que puedes hacer en la aplicación oficial, lo puedes hacer con código.
- **Eficiente y Rápida:** Conexión XMPP optimizada con manejo inteligente del token y keepalives.
- **Soporte Multimedia:** Sube y descarga imágenes, audios, documentos y videos.
- **Grupos y Canales:** Administra grupos MUC Light, y el nuevo sistema de Canales.
- **Historias y Estados:** Soporte nativo para visualizar estados y publicar nuevas historias.
- **Bots Interactivos:** Capacidad para enviar botones interactivos (In-Line keyboards).
- **Diseño "Event-Driven":** Usa decoradores `@client.on_message` al estilo de librerías modernas como Pyrogram o Telethon.

---

> Continúa con la [Instalación](getting-started/installation.md) o salta a los [Primeros Pasos](getting-started/quickstart.md).
