from todus.stanzas.utils import build_iq

def get_turn_credentials_iq(user_id: str) -> str:
    """
    Genera un IQ para solicitar credenciales temporales de TURN al servidor.

    Args:
        user_id (str): El JID o ID del usuario (típicamente uno mismo, e.g. '5350000000@im.todus.cu' o '5350000000').

    Returns:
        str: El XML de la stanza.
    """
    if not user_id.endswith("@im.todus.cu"):
        user_id = f"{user_id}@im.todus.cu"
        
    query = "<query xmlns='todus:turn:cred'/>"
    return build_iq("get", user_id, query)

def call_status_iq(to_user: str, from_user: str, status: str, content: str = "{}") -> str:
    """
    Genera un IQ para enviar eventos de señalización de WebRTC (Call Status).

    Args:
        to_user (str): Número del usuario destino (ej. '5350000000').
        from_user (str): Número del usuario origen (ej. '5351111111').
        status (str): Estado de la llamada ('CALL', 'PICKED', 'END', 'offer', 'answer', 'ice-candidate').
        content (str, opcional): Payload de la señalización (JSON con SDP o ICE).

    Returns:
        str: El XML de la stanza.
    """
    to_jid = f"{to_user}@im.todus.cu" if not to_user.endswith("@im.todus.cu") else to_user
    
    # Limpiamos los JID para los atributos internos (generalmente ToDus usa 'numero' a secas o 'numero@im.todus.cu', mantenemos el valor limpio)
    query = (
        f"<query xmlns='todus:call:status' "
        f"to_user='{to_user}' "
        f"from_user='{from_user}' "
        f"status='{status}' "
        f"content='{content}'/>"
    )
    return build_iq("set", to_jid, query)
