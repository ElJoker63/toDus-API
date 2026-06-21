"""Mixin para interacciones de Privacidad de ToDus."""

from ..stanzas import privacy

class ToDusPrivacyMixin:
    """Mixin que añade capacidades de Privacidad a los clientes ToDus."""

    def get_profile_privacy(self) -> dict:
        """Obtiene la configuración de privacidad de tu perfil de forma síncrona."""
        stanza = privacy.get_profile_privacy()
        res = self.send_iq_and_wait(stanza)
        # Parse result
        import re
        query = res.get("query", "") or res.get("query_attrs", "")
        privacy_data = {}
        for match in re.finditer(r"<item\s+name='([^']+)'\s+value='([^']+)'", query):
            privacy_data[match.group(1)] = match.group(2)
        return privacy_data

    def set_profile_privacy(self, profile_photo: str = "everyone", last: str = "everyone", info: str = "everyone") -> str:
        """Configura la privacidad de tu perfil."""
        stanza = privacy.set_profile_privacy(profile_photo, last, info)
        return self.send_stanza(stanza)

    def get_group_privacy(self) -> dict:
        """Obtiene la configuración de quién te puede añadir a grupos de forma síncrona."""
        stanza = privacy.get_group_privacy()
        res = self.send_iq_and_wait(stanza)
        # Parse result
        import re
        query = res.get("query", "") or res.get("query_attrs", "")
        privacy_data = {}
        for match in re.finditer(r"<item\s+name='([^']+)'\s+value='([^']+)'", query):
            privacy_data[match.group(1)] = match.group(2)
        return privacy_data

    def set_group_privacy(self, who_can: str = "everyone", exceptions: str = "") -> str:
        """Configura quién te puede añadir a grupos."""
        stanza = privacy.set_group_privacy(who_can, exceptions)
        return self.send_stanza(stanza)
