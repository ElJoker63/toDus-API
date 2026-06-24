"""Cliente XMPP/HTTP para ToDus, unificado mediante Mixins."""

import logging
import socket
import time
import re
from base64 import b64encode
from typing import Callable

from .base import ToDusClientBase
from .auth import ToDusAuthMixin
from .message import ToDusMessageMixin
from .file import ToDusFileMixin
from .profile import ToDusProfileMixin
from .channels import ToDusChannelMixin
from .status import ToDusStatusMixin
from .privacy import ToDusPrivacyMixin
from .block import ToDusBlockMixin
from .last import ToDusLastMixin
from .location import ToDusLocationMixin
from .call import ToDusCallMixin
from ..errors import AuthenticationError, TokenExpiredError, ConnectionLostError
from ..types import FileType
from .. import util, parser, stanza

logger = logging.getLogger("todus")


class ToDusClient(
    ToDusAuthMixin,
    ToDusMessageMixin,
    ToDusFileMixin,
    ToDusProfileMixin,
    ToDusChannelMixin,
    ToDusStatusMixin,
    ToDusPrivacyMixin,
    ToDusBlockMixin,
    ToDusLastMixin,
    ToDusLocationMixin,
    ToDusCallMixin,
    ToDusClientBase,
):
    """Cliente unificado para la API de ToDus."""
    pass


