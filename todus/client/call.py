from ..stanzas import call
from .. import util

class ToDusCallMixin:
    """Mixin que añade capacidades de Señalización de Llamadas (WebRTC) a los clientes ToDus."""

    def request_turn_credentials(self) -> str:
        """
        Solicita las credenciales temporales de TURN al servidor.
        El servidor responderá con un IQ de tipo 'result' que contiene 
        los servidores TURN, nombre de usuario y contraseña para WebRTC.

        Returns:
            La stanza enviada.
        """
        # Se envía al propio usuario (el jid actual del cliente)
        iq = call.get_turn_credentials_iq(self.jid)
        return self.send_stanza(iq)

    def send_call_status(self, to_phone: str, status: str, content: str = "{}"):
        """
        Envía un evento de señalización de llamada (WebRTC) a otro usuario.

        Args:
            to_phone (str): El número de teléfono del destinatario.
            status (str): El estado o evento (ej. 'CALL', 'PICKED', 'END', 'offer', 'answer', 'ice-candidate').
            content (str): Payload de datos, usualmente un JSON que contiene SDP o información de ICE.

        Returns:
            La stanza enviada.
        """
        to_user = util.build_jid(to_phone)
        from_user = self.jid
        iq = call.call_status_iq(to_user=to_user, from_user=from_user, status=status, content=content)
        return self.send_stanza(iq)

    def start_call(self, phone_number: str, content: str = "{}") -> str:
        """Inicia la señalización de una llamada hacia un usuario."""
        return self.send_call_status(phone_number, "CALL", content)

    def pickup_call(self, phone_number: str, content: str = "{}") -> str:
        """Responde a una llamada entrante."""
        return self.send_call_status(phone_number, "PICKED", content)

    def end_call(self, phone_number: str, reason: str = "{}") -> str:
        """Finaliza o cuelga una llamada."""
        return self.send_call_status(phone_number, "END", reason)

    def reject_call(self, phone_number: str, reason: str = "{}") -> str:
        """Rechaza una llamada entrante."""
        return self.send_call_status(phone_number, "REJECTED", reason)
