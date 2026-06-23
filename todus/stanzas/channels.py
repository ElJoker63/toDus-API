import hashlib
import json
from base64 import b64encode
from .utils import iq
from .. import util

def create_channel_iq(name: str, link: str, public: int = 1, desc: str = "", picture: str = "", subs: list[str] = None, msg_id: str = "") -> str:
    """
    Genera el IQ para crear un nuevo canal.
    """
    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    
    attrs = []
    if name: attrs.append(f"name='{util.escape_xml(name)}'")
    if picture: attrs.append(f"profile_photo='{util.escape_xml(picture)}'")
    if link: attrs.append(f"link='{util.escape_xml(link)}'")
    attrs.append(f"public='{public}'")
    if subs: attrs.append(f"subs='{util.escape_xml(','.join(subs))}'")
    if desc: attrs.append(f"desc='{util.escape_xml(desc)}'")
    
    attr_str = " ".join(attrs)
    payload = f"<query xmlns='todus:ch:create' {attr_str}/>"
    return iq(type_="set", iq_id=mid, payload=payload, to="ch")

def publish_to_channel_iq(channel_jid: str, publ_data: dict | str, msg_id: str = "") -> str:
    """
    Genera el IQ para publicar en un canal. 
    ToDus espera el contenido del mensaje (publ) como JSON codificado en Base64.
    """
    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    
    if isinstance(publ_data, dict):
        publ_str = json.dumps(publ_data)
    else:
        publ_str = publ_data
        
    publ_b64 = b64encode(publ_str.encode("utf-8")).decode("utf-8")
    
    if "@" not in channel_jid:
        channel_jid = f"{channel_jid}@ch.todus.cu"
        
    payload = f"<query xmlns='todus:ch:publish' publ='{publ_b64}'/>"
    return iq(type_="set", iq_id=mid, payload=payload, to=channel_jid)

def subscribe_channel_iq(channel_jid: str, msg_id: str = "") -> str:
    """
    Genera el IQ para suscribirse a un canal.
    """
    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    
    if "@" not in channel_jid:
        channel_jid = f"{channel_jid}@ch.todus.cu"
        
    payload = f"<query xmlns='todus:ch:subscribe'/>"
    return iq(type_="set", iq_id=mid, payload=payload, to=channel_jid)

def leave_channel_iq(channel_jid: str, msg_id: str = "") -> str:
    """
    Genera el IQ para salir de un canal.
    """
    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    
    if "@" not in channel_jid:
        channel_jid = f"{channel_jid}@ch.todus.cu"
        
    payload = f"<query xmlns='todus:ch:leave'/>"
    return iq(type_="set", iq_id=mid, payload=payload, to=channel_jid)

def get_channel_publications_iq(channel_jid: str, last_id: str = "", limit: int = 25, msg_id: str = "") -> str:
    """
    Genera el IQ para recuperar las publicaciones de un canal.
    """
    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    
    if "@" not in channel_jid:
        channel_jid = f"{channel_jid}@ch.todus.cu"
        
    attrs = []
    if last_id: attrs.append(f"last_id='{util.escape_xml(last_id)}'")
    if limit: attrs.append(f"limit='{limit}'")
    
    attr_str = " ".join(attrs) if attrs else ""
    payload = f"<query xmlns='todus:ch:getpub' {attr_str}/>"
    return iq(type_="get", iq_id=mid, payload=payload, to=channel_jid)

def get_my_channels_iq(msg_id: str = "") -> str:
    """
    Genera el IQ para listar los canales del usuario actual.
    """
    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    
    payload = f"<query xmlns='todus:ch:my_channels:2'/>"
    return iq(type_="get", iq_id=mid, payload=payload, to="ch")

def get_channel_info_iq(channel_link: str, msg_id: str = "") -> str:
    """
    Genera el IQ para obtener información de un canal mediante su enlace.
    """
    mid = msg_id or hashlib.md5(util.generate_token(16).encode()).hexdigest()
    
    payload = f"<query xmlns='todus:ch:info:link:v2' link='{util.escape_xml(channel_link)}'/>"
    return iq(type_="get", iq_id=mid, payload=payload, to="ch")
