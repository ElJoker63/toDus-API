import logging
from .base import ToDusClientBase
from ..stanzas import channels as ch_stanzas
from ..errors import AuthenticationError

class ToDusChannelMixin(ToDusClientBase):
    """Mixin que agrupa las operaciones relacionadas con los canales."""
    
    def create_channel(self, name: str, link: str, public: int = 1, desc: str = "", picture: str = "", subs: list[str] = None) -> str:
        """
        Crea un nuevo canal en ToDus.
        
        Args:
            name: El nombre del canal.
            link: Enlace único (sin el @).
            public: 1 si es público, 0 si es privado.
            desc: Descripción del canal.
            picture: URL de la foto del canal.
            subs: Lista opcional de números de teléfono a añadir inicialmente.
            
        Returns:
            El msg_id de la petición IQ enviada.
        """
        if not self.logged or not self.token:
            raise AuthenticationError("Se requiere haber iniciado sesión (login).")
            
        iq_xml = ch_stanzas.create_channel_iq(
            name=name,
            link=link,
            public=public,
            desc=desc,
            picture=picture,
            subs=subs
        )
        
        with self._xmpp_session(self.token) as sock:
            sock.send(iq_xml.encode())
            
        import re
        match = re.search(r" i='([^']+)'", iq_xml)
        return match.group(1) if match else ""
        
    def publish_to_channel(self, channel_jid: str, publ_data: dict | str) -> str:
        """
        Publica un mensaje en el canal especificado.
        
        Args:
            channel_jid: El JID o enlace del canal.
            publ_data: El contenido del mensaje (usualmente un dict que se convertirá a JSON).
            
        Returns:
            El msg_id de la petición IQ.
        """
        if not self.logged or not self.token:
            raise AuthenticationError("Se requiere haber iniciado sesión (login).")
            
        iq_xml = ch_stanzas.publish_to_channel_iq(channel_jid, publ_data)
        
        with self._xmpp_session(self.token) as sock:
            sock.send(iq_xml.encode())
            
        import re
        match = re.search(r" i='([^']+)'", iq_xml)
        return match.group(1) if match else ""

    def subscribe_channel(self, channel_jid: str) -> str:
        """
        Se suscribe a un canal público.
        """
        if not self.logged or not self.token:
            raise AuthenticationError("Se requiere haber iniciado sesión (login).")
            
        iq_xml = ch_stanzas.subscribe_channel_iq(channel_jid)
        
        with self._xmpp_session(self.token) as sock:
            sock.send(iq_xml.encode())
            
        import re
        match = re.search(r" i='([^']+)'", iq_xml)
        return match.group(1) if match else ""
        
    def leave_channel(self, channel_jid: str) -> str:
        """
        Abandona o se desuscribe de un canal.
        """
        if not self.logged or not self.token:
            raise AuthenticationError("Se requiere haber iniciado sesión (login).")
            
        iq_xml = ch_stanzas.leave_channel_iq(channel_jid)
        
        with self._xmpp_session(self.token) as sock:
            sock.send(iq_xml.encode())
            
        import re
        match = re.search(r" i='([^']+)'", iq_xml)
        return match.group(1) if match else ""

    def get_my_channels(self) -> str:
        """
        Solicita la lista de canales a los que el usuario está suscrito o es administrador.
        """
        if not self.logged or not self.token:
            raise AuthenticationError("Se requiere haber iniciado sesión (login).")
            
        iq_xml = ch_stanzas.get_my_channels_iq()
        
        with self._xmpp_session(self.token) as sock:
            sock.send(iq_xml.encode())
            
        import re
        match = re.search(r" i='([^']+)'", iq_xml)
        return match.group(1) if match else ""
        
    def get_channel_info(self, channel_link: str) -> str:
        """
        Solicita la información de un canal mediante su enlace.
        """
        if not self.logged or not self.token:
            raise AuthenticationError("Se requiere haber iniciado sesión (login).")
            
        iq_xml = ch_stanzas.get_channel_info_iq(channel_link)
        
        with self._xmpp_session(self.token) as sock:
            sock.send(iq_xml.encode())
            
        import re
        match = re.search(r" i='([^']+)'", iq_xml)
        return match.group(1) if match else ""
        
    def get_channel_publications(self, channel_jid: str, last_id: str = "", limit: int = 25) -> str:
        """
        Solicita la lista paginada de las últimas publicaciones de un canal.
        """
        if not self.logged or not self.token:
            raise AuthenticationError("Se requiere haber iniciado sesión (login).")
            
        iq_xml = ch_stanzas.get_channel_publications_iq(channel_jid, last_id, limit)
        
        with self._xmpp_session(self.token) as sock:
            sock.send(iq_xml.encode())
            
        import re
        match = re.search(r" i='([^']+)'", iq_xml)
        return match.group(1) if match else ""
