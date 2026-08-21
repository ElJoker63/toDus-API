"""EventBus para registrar handlers y despachar eventos con filtros."""

import logging
from typing import Callable, Any
from .filters import EventFilter

logger = logging.getLogger("todus")


class EventBus:
    """Bus de eventos pub/sub para ToDus."""

    def __init__(self) -> None:
        self._handlers: list[tuple[Callable[[dict], None], list[EventFilter]]] = []

    def on(self, *filters: EventFilter) -> Callable:
        """Decorador o método para registrar un handler con filtros opcionales."""

        def decorator(func: Callable[[dict], None]) -> Callable[[dict], None]:
            self.add_handler(func, list(filters))
            return func

        return decorator

    def add_handler(self, handler: Callable[[dict], None], filters: list[EventFilter] | None = None) -> None:
        """Añade un handler al bus."""
        self._handlers.append((handler, filters or []))

    def remove_handler(self, handler: Callable[[dict], None]) -> None:
        """Remueve un handler del bus."""
        self._handlers = [h for h in self._handlers if h[0] != handler]

    def dispatch(self, event: dict) -> None:
        """Despacha un evento a todos los handlers cuyos filtros coincidan."""
        for handler, filters in list(self._handlers):
            try:
                if all(f.filter(event) for f in filters):
                    handler(event)
            except Exception as e:
                logger.error(f"Error procesando handler de evento {handler}: {e}", exc_info=True)

    def clear(self) -> None:
        """Limpia todos los handlers registrados."""
        self._handlers.clear()
