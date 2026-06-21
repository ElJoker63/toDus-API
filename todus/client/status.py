"""Mixin para interacciones con Estados/Historias de ToDus."""

import json
from base64 import b64encode

from ..stanzas import status
from .. import util

class ToDusStatusMixin:
    """Mixin que añade capacidades de Estados (StatusManager) a los clientes ToDus."""

    def publish_status(self, json_content: dict | str) -> str:
        """
        Publica un nuevo estado/historia.
        
        Args:
            json_content: El contenido del estado en formato JSON (dict o string).
                          ToDus espera un JSON que describe el fondo, texto, tipo de estado, etc.
        Returns:
            El msg_id (IQ id) de la petición.
        """
        if isinstance(json_content, dict):
            json_content = json.dumps(json_content)
            
        json_b64 = b64encode(json_content.encode('utf-8')).decode('utf-8')
        stanza = status.publish_status(json_b64)
        return self.send_stanza(stanza)

    def delete_status(self, status_id: str) -> str:
        """
        Borra un estado previamente publicado.
        
        Args:
            status_id: ID del estado a borrar.
        Returns:
            El msg_id de la petición.
        """
        stanza = status.delete_status(status_id)
        return self.send_stanza(stanza)

    def get_status(self, status_id: str) -> dict:
        """
        Obtiene un estado específico de forma síncrona.
        
        Args:
            status_id: ID del estado a consultar.
        Returns:
            Un diccionario con los datos del estado.
        """
        stanza = status.get_status(status_id)
        return self.send_iq_and_wait(stanza)

    def follow_user(self, phone_number: str) -> str:
        """
        Sigue los estados de un usuario.
        
        Args:
            phone_number: Número de teléfono o username a seguir.
        Returns:
            El msg_id de la petición.
        """
        uid = util.build_jid(phone_number)
        stanza = status.follow_user(uid)
        return self.send_stanza(stanza)

    def unfollow_user(self, phone_number: str) -> str:
        """
        Deja de seguir los estados de un usuario.
        
        Args:
            phone_number: Número de teléfono o username a dejar de seguir.
        Returns:
            El msg_id de la petición.
        """
        uid = util.build_jid(phone_number)
        stanza = status.unfollow_user(uid)
        return self.send_stanza(stanza)

    def get_followers(self, phone_number: str = "", limit: int = 20, offset: int = 0) -> list[str]:
        """
        Obtiene de forma síncrona la lista de seguidores de un usuario.
        
        Args:
            phone_number: Número de teléfono (opcional, por defecto el propio).
            limit: Cantidad de resultados por página.
            offset: Desplazamiento para paginación.
        Returns:
            Una lista con los números de teléfono de los seguidores.
        """
        uid = util.build_jid(phone_number) if phone_number else self.jid
        stanza = status.get_followers(uid, limit, offset)
        res = self.send_iq_and_wait(stanza)
        
        query = res.get("query_attrs", "") or res.get("query", "")
        import re
        match = re.search(r"result='([^']*)'", query)
        if match and match.group(1):
            jids = match.group(1).split(",")
            return [j.split("@")[0] for j in jids if j]
        return []

    def get_following(self, phone_number: str = "", limit: int = 20, offset: int = 0) -> list[str]:
        """
        Obtiene de forma síncrona la lista de usuarios a los que sigue un usuario.
        
        Args:
            phone_number: Número de teléfono (opcional, por defecto el propio).
            limit: Cantidad de resultados por página.
            offset: Desplazamiento para paginación.
        Returns:
            Una lista con los números de teléfono a los que sigue.
        """
        uid = util.build_jid(phone_number) if phone_number else self.jid
        stanza = status.get_following(uid, limit, offset)
        res = self.send_iq_and_wait(stanza)
        
        query = res.get("query_attrs", "") or res.get("query", "")
        import re
        match = re.search(r"result='([^']*)'", query)
        if match and match.group(1):
            jids = match.group(1).split(",")
            return [j.split("@")[0] for j in jids if j]
        return []

    def get_follower_info(self, phone_number: str) -> dict:
        """
        Obtiene información de la relación de seguimiento con un usuario de forma síncrona.
        
        Args:
            phone_number: Número del usuario a consultar.
        Returns:
            Un diccionario con la información de seguimiento.
        """
        uid = util.build_jid(phone_number)
        stanza = status.get_follower_info(uid)
        return self.send_iq_and_wait(stanza)
