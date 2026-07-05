"""Tipos y enumeraciones de ToDus."""

from enum import IntEnum, StrEnum


class FileType(IntEnum):
    """Tipos de archivo soportados por ToDus."""
    FILE = 0
    VOICE = 1
    AUDIO = 2
    VIDEO = 3
    PICTURE = 4
    PROFILE = 5
    PROFILE_THUMBNAIL = 6
    PRODUCT = 7
    BACKUP = 8
    NEWS = 9
    STREAM_VIDEO = 10
    STATUS_IMAGE = 11


class ChatState(StrEnum):
    """Estados de chat XEP-0085."""
    COMPOSING = "composing"
    PAUSED = "paused"
    ACTIVE = "active"
    GONE = "gone"
    INACTIVE = "inactive"


class MessageType(StrEnum):
    """Tipos de mensaje XMPP."""
    CHAT = "chat"
    GROUPCHAT = "groupchat"
    ERROR = "error"
    HEADLINE = "headline"
    NORMAL = "normal"


class PresenceShow(StrEnum):
    """Estados de presencia XMPP."""
    CHAT = "chat"
    AWAY = "away"
    XA = "xa"
    DND = "dnd"


class ButtonSize(StrEnum):
    """Tamaños de botón interactivo."""
    FULL = "0.82"
    HALF = "0.5"


class ButtonCommand(StrEnum):
    """Tipos de comando para botones interactivos."""
    SEND = "cmd_type_send"
    URL = "cmd_type_url"
    COPY = "cmd_type_copy"
    CALL = "cmd_type_call"
    ADD_SHORTCUT = "cmd_add_shortcut"
    COPY_TO_CLIPBOARD = "cmd_copy_to_clipboard"
    OPEN_APP_SCREEN = "cmd_open_app_screen"
    OPEN_WEB = "cmd_open_web"
    PLACEHOLDER = "cmd_placeholder"
    PLACEHOLDER_CONTACT_SEND = "cmd_placeholder_contact_send"
    PLACEHOLDER_SEND = "cmd_placeholder_send"
