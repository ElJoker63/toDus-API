"""Generadores de stanzas para Versión/Actualización de ToDus."""

from .utils import build_iq

VERSION_JID = "im.todus.cu"


def get_update_info(msg_id: str = "") -> str:
    """Obtiene información sobre actualizaciones disponibles."""
    query = "<query xmlns='todus:version:get'/>"
    return build_iq("get", VERSION_JID, query, msg_id=msg_id)