class ToDusClient2(ToDusClient):
    """Cliente con persistencia de credenciales, soporte para grupos y auto-detección de destino."""

    def __init__(self, phone_number: str, password: str = "", proxy: str | None = None, **kwargs) -> None:
        super().__init__(proxy=proxy, **kwargs)
        self.phone_number = util.normalize_phone(phone_number) if phone_number else ""
        self.password = (password or "").strip()
        self._token = ""
        self._group_client = None

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, value: str):
        self._token = value

    @property
    def registered(self) -> bool:
        return bool(self.phone_number and self.password)

    @property
    def logged(self) -> bool:
        return bool(self._token)

    @property
    def jid(self) -> str:
        """JID asociado al cliente."""
        if self.phone_number:
            return util.build_jid(self.phone_number)
        return ""

    @property
    def groups(self):
        """Acceso al cliente de grupos MUC Light."""
        if self._group_client is None:
            from ..group import GroupClient
            self._group_client = GroupClient(self)
        return self._group_client

    def login(self, phone: str = None, password: str = None) -> str:
        phone = phone or self.phone_number
        password = password or self.password
        if not phone or not password:
            raise AuthenticationError("Faltan credenciales (teléfono o contraseña)")
        self._token = super().login(phone, password)
        self.phone_number = util.normalize_phone(phone)
        return self._token

    def request_code(self, phone: str = None) -> None:
        phone = phone or self.phone_number
        super().request_code(phone)
        self.phone_number = util.normalize_phone(phone)

    def validate_code(self, code: str, phone: str = None) -> str:
        phone = phone or self.phone_number
        self.password = super().validate_code(phone, code)
        self.phone_number = util.normalize_phone(phone)
        return self.password

    def send_stanza(self, stanza_str: str) -> str:
        """
        Envía una stanza XML genérica usando el token actual.
        """
        if not self._token:
            raise AuthenticationError("No autenticado: token ausente")
        with self._xmpp_session(self._token) as sock:
            sock.send(stanza_str.encode())
        
        match = re.search(r" i=['\"]([^'\"]+)['\"]", stanza_str)
        return match.group(1) if match else ""

    def send_iq_and_wait(self, stanza_str: str, timeout: int = 15) -> dict:
        """
        Envía una stanza IQ y espera su respuesta de forma síncrona.
        """
        if not self._token:
            raise AuthenticationError("No autenticado")
            
        match = re.search(r" i=['\"]([^'\"]+)['\"]", stanza_str)
        iq_id = match.group(1) if match else ""
        
        with self._xmpp_session(self._token) as sock:
            sock.send(stanza_str.encode())
            if not iq_id:
                return {}
                
            start_time = time.time()
            while (time.time() - start_time) < timeout:
                response = self._recv_all(sock)
                if response is None:
                    raise ConnectionLostError("Conexión perdida esperando respuesta IQ")
                if response == "":
                    continue
                
                if f"i='{iq_id}'" in response or f'i="{iq_id}"' in response:
                    stanzas = parser.extract_all_stanzas(response)
                    for iq_str in stanzas.get("iqs", []):
                        if f"i='{iq_id}'" in iq_str or f'i="{iq_id}"' in iq_str:
                            return parser.parse_iq(iq_str)
                    
                    if "t='result'" in response or "t='error'" in response:
                        return parser.parse_iq(response)
        return {}

    def _is_group_target(self, target: str) -> bool:
        """Determina si el destino es un grupo o un teléfono."""
        if not target: return False
        if "@" in target:
            return "muclight" in target
        # Los teléfonos cubanos son 10 dígitos empezando por 53
        return not (target.isdigit() and len(target) == 10 and target.startswith("53"))

    # --- Mensajería ---

    def send_message(self, to: str, body: str, reply_to: str = "") -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        if self._is_group_target(to):
            return self.groups.send_message(to, body)
        return super().send_message(self._token, util.build_jid(to), body, reply_to=reply_to)

    def edit_message(self, to: str, new_body: str, original_msg_id: str) -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        if self._is_group_target(to):
            return self.groups.edit_message(to, new_body, original_msg_id)
        return super().edit_message(self._token, util.build_jid(to), new_body, original_msg_id)

    def delete_message(self, to: str, message_id: str, body: str = "", media_xml: str = "") -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        if self._is_group_target(to):
            return self.groups.delete_message(to, message_id, body=body, media_xml=media_xml)
        return super().delete_message(self._token, util.build_jid(to), message_id, body=body, media_xml=media_xml)

    def send_file_message(self, to: str, url: str, file_type: FileType, caption: str = "", file_name: str = "", file_size: int = 0, reply_to: str = "") -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        if self._is_group_target(to):
            return self.groups.send_file(to, url, file_name, file_size, caption)
        return super().send_file_message(self._token, util.build_jid(to), url, file_type, caption, file_name=file_name, file_size=file_size, reply_to=reply_to)

    def send_image_message(self, to: str, url: str, file_name: str, file_size: int, width: int = 0, height: int = 0, thumbnail: str = "", caption: str = "", reply_to: str = "") -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        if self._is_group_target(to):
            return self.groups.send_image(to, url, file_name, file_size, width, height, thumbnail, caption, reply_to=reply_to)
        return super().send_image_message(
            token=self._token,
            to_jid=util.build_jid(to),
            url=url,
            file_name=file_name,
            file_size=file_size,
            width=width,
            height=height,
            thumbnail=thumbnail,
            caption=caption,
            reply_to=reply_to
        )

    def send_video_message(self, to: str, url: str, video_id: str, file_name: str, file_size: int, duration: int, width: int, height: int, thumbnail: str, info_text: str = "", reply_to: str = "") -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        if self._is_group_target(to):
            return self.groups.send_video(to, url, video_id, file_name, file_size, duration, width, height, thumbnail, info_text, reply_to=reply_to)
        return super().send_video_message(
            token=self._token,
            to_jid=util.build_jid(to),
            url=url,
            video_id=video_id,
            file_name=file_name,
            file_size=file_size,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            info_text=info_text,
            reply_to=reply_to
        )

    def send_image_message_simple(self, to: str, url: str, file_name: str, file_size: int, reply_to: str = "") -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        if self._is_group_target(to):
            return self.groups.send_image(to, url, file_name, file_size, 0, 0, "", "", reply_to=reply_to)
        return super().send_image_message_simple(self._token, util.build_jid(to), url, file_name, file_size, reply_to=reply_to)

    def send_sticker_message(self, to: str, sticker_id: str, sticker_name: str, sticker_pack: str, sticker_hash: str, reply_to: str = "") -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        if self._is_group_target(to):
            return self.groups.send_sticker(to, sticker_id, sticker_name, sticker_pack, sticker_hash)
        return super().send_sticker_message(self._token, util.build_jid(to), sticker_id, sticker_name, sticker_pack, sticker_hash, reply_to=reply_to)

    def send_chat_state(self, to: str, state: str) -> None:
        if not self._token: raise AuthenticationError("No autenticado")
        super().send_chat_state(self._token, util.build_jid(to), state)

    def send_location_message(self, to: str, lat: float, lon: float, zoom: float = 11.0, text: str = "", reply_to: str = "") -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        if self._is_group_target(to):
            return self.groups.send_location(to, lat, lon, zoom, text)
        return super().send_location_message(self._token, util.build_jid(to), lat, lon, zoom, text, reply_to=reply_to)

    def send_read_receipt(self, to: str, msg_id: str) -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        return super().send_read_receipt(self._token, util.build_jid(to), msg_id)

    # --- Canales ---

    def get_my_channels(self) -> list[str]:
        """
        Obtiene de forma síncrona la lista de JIDs de los canales del usuario.
        """
        if not self._token: raise AuthenticationError("No autenticado")
        stanza_str = stanza.channels.get_my_channels_iq()
        res = self.send_iq_and_wait(stanza_str)
        
        query_attrs = res.get("query_attrs", "")
        match = re.search(r"channels=['\"]([^'\"]+)['\"]", query_attrs)
        if match:
            channels_str = match.group(1)
            return [c.strip() for c in channels_str.split(",") if c.strip()]
        return []

    def get_channel_info(self, channel_link: str) -> dict:
        """
        Obtiene de forma síncrona la información de un canal.
        """
        if not self._token: raise AuthenticationError("No autenticado")
        stanza_str = stanza.channels.get_channel_info_iq(channel_link)
        return self.send_iq_and_wait(stanza_str)

    def get_channel_publications(self, channel_jid: str, last_id: str = "", limit: int = 25) -> dict:
        """
        Obtiene de forma síncrona las publicaciones de un canal.
        """
        if not self._token: raise AuthenticationError("No autenticado")
        stanza_str = stanza.channels.get_channel_publications_iq(channel_jid, last_id, limit)
        return self.send_iq_and_wait(stanza_str)

    def publish_to_channel(self, channel_jid: str, publ_data: dict | str) -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        stanza_str = stanza.channels.publish_to_channel_iq(channel_jid, publ_data)
        return self.send_stanza(stanza_str)

    def subscribe_channel(self, channel_jid: str) -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        stanza_str = stanza.channels.subscribe_channel_iq(channel_jid)
        return self.send_stanza(stanza_str)

    def leave_channel(self, channel_jid: str) -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        stanza_str = stanza.channels.leave_channel_iq(channel_jid)
        return self.send_stanza(stanza_str)

    # --- Privacidad y Otros ---

    def get_last_seen(self, phone: str) -> dict:
        if not self._token: raise AuthenticationError("No autenticado")
        stanza_str = stanza.last.get_last_seen(util.build_jid(phone))
        return self.send_iq_and_wait(stanza_str)

    def block_user(self, phone: str) -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        return self.send_stanza(stanza.block.block_user(util.build_jid(phone)))

    def unblock_user(self, phone: str) -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        return self.send_stanza(stanza.block.unblock_user(util.build_jid(phone)))

    def get_block_list(self) -> list[str]:
        if not self._token: raise AuthenticationError("No autenticado")
        stanza_str = stanza.block.get_block_list()
        res = self.send_iq_and_wait(stanza_str)
        query = res.get("query", "") or res.get("query_attrs", "")
        blocked = []
        for match in re.finditer(r"<item\s+jid=['\"]([^'\"]+)['\"]", query):
            jid = match.group(1)
            blocked.append(jid.split("@")[0])
        return blocked

    def get_profile_privacy(self) -> dict:
        if not self._token: raise AuthenticationError("No autenticado")
        stanza_str = stanza.privacy.get_profile_privacy()
        res = self.send_iq_and_wait(stanza_str)
        query = res.get("query", "") or res.get("query_attrs", "")
        privacy_data = {}
        for match in re.finditer(r"<item\s+name=['\"]([^'\"]+)['\"]\s+value=['\"]([^'\"]+)['\"]", query):
            privacy_data[match.group(1)] = match.group(2)
        return privacy_data

    def set_profile_privacy(self, profile_photo: str = "everyone", last: str = "everyone", info: str = "everyone") -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        return self.send_stanza(stanza.privacy.set_profile_privacy(profile_photo, last, info))

    # --- Archivos ---

    def upload_file(self, data: bytes, file_type: FileType = FileType.FILE, progress_callback: Callable[[int, int], None] = None, file_name: str = "") -> str:
        if not self._token: raise AuthenticationError("No autenticado")
        return super().upload_file(self._token, data, file_type, progress_callback, file_name=file_name)

    def download_file(self, url: str, path: str) -> int:
        if not self._token: raise AuthenticationError("No autenticado")
        return super().download_file(self._token, url, path)

    def download_file_to_folder(self, url: str, folder: str, filename: str = "") -> tuple[int, str]:
        if not self._token: raise AuthenticationError("No autenticado")
        return super().download_file_to_folder(self._token, url, folder, filename)

    # --- Perfil ---

    def update_profile(self, alias: str = "", bio: str = "", picture_url: str = "", thumbnail_url: str = "") -> bool:
        if not self._token: raise AuthenticationError("No autenticado")
        return super().update_profile(self._token, alias, bio, picture_url, thumbnail_url)

    def upload_avatar(self, image_data: bytes, thumbnail_data: bytes = None) -> tuple[str, str]:
        if not self._token: raise AuthenticationError("No autenticado")
        return super().upload_avatar(self._token, image_data, thumbnail_data)

    def upload_avatar_from_file(self, filepath: str, thumbnail_path: str = None) -> tuple[str, str]:
        with open(filepath, "rb") as f:
            image_data = f.read()
        thumbnail_data = None
        if thumbnail_path:
            with open(thumbnail_path, "rb") as f:
                thumbnail_data = f.read()
        return self.upload_avatar(image_data, thumbnail_data)

    # --- Recepción ---

    def listen_messages(self, callback: Callable[[dict], None]) -> None:
        if not self._token: raise AuthenticationError("No autenticado")

        def _callback_wrapper(msg: dict):
            if msg.get("type") == "gc":
                msg = self.groups.process_group_message(msg)
            callback(msg)

        while True:
            try:
                super().listen_messages(self._token, _callback_wrapper)
            except TokenExpiredError:
                logger.info("Token expirado, reintentando login...")
                try:
                    self.login()
                except Exception:
                    time.sleep(30)
            except (ConnectionLostError, OSError, socket.error):
                logger.warning("Conexión perdida, reintentando en 15s...")
                time.sleep(15)
            except Exception as e:
                logger.error(f"Error inesperado en listen_messages: {e}")
                time.sleep(5)
