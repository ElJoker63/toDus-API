# Instalación

Para utilizar `todus-API`, necesitas tener Python instalado en tu ordenador. Se recomienda encarecidamente utilizar Python 3.11 o superior.

## Instalación desde PyPI

Puedes instalar la última versión estable directamente desde PyPI usando `pip`:

```bash
pip install todus-API
```

## Instalación desde Código Fuente (GitHub)

Si quieres instalar la versión más reciente en desarrollo:

```bash
git clone https://github.com/ElJoker63/toDus-API.git
cd toDus-API
pip install -e .
```

## Dependencias

La librería no depende de pesados frameworks asíncronos externos. Utiliza la librería estándar de Python (`socket`, `ssl`, `threading`) optimizada para alto rendimiento. Opcionalmente, puedes necesitar un proxy si tu entorno lo requiere.

---

Siguiente paso: **[Primeros Pasos](quickstart.md)**.
