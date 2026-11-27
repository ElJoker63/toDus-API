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
        """Reserva slot bajo lock y espera fuera del lock el intervalo mínimo."""
        with self._lock:
            if self.min_interval <= 0:
                return
            now = time.time()
            next_allowed = self.last_send + self.min_interval
            if next_allowed > now:
                sleep_time = next_allowed - now
                self.last_send = next_allowed
            else:
                sleep_time = 0.0
                self.last_send = now
        if sleep_time > 0:
            time.sleep(sleep_time)
