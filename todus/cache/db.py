"""Almacenamiento persistente basado en SQLite para ToDus."""

import os
import sqlite3
import threading
from typing import Any


class SQLiteCache:
    """Caché y base de datos local basada en SQLite con Thread Safety."""

    def __init__(self, db_path: str = "todus_cache.db") -> None:
        self.db_path = db_path
        self._local = threading.local()
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.row_factory = sqlite3.Row
            self._local.conn = conn
        return self._local.conn

    def _init_db(self) -> None:
        conn = self._get_conn()
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS kv_store (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at INTEGER
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS joined_groups (
                    group_id TEXT PRIMARY KEY,
                    title TEXT,
                    joined_at INTEGER
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS message_queue (
                    msg_id TEXT PRIMARY KEY,
                    target TEXT,
                    body TEXT,
                    payload TEXT,
                    status TEXT,
                    retry_count INTEGER DEFAULT 0,
                    max_retries INTEGER DEFAULT 5,
                    created_at INTEGER,
                    last_attempt INTEGER
                )
                """
            )

    def set(self, key: str, value: str) -> None:
        import time
        conn = self._get_conn()
        with conn:
            conn.execute(
                "INSERT INTO kv_store (key, value, updated_at) VALUES (?, ?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
                (key, value, int(time.time())),
            )

    def get(self, key: str, default: str = "") -> str:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM kv_store WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else default

    # --- Persistencia de Grupos (#19) ---

    def add_joined_group(self, group_id: str, title: str = "") -> None:
        import time
        conn = self._get_conn()
        with conn:
            conn.execute(
                "INSERT INTO joined_groups (group_id, title, joined_at) VALUES (?, ?, ?) ON CONFLICT(group_id) DO UPDATE SET title=excluded.title",
                (group_id, title, int(time.time())),
            )

    def remove_joined_group(self, group_id: str) -> None:
        conn = self._get_conn()
        with conn:
            conn.execute("DELETE FROM joined_groups WHERE group_id = ?", (group_id,))

    def get_joined_groups(self) -> list[dict]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT group_id, title, joined_at FROM joined_groups")
        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None
