"""Mixin para interacciones de Bloqueos de ToDus."""

from ..stanzas import block
from .. import util

class ToDusBlockMixin:
    """Mixin que añade capacidades de Bloqueo a los clientes ToDus."""

    def block_user(self, phone_number: str) -> str:
        """Bloquea a un usuario para que no pueda enviarte mensajes ni ver tus estados."""
        jid = util.build_jid(phone_number)
        stanza = block.block_user(jid)
        return self.send_stanza(stanza)

    def unblock_user(self, phone_number: str) -> str:
        """Desbloquea a un usuario."""
        jid = util.build_jid(phone_number)
        stanza = block.unblock_user(jid)
        return self.send_stanza(stanza)

    def get_block_list(self) -> list[str]:
        """Obtiene la lista completa de usuarios bloqueados de forma síncrona."""
        stanza = block.get_block_list()
        res = self.send_iq_and_wait(stanza)
        # Parse result
        import re
        query = res.get("query", "") or res.get("query_attrs", "")
        blocked = []
        for match in re.finditer(r"<item\s+jid='([^']+)'", query):
            jid = match.group(1)
            blocked.append(jid.split("@")[0])
        return blocked

    def get_block_list_paginated(self, limit: int = 20, offset: int = 0) -> list[str]:
        """Obtiene la lista de usuarios bloqueados de forma paginada de forma síncrona."""
        stanza = block.get_block_list_paginated(limit, offset)
        res = self.send_iq_and_wait(stanza)
        # Parse result
        import re
        query = res.get("query", "") or res.get("query_attrs", "")
        blocked = []
        for match in re.finditer(r"<item\s+jid='([^']+)'", query):
            jid = match.group(1)
            blocked.append(jid.split("@")[0])
        return blocked
