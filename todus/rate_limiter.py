"""Controlador de tasa de envío (Rate Limiter) para evitar baneo por parte de ToDus."""

import logging
import threading
import time

logger = logging.getLogger("todus")


class RateLimiter:
    """Garantiza un intervalo mínimo entre envíos consecutivos para evitar desbordar el servidor."""

    def __init__(self, max_per_second: float = 2.0) -> None:
        self.min_interval = 1.0 / max_per_second if max_per_second > 0 else 0.0
        self.last_send = 0.0
        self._lock = threading.Lock()

    def set_rate(self, max_per_second: float) -> None:
        with self._lock:
            self.min_interval = 1.0 / max_per_second if max_per_second > 0 else 0.0

    def wait(self) -> None:
        """Bloquea si es necesario hasta que haya transcurrido el intervalo mínimo."""
        with self._lock:
            now = time.time()
            elapsed = now - self.last_send
            if elapsed < self.min_interval:
                sleep_time = self.min_interval - elapsed
                time.sleep(sleep_time)
            self.last_send = time.time()
