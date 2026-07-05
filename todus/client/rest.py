"""Mixin para interacciones REST API de ToDus (stickers, certified, linked devices, report, link preview)."""

import json
import logging
from .. import constants

logger = logging.getLogger("todus")


class ToDusRestMixin:
    """Mixin que añade capacidades REST API a los clientes ToDus."""

    # --- Stickers ---

    def get_sticker_packs(self, limit: int = 20, offset: int = 0, title: str = "") -> dict:
        """Obtiene la lista de packs de stickers disponibles."""
        params = {"limit": limit, "offset": offset}
        if title:
            params["title"] = title
        headers = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": f"ToDus {self.version_name} Auth",
        }
        try:
            resp = self.session.get(
                f"{constants.STICKERS_URL}/v1/stickers/packs/{limit}/{offset}",
                params=params,
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json() if resp.content else {}
        except Exception as e:
            logger.error(f"Error getting sticker packs: {e}")
            return {}

    def get_sticker_pack_info(self, pack_name: str) -> dict:
        """Obtiene la información de un pack de stickers específico."""
        headers = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": f"ToDus {self.version_name} Auth",
        }
        try:
            resp = self.session.get(
                f"{constants.STICKERS_URL}/v1/stickers/info/{pack_name}",
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json() if resp.content else {}
        except Exception as e:
            logger.error(f"Error getting sticker pack info: {e}")
            return {}

    # --- Certified / Cards ---

    def get_certified_info(self, uid: str) -> dict:
        """Obtiene la información de usuario certificado (card)."""
        headers = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": f"ToDus {self.version_name} Auth",
        }
        try:
            resp = self.session.get(
                f"{constants.CHAT_URL}/card/info/{uid}",
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json() if resp.content else {}
        except Exception as e:
            logger.error(f"Error getting certified info: {e}")
            return {}

    def subscribe_certified(self, uid: str) -> bool:
        """Se suscribe a las actualizaciones de un usuario certificado."""
        headers = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": f"ToDus {self.version_name} Auth",
        }
        try:
            resp = self.session.get(
                f"{constants.CHAT_URL}/card/subscribe/{uid}",
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error subscribing to certified: {e}")
            return False

    def unsubscribe_certified(self, uid: str) -> bool:
        """Se desuscribe de las actualizaciones de un usuario certificado."""
        headers = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": f"ToDus {self.version_name} Auth",
        }
        try:
            resp = self.session.get(
                f"{constants.CHAT_URL}/card/unsubscribe/{uid}",
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error unsubscribing from certified: {e}")
            return False

    # --- Linked Devices ---

    def get_linked_devices(self) -> list[dict]:
        """Obtiene la lista de dispositivos vinculados."""
        headers = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": f"ToDus {self.version_name} Auth",
        }
        try:
            resp = self.session.get(
                f"{constants.CLIENT_URL}/list",
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("sessions", [])
        except Exception as e:
            logger.error(f"Error getting linked devices: {e}")
            return []

    def logout_linked_device(self, session_id: str) -> bool:
        """Cierra la sesión de un dispositivo vinculado."""
        headers = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": f"ToDus {self.version_name} Auth",
            "Content-Type": "application/json",
        }
        try:
            resp = self.session.post(
                f"{constants.CLIENT_URL}/logout",
                json={"sessionId": session_id},
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error logging out linked device: {e}")
            return False

    # --- Report ---

    def report_message(self, message_id: str, reason: str = "", description: str = "") -> bool:
        """Reporta un mensaje al servidor."""
        headers = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": f"ToDus {self.version_name} Auth",
            "Content-Type": "application/json",
        }
        body = {"message_id": message_id}
        if reason:
            body["reason"] = reason
        if description:
            body["description"] = description
        try:
            resp = self.session.post(
                f"{constants.CHAT_URL}/v1/report",
                json=body,
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error reporting message: {e}")
            return False

    # --- Link Preview ---

    def get_link_preview(self, url: str) -> dict:
        """Obtiene la previsualización de una URL (OpenGraph/OG data)."""
        headers = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": f"ToDus {self.version_name} Auth",
            "Content-Type": "application/json",
        }
        try:
            resp = self.session.post(
                f"{constants.AUTH_URL}/v3/preview",
                json={"url": url},
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json() if resp.content else {}
        except Exception as e:
            logger.error(f"Error getting link preview: {e}")
            return {}

    # --- App Version ---

    def check_app_version(self) -> dict:
        """Verifica si hay actualizaciones disponibles de la app ToDus."""
        headers = {
            "User-Agent": f"ToDus {self.version_name} Auth",
        }
        try:
            resp = self.session.get(
                f"{constants.CHAT_URL}/todus/release/rel/latest",
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json() if resp.content else {}
        except Exception as e:
            logger.error(f"Error checking app version: {e}")
            return {}
