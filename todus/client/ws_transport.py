"""Transporte alternativo por WebSocket para ToDus en entornos con proxies/firewalls restrictivos."""

import logging
import socket
from typing import Any

logger = logging.getLogger("todus")


class WebSocketTransport:
    """Simulador/Abstracción de transporte WebSocket para ToDus XMPP sobre WSS."""

    def __init__(self, ws_url: str = "wss://im.todus.cu/ws", timeout: int = 30) -> None:
        self.ws_url = ws_url
        self.timeout = timeout
        self._ws = None

    def connect(self) -> Any:
        """Conecta al servidor WebSocket de ToDus."""
        try:
            import websocket
        except ImportError:
            raise ImportError("Se requiere el paquete 'websocket-client' para usar WebSocket transport. Instálalo con 'pip install websocket-client'")

        self._ws = websocket.create_connection(self.ws_url, timeout=self.timeout)
        return self._ws

    def send(self, data: bytes | str) -> None:
        if not self._ws:
            raise OSError("WebSocket no está conectado")
        if isinstance(data, bytes):
            self._ws.send_binary(data)
        else:
            self._ws.send(data)

    def recv(self, bufsize: int = 8192) -> bytes:
        if not self._ws:
            raise OSError("WebSocket no está conectado")
        msg = self._ws.recv()
        if isinstance(msg, str):
            return msg.encode("utf-8")
        return msg

    def close(self) -> None:
        if self._ws:
            try:
                self._ws.close()
            except Exception:
                pass
            self._ws = None
