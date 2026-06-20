# Changelog

Todos los cambios notables en este proyecto se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

## [1.3.4] - 2026-06-20

### Fixed
- Asegurado que las operaciones de subida de archivos (`upload_file`) y avatares (`upload_avatar`) utilicen el proxy configurado al direccionarlas a través de la sesión del cliente.
- Agregados tests unitarios para verificar el comportamiento de proxies en la subida de archivos y avatares.

## [1.3.3] - 2026-06-19

### Changed
- Renombrado el paquete a `toDus-API`.

## [1.3.2] - 2026-06-19

### Fixed
- Corregido el flujo de publicación en GitHub Actions para usar `secrets.PYPI_API_TOKEN`.

## [1.3.1] - 2026-06-19

### Added
- Soporte inicial para proxy HTTP y SOCKS5 en peticiones HTTP y sockets XMPP.

## [1.3.0] - 2026-06-19

### Added
- Soporte completo para grupos MUC Light (`GroupClient`)
- Roles de grupo (`GroupRole`) y eventos de grupo (`GroupEvent`)
- Auto-detección de destino privado/grupo en `ToDusClient2`
- Envío de mensajes de ubicación (`send_location_message`)
- Envío de mensajes de eventos/calendario (`send_event_message`)
- Callbacks específicos por grupo (`on_group_message`)
- Firma de URLs con nombre legible de archivo (`sanitize_filename`)
- Soporte de progreso en subidas (`progress_callback`)
- Módulo `stanzas/` reorganizado en subdirectorio
- Módulo `client/` reorganizado en subdirectorio con mixins
- `pyproject.toml` moderno (PEP 621)
- Tests unitarios con pytest
- CI/CD con GitHub Actions

### Changed
- Estructura interna reorganizada para claridad
- Migración de `setup.py` a `pyproject.toml`

## [1.2.0] - 2026-06-01

### Added
- Envío de stickers (`send_sticker_message`)
- Envío de contactos (`send_contact_message`)
- Envío de botones interactivos (`send_button_message`)
- Edición de mensajes (`edit_message`)
- Eliminación de mensajes (`delete_message`)
- Parser incremental de stanzas XMPP (`IncrementalParser`)

## [1.1.0] - 2026-05-15

### Added
- Envío de imágenes con dimensiones y thumbnail
- Envío de videos con metadata
- Subida y descarga de archivos con `FileType`
- Perfil de usuario (alias, bio, avatar)
- Utilidades: `format_size`, `get_image_dimensions`, `generate_blurhash`

## [1.0.0] - 2026-05-01

### Added
- Cliente básico XMPP para ToDus (`ToDusClient`)
- Cliente stateful con auto-login (`ToDusClient2`)
- Autenticación por SMS + JWT
- Envío y recepción de mensajes de texto
- Manejo de excepciones personalizadas
- Constantes del protocolo ToDus

[1.3.4]: https://github.com/ElJoker63/toDus-API/compare/v1.3.3...v1.3.4
[1.3.3]: https://github.com/ElJoker63/toDus-API/compare/v1.3.2...v1.3.3
[1.3.2]: https://github.com/ElJoker63/toDus-API/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/ElJoker63/toDus-API/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/ElJoker63/toDus-API/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/ElJoker63/toDus-API/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/ElJoker63/toDus-API/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ElJoker63/toDus-API/releases/tag/v1.0.0
