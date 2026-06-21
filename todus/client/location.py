"""Mixin para interacciones de Ubicación (Near) de ToDus."""

from ..stanzas import location

class ToDusLocationMixin:
    """Mixin que añade capacidades de Ubicación a los clientes ToDus."""

    def set_location(self, lat: float, lon: float) -> str:
        """Comparte tu ubicación geográfica en el sistema 'Cerca de mí'."""
        stanza = location.set_location(lat, lon)
        return self.send_stanza(stanza)

    def hide_location(self) -> str:
        """Oculta tu ubicación para no aparecer en 'Cerca de mí'."""
        stanza = location.hide_location()
        return self.send_stanza(stanza)

    def get_people_near(self, limit: int = 20, offset: int = 0) -> list[dict]:
        """Busca personas cerca de tu ubicación actual de forma síncrona."""
        stanza = location.get_people_near(limit, offset)
        res = self.send_iq_and_wait(stanza)
        # Parse result
        import re
        query = res.get("query", "") or res.get("query_attrs", "")
        people = []
        for match in re.finditer(r"<item\s+jid='([^']+)'", query):
            jid = match.group(1)
            people.append({"jid": jid, "phone": jid.split("@")[0]})
        return people

    def get_near_status(self) -> dict:
        """Obtiene tu configuración actual de visibilidad de ubicación de forma síncrona."""
        stanza = location.get_near_status()
        res = self.send_iq_and_wait(stanza)
        # Parse result
        import re
        query = res.get("query", "") or res.get("query_attrs", "")
        status_data = {}
        # Asumiendo que ToDus responde con atributos o items
        match = re.search(r"status='([^']+)'", query)
        if match:
            status_data["status"] = match.group(1)
        return status_data
