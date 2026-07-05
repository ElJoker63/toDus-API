"""Generadores de stanzas para administración de Canales de ToDus."""

import hashlib
from .utils import iq
from .. import util


def get_channel_admins_iq(channel_jid: str, msg_id: str = "") -> str:
    """Obtiene la lista de administradores de un canal."""
    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    if "@" not in channel_jid:
        channel_jid = f"{channel_jid}@ch.todus.cu"
    payload = "<query xmlns='todus:ch:getadmins'/>"
    return iq(type_="get", iq_id=mid, payload=payload, to=channel_jid)


def add_channel_admin_iq(channel_jid: str, user_jid: str, msg_id: str = "") -> str:
    """Añade un administrador al canal."""
    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    if "@" not in channel_jid:
        channel_jid = f"{channel_jid}@ch.todus.cu"
    payload = f"<query xmlns='todus:ch:addadmin' user='{user_jid}'/>"
    return iq(type_="set", iq_id=mid, payload=payload, to=channel_jid)


def remove_channel_admin_iq(channel_jid: str, user_jid: str, msg_id: str = "") -> str:
    """Elimina un administrador del canal."""
    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    if "@" not in channel_jid:
        channel_jid = f"{channel_jid}@ch.todus.cu"
    payload = f"<query xmlns='todus:ch:removeadmin' user='{user_jid}'/>"
    return iq(type_="set", iq_id=mid, payload=payload, to=channel_jid)


def edit_channel_publication_iq(channel_jid: str, pub_id: str, publ_data: dict | str, msg_id: str = "") -> str:
    """Edita una publicación existente en un canal."""
    import json
    from base64 import b64encode

    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    if "@" not in channel_jid:
        channel_jid = f"{channel_jid}@ch.todus.cu"

    if isinstance(publ_data, dict):
        publ_str = json.dumps(publ_data)
    else:
        publ_str = publ_data

    publ_b64 = b64encode(publ_str.encode("utf-8")).decode("utf-8")
    payload = f"<query xmlns='todus:ch:editpub' pub_id='{pub_id}' publ='{publ_b64}'/>"
    return iq(type_="set", iq_id=mid, payload=payload, to=channel_jid)


def delete_channel_publication_iq(channel_jid: str, pub_id: str, msg_id: str = "") -> str:
    """Elimina una publicación de un canal."""
    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    if "@" not in channel_jid:
        channel_jid = f"{channel_jid}@ch.todus.cu"
    payload = f"<query xmlns='todus:ch:deletepub' pub_id='{pub_id}'/>"
    return iq(type_="set", iq_id=mid, payload=payload, to=channel_jid)
