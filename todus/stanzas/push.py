"""Generadores de stanzas para Push (Firebase) de ToDus."""

from .utils import build_iq

PUSH_JID = "im.todus.cu"


def register_push(firebase_token: str, msg_id: str = "") -> str:
    """Registra el token de Firebase para notificaciones push."""
    query = f"<query xmlns='todus:push:register' token='{firebase_token}'/>"
    return build_iq("set", PUSH_JID, query, msg_id=msg_id)


def unregister_push(msg_id: str = "") -> str:
    """Des registra el token de Firebase."""
    query = "<query xmlns='todus:push:unregister'/>"
    return build_iq("set", PUSH_JID, query, msg_id=msg_id)
