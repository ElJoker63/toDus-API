"""Cola de mensajes con persistencia SQLite y trabajador de reintentos automático."""

import json
import logging
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, TYPE_CHECKING
from .db import SQLiteCache

if TYPE_CHECKING:
    from ..client import ToDusClient2

logger = logging.getLogger("todus")


class MessageStatus(str, Enum):
    PENDING = "pending"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"


@dataclass
class OutgoingMessage:
    msg_id: str
    target: str
    body: str
    payload: dict
    status: MessageStatus
    retry_count: int = 0
    max_retries: int = 5
    created_at: int = 0
    last_attempt: int = 0


class MessageQueue:
    """Cola de mensajes salientes con soporte para auto-reintento."""

    def __init__(self, db: SQLiteCache | None = None, client: Any = None, auto_start_worker: bool = True) -> None:
        self.db = db or SQLiteCache()
        self.client = client
        self._running = False
        self._worker_thread: threading.Thread | None = None
        if auto_start_worker and self.client:
            self.start_retry_worker()

    def set_client(self, client: Any) -> None:
        """Establece la instancia de cliente usada para enviar mensajes."""
        self.client = client
        if not self._running and client:
            self.start_retry_worker()

    def enqueue(self, msg_id: str, target: str, body: str, payload: dict | None = None, max_retries: int = 5) -> OutgoingMessage:
        """Añade un mensaje a la cola en estado PENDING."""
        now = int(time.time())
        msg = OutgoingMessage(
            msg_id=msg_id,
            target=target,
            body=body,
            payload=payload or {},
            status=MessageStatus.PENDING,
            retry_count=0,
            max_retries=max_retries,
            created_at=now,
            last_attempt=0,
        )
        conn = self.db._get_conn()
        with conn:
            conn.execute(
                """
                INSERT INTO message_queue (msg_id, target, body, payload, status, retry_count, max_retries, created_at, last_attempt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(msg_id) DO UPDATE SET
                    target=excluded.target, body=excluded.body, payload=excluded.payload, status=excluded.status
                """,
                (
                    msg.msg_id,
                    msg.target,
                    msg.body,
                    json.dumps(msg.payload),
                    msg.status.value,
                    msg.retry_count,
                    msg.max_retries,
                    msg.created_at,
                    msg.last_attempt,
                ),
            )
        return msg

    def update_status(self, msg_id: str, status: MessageStatus, retry_count: int | None = None) -> None:
        """Actualiza el estado de un mensaje en la cola."""
        now = int(time.time())
        conn = self.db._get_conn()
        with conn:
            if retry_count is not None:
                conn.execute(
                    "UPDATE message_queue SET status = ?, retry_count = ?, last_attempt = ? WHERE msg_id = ?",
                    (status.value, retry_count, now, msg_id),
                )
            else:
                conn.execute(
                    "UPDATE message_queue SET status = ?, last_attempt = ? WHERE msg_id = ?",
                    (status.value, now, msg_id),
                )

    def dequeue_pending(self, limit: int = 50) -> list[OutgoingMessage]:
        """Obtiene mensajes pendientes o con fallos pendientes de reintento."""
        conn = self.db._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT msg_id, target, body, payload, status, retry_count, max_retries, created_at, last_attempt
            FROM message_queue
            WHERE status IN ('pending', 'failed') AND retry_count < max_retries
            ORDER BY created_at ASC
            LIMIT ?
            """,
            (limit,),
        )
        results = []
        for row in cursor.fetchall():
            payload_dict = {}
            if row["payload"]:
                try:
                    payload_dict = json.loads(row["payload"])
                except Exception:
                    pass
            results.append(
                OutgoingMessage(
                    msg_id=row["msg_id"],
                    target=row["target"],
                    body=row["body"],
                    payload=payload_dict,
                    status=MessageStatus(row["status"]),
                    retry_count=row["retry_count"],
                    max_retries=row["max_retries"],
                    created_at=row["created_at"],
                    last_attempt=row["last_attempt"],
                )
            )
        return results

    def start_retry_worker(self) -> None:
        """Inicia el hilo trabajador de reintentos."""
        if self._running:
            return
        self._running = True
        self._worker_thread = threading.Thread(target=self._retry_worker_loop, daemon=True)
        self._worker_thread.start()

    def stop_retry_worker(self) -> None:
        """Detiene el hilo trabajador de reintentos."""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=2.0)
            self._worker_thread = None

    def _retry_worker_loop(self) -> None:
        """Trabajador de fondo que reintenta enviar mensajes fallidos/pendientes."""
        logger.info("MessageQueue retry worker iniciado")
        while self._running:
            try:
                if not self.client or not getattr(self.client, "logged", False):
                    time.sleep(3)
                    continue

                pending = self.dequeue_pending(limit=20)
                for msg in pending:
                    if not self._running:
                        break

                    logger.info(f"Reintentando envío de mensaje {msg.msg_id} a {msg.target} (Intento {msg.retry_count + 1}/{msg.max_retries})")
                    self.update_status(msg.msg_id, MessageStatus.SENDING, retry_count=msg.retry_count + 1)
                    
                    try:
                        # Si hay un método específico en el payload, usarlo
                        msg_type = msg.payload.get("msg_type", "text")
                        if msg_type == "text":
                            self.client.send_message(msg.target, msg.body)
                        elif hasattr(self.client, f"send_{msg_type}_message"):
                            send_fn = getattr(self.client, f"send_{msg_type}_message")
                            send_fn(to=msg.target, **msg.payload.get("kwargs", {}))
                        else:
                            self.client.send_message(msg.target, msg.body)
                        
                        self.update_status(msg.msg_id, MessageStatus.SENT)
                        logger.info(f"Mensaje {msg.msg_id} reenviado exitosamente")
                    except Exception as e:
                        logger.warning(f"Error reenviando mensaje {msg.msg_id}: {e}")
                        new_status = MessageStatus.FAILED if (msg.retry_count + 1) >= msg.max_retries else MessageStatus.PENDING
                        self.update_status(msg.msg_id, new_status)
                        
                    time.sleep(1) # Pequeña pausa entre envíos

            except Exception as e:
                logger.error(f"Error en worker loop de MessageQueue: {e}")

            time.sleep(1)
        self.db.close()
