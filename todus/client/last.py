"""Mixin para interacciones de Última Conexión de ToDus."""

from ..stanzas import last
from .. import util

class ToDusLastMixin:
    """Mixin que añade capacidades de consultar Última Conexión a los clientes ToDus."""

    def get_last_seen(self, phone_number: str) -> dict:
        """Obtiene la última vez que un usuario estuvo conectado de forma síncrona."""
        jid = util.build_jid(phone_number)
        stanza = last.get_last_seen(jid)
        res = self.send_iq_and_wait(stanza)
        # Parse result
        import re
        query = res.get("query", "") or res.get("query_attrs", "")
        last_data = {}
        match = re.search(r"seconds='([^']+)'", query)
        if match:
            last_data["seconds"] = match.group(1)
        return last_data
