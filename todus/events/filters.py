"""Filtros para el EventBus de ToDus."""

import re
from typing import Callable, Any


class EventFilter:
    """Clase base para filtros de eventos."""

    def filter(self, event: dict) -> bool:
        raise NotImplementedError


class PhoneFilter(EventFilter):
    """Filtra eventos por número de teléfono del remitente."""

    def __init__(self, from_phone: str) -> None:
        self.from_phone = str(from_phone).strip().lstrip("+")

    def filter(self, event: dict) -> bool:
        raw_phone = event.get("from") or event.get("sender_phone") or event.get("sender", "") or ""
        phone = str(raw_phone)
        if "/" in phone:
            phone = phone.split("/", 1)[0]
        if "@" in phone:
            phone = phone.split("@", 1)[0]
        phone = phone.lstrip("+")
        return self.from_phone == phone


class GroupFilter(EventFilter):
    """Filtra eventos por ID de grupo o mensajería de grupo MUC Light."""

    def __init__(self, group_id: str | None = None) -> None:
        self.group_id = group_id

    def filter(self, event: dict) -> bool:
        is_group = event.get("type") == "gc" or "group_id" in event or "muclight" in str(event.get("from", ""))
        if not is_group:
            return False
        if self.group_id:
            event_group = event.get("group_id") or event.get("from", "")
            return self.group_id in str(event_group)
        return True


class TextFilter(EventFilter):
    """Filtra eventos de mensaje por coincidencia exacta o substring en el cuerpo."""

    def __init__(self, text: str, exact: bool = False, case_sensitive: bool = False) -> None:
        self.text = text if case_sensitive else text.lower()
        self.exact = exact
        self.case_sensitive = case_sensitive

    def filter(self, event: dict) -> bool:
        body = event.get("body", "")
        if not body:
            return False
        target = body if self.case_sensitive else body.lower()
        if self.exact:
            return target == self.text
        return self.text in target


class RegexFilter(EventFilter):
    """Filtra eventos por expresión regular sobre el cuerpo del mensaje."""

    def __init__(self, pattern: str, flags: int = 0) -> None:
        self.regex = re.compile(pattern, flags)

    def filter(self, event: dict) -> bool:
        body = event.get("body", "")
        if not body:
            return False
        return bool(self.regex.search(body))


class CommandFilter(EventFilter):
    """Filtra comandos que inicien con prefijo especificado (por defecto '/')."""

    def __init__(self, command: str, prefix: str = "/") -> None:
        self.command = command.lstrip(prefix).lower()
        self.prefix = prefix

    def filter(self, event: dict) -> bool:
        body = (event.get("body") or "").strip()
        if not body.startswith(self.prefix):
            return False
        parts = body[len(self.prefix):].split()
        if not parts:
            return False
        return parts[0].lower() == self.command
