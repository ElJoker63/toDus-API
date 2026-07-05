"""Generadores de stanzas para Roster (Contactos) de ToDus."""

from .utils import build_iq

ROSTER_JID = "im.todus.cu"


def get_roster_hash(msg_id: str = "") -> str:
    """Obtiene el hash del roster actual."""
    query = "<query xmlns='jabber:iq:roster' ver='1'/>"
    return build_iq("get", ROSTER_JID, query, msg_id=msg_id)


def get_roster_paginated(limit: int = 50, offset: int = 0, msg_id: str = "") -> str:
    """Obtiene la lista de contactos de forma paginada."""
    query = f"<query xmlns='todus:roster:get' limit='{limit}' offset='{offset}'/>"
    return build_iq("get", ROSTER_JID, query, msg_id=msg_id)


def get_roster_version(msg_id: str = "") -> str:
    """Obtiene la versión actual del roster."""
    query = "<query xmlns='todus:roster:version'/>"
    return build_iq("get", ROSTER_JID, query, msg_id=msg_id)


def update_roster_version(version: str, msg_id: str = "") -> str:
    """Actualiza la versión del roster."""
    query = f"<query xmlns='todus:roster:version' ver='{version}'/>"
    return build_iq("set", ROSTER_JID, query, msg_id=msg_id)


def update_roster_entry(jid: str, name: str = "", groups: list[str] = None, msg_id: str = "") -> str:
    """Actualiza una entrada del roster (añade o modifica contacto)."""
    name_attr = f" name='{name}'" if name else ""
    groups_xml = ""
    if groups:
        for g in groups:
            groups_xml += f"<group>{g}</group>"
    query = f"<query xmlns='jabber:iq:roster'><item jid='{jid}'{name_attr}>{groups_xml}</item></query>"
    return build_iq("set", ROSTER_JID, query, msg_id=msg_id)


def delete_roster_entry(jid: str, msg_id: str = "") -> str:
    """Elimina un contacto del roster."""
    query = f"<query xmlns='jabber:iq:roster'><item jid='{jid}' subscription='remove'/></query>"
    return build_iq("set", ROSTER_JID, query, msg_id=msg_id)


def get_todus_id(phone: str, msg_id: str = "") -> str:
    """Obtiene el ToDus ID (@username) de un usuario."""
    jid = f"{phone}@im.todus.cu" if "@" not in phone else phone
    query = "<query xmlns='todus:users:gettodusid'/>"
    return build_iq("get", jid, query, msg_id=msg_id)


def edit_todus_id(new_id: str, msg_id: str = "") -> str:
    """Cambia el ToDus ID (@username) del usuario."""
    query = f"<query xmlns='todus:users:updatetodusid' todus_id='{new_id}'/>"
    return build_iq("set", ROSTER_JID, query, msg_id=msg_id)


def get_users_info(jids: list[str], msg_id: str = "") -> str:
    """Obtiene información de múltiples usuarios."""
    items = "".join(f"<item jid='{j}'/>" for j in jids)
    query = f"<query xmlns='todus:users:info'>{items}</query>"
    return build_iq("get", ROSTER_JID, query, msg_id=msg_id)
