import logging
import threading
import time
import socket
import hashlib
from typing import Callable
from .. import util, stanza, constants
from ..errors import TokenExpiredError, ConnectionLostError
from ..types import FileType

logger = logging.getLogger("todus")


class ToDusMessageMixin:
    """Mixin que contiene la lógica de mensajería (envío y recepción) de ToDus."""

    # --- Mensajeria Privada ---

    def send_message(self, token: str, to_jid: str, body: str, reply_to: str = "") -> str:
        """Envía mensaje de texto privado. Retorna el msg_id generado."""
        mid = util.generate_token(8)
        msg = stanza.message(to_jid, body, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def edit_message(self, token: str, to_jid: str, new_body: str, original_msg_id: str, reply_to: str = "") -> str:
        """Edita un mensaje privado."""
        edit_id = util.generate_token(8)
        msg = stanza.edit_message(to_jid, new_body, original_msg_id, edit_id=edit_id, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return edit_id

    def send_file_message(self, token: str, to_jid: str, url: str, file_type: FileType, caption: str = "", file_name: str = "", file_size: int = 0, reply_to: str = "") -> str:
        mid = util.generate_token(8)
        msg = stanza.file_message(to_jid, url, int(file_type), caption, msg_id=mid, reply_to=reply_to, file_name=file_name, file_size=file_size)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_image_message(self, token: str, to_jid: str, url: str, file_name: str, file_size: int, width: int = 0, height: int = 0, thumbnail: str = "", caption: str = "", reply_to: str = "") -> str:
        """Envía mensaje privado con imagen adjunta."""
        mid = util.generate_token(8)
        msg = stanza.image_message(to_jid, url, file_name, file_size, width, height, thumbnail, caption, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_image_message_simple(self, token: str, to_jid: str, url: str, file_name: str, file_size: int, msg_id: str = "", reply_to: str = "") -> str:
        """Envía mensaje privado con imagen SIN metadata."""
        mid = msg_id or util.generate_token(8)
        msg = stanza.image_message_simple(to_jid, url, file_name, file_size, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_button_message(self, token: str, to_jid: str, text: str, buttons: list[dict], reply_to: str = "") -> str:
        """Envía mensaje con botones interactivos."""
        mid = util.generate_token(8)
        msg = stanza.button_message(to_jid, text, buttons, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_contact_message(self, token: str, to_jid: str, contact_id: str, contact_name: str, contact_phone: str, reply_to: str = "") -> str:
        mid = util.generate_token(8)
        msg = stanza.contact_message(to_jid, contact_id, contact_name, contact_phone, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_sticker_message(self, token: str, to_jid: str, sticker_id: str, sticker_name: str, sticker_pack: str, sticker_hash: str, reply_to: str = "") -> str:
        mid = util.generate_token(8)
        msg = stanza.sticker_message(to_jid, sticker_id, sticker_name, sticker_pack, sticker_hash, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_video_message(self, token: str, to_jid: str, url: str, video_id: str, file_name: str, file_size: int, duration: int, width: int, height: int, thumbnail: str, info_text: str = "", reply_to: str = "") -> str:
        mid = hashlib.md5(util.generate_token(16).encode()).hexdigest()
        msg = stanza.video_message(to_jid, url, video_id, file_name, file_size, duration, width, height, thumbnail, msg_id=mid, reply_to=reply_to, info_text=info_text)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_location_message(self, token: str, to_jid: str, lat: float, lon: float, zoom: float = 11.0, text: str = "", reply_to: str = "") -> str:
        """Envía un mensaje con ubicación adjunta."""
        mid = util.generate_token(8)
        msg = stanza.location_message(to_jid, lat, lon, zoom, text, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_event_message(self, token: str, to_jid: str, title: str, start: int, end: int, all_day: bool, ics_data: str, event_id: str = "", reply_to: str = "") -> str:
        """Envía un mensaje con evento/calendario adjunto."""
        mid = util.generate_token(8)
        msg = stanza.event_message(to_jid, event_id, title, start, end, all_day, ics_data, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_voice_message(self, token: str, to_jid: str, url: str, voice_id: str, file_size: int, duration: int, wave_sample: str = "", reply_to: str = "") -> str:
        """Envía un mensaje con nota de voz adjunta."""
        mid = util.generate_token(8)
        msg = stanza.voice_message(to_jid, url, voice_id, file_size, duration, wave_sample, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_audio_message(self, token: str, to_jid: str, url: str, audio_id: str, file_name: str, file_size: int, duration: int, reply_to: str = "") -> str:
        """Envía un mensaje con audio adjunto."""
        mid = util.generate_token(8)
        msg = stanza.audio_message(to_jid, url, audio_id, file_name, file_size, duration, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_gif_message(self, token: str, to_jid: str, url: str, gif_id: str, file_name: str, file_size: int, width: int = 0, height: int = 0, thumbnail: str = "", reply_to: str = "") -> str:
        """Envía un mensaje con GIF adjunto."""
        mid = util.generate_token(8)
        msg = stanza.gif_message(to_jid, url, gif_id, file_name, file_size, width, height, thumbnail, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def forward_message(self, token: str, to_jid: str, original_from: str, original_id: str, reply_to: str = "") -> str:
        """Reenvía un mensaje existente."""
        mid = util.generate_token(8)
        msg = stanza.forward_message(to_jid, original_from, original_id, msg_id=mid, reply_to=reply_to)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return mid

    def send_deleted_owner_message(self, token: str, to_jid: str, message_id: str) -> str:
        """Elimina un mensaje propio (deletedowner)."""
        msg = stanza.deleted_owner_message(to_jid, message_id)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return message_id

    def send_chat_state(self, token: str, to_jid: str, state: str) -> None:
        st = stanza.chat_state(to_jid, state)
        with self._xmpp_session(token) as sock:
            sock.send(st.encode())

    def delete_message(self, token: str, to_jid: str, message_id: str, msg_type: str = "c", body: str = "", media_xml: str = "") -> str:
        """Elimina un mensaje propio."""
        msg = stanza.delete_message(to_jid, message_id, msg_id=message_id, msg_type=msg_type, body=body, media_xml=media_xml)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return message_id

    def send_read_receipt(self, token: str, to_jid: str, msg_id: str, msg_type: str = "c") -> str:
        """Envía una confirmación de lectura (read receipt)."""
        rid = util.generate_token(8)
        msg = stanza.read_receipt(to_jid, msg_id, receipt_id=rid, msg_type=msg_type)
        with self._xmpp_session(token) as sock:
            sock.send(msg.encode())
        return rid

    def get_message_archive(self, token: str, since: str = "", before: str = "", limit: int = 50) -> str:
        """Consulta el archivo de mensajes de ToDus (XMPP MAM)."""
        qid = util.generate_token(8)
        mam_stanza = stanza.mam_query(qid, since=since, before=before, limit=limit)
        with self._xmpp_session(token) as sock:
            sock.send(mam_stanza.encode())
        return qid

    # --- Recepción de mensajes ---

    def listen_messages(self, token: str, callback: Callable[[dict], None], stop_event: threading.Event | None = None) -> None:
        backoff = 2.0
        while stop_event is None or not stop_event.is_set():
            try:
                with self._xmpp_session(token, reuse=False) as sock:
                    backoff = 2.0 # Reset tras conexión exitosa
                    self._listen_loop(sock, callback, stop_event=stop_event)
            except TokenExpiredError:
                raise
            except (ConnectionLostError, OSError, socket.error) as e:
                if stop_event and stop_event.is_set():
                    break
                logger.warning(f"Conexión de recepción perdida ({e}). Reintentando en {backoff:.1f}s...")
                time.sleep(backoff)
                backoff = min(backoff * 2.0, 60.0)

    def _listen_loop(self, sock, callback: Callable[[dict], None], stop_event: threading.Event | None = None) -> None:
        loop_stop = stop_event or threading.Event()
        ping_id = util.generate_token(5)
        ka = threading.Thread(
            target=self._keepalive_worker,
            args=(sock, loop_stop, ping_id),
            daemon=True,
        )
        ka.start()
        self._xml_parser.reset()

        try:
            while not loop_stop.is_set():
                try:
                    response = self._recv_all(sock)
                except OSError as e:
                    raise ConnectionLostError(e)

                if response is None:
                    raise ConnectionLostError("Servidor cerró conexión")

                if response == "":
                    continue

                stanzas = self._xml_parser.feed(response)

                for msg in stanzas:
                    # Enriquecer mensajes de grupo automáticamente (#6)
                    if msg.get("type") == "gc" and hasattr(self, "groups"):
                        try:
                            msg = self.groups.process_group_message(msg)
                        except Exception:
                            pass

                    is_content = (
                        msg.get("body")
                        or msg.get("url")
                        or msg.get("contact_id")
                        or msg.get("sticker_id")
                        or msg.get("video_url")
                        or msg.get("buttons")
                        or msg.get("location_id")
                    )
                    
                    if is_content and not msg.get("deleted"):
                        msg_id = msg.get("id", "")
                        msg_from = msg.get("from", "")
                        if msg_id and msg_from:
                            try:
                                receipt = stanza.receipt(msg_from, msg_id)
                                sock.send(receipt.encode())
                            except Exception:
                                pass
                        
                        if msg_id:
                            try:
                                ack = stanza.ack(msg_id)
                                sock.send(ack.encode())
                            except Exception:
                                pass
                    
                    if (
                        is_content
                        or msg.get("chat_state")
                        or msg.get("receipt")
                        or msg.get("deleted")
                    ):
                        callback(msg)

        finally:
            if stop_event is None:
                loop_stop.set()
            self._xml_parser.reset()

    def _keepalive_worker(self, sock, stop: threading.Event, ping_id: str) -> None:
        while not stop.is_set():
            time.sleep(constants.KEEPALIVE_INTERVAL)
            if stop.is_set():
                break
            try:
                sock.send(stanza.ping(ping_id).encode())
            except OSError:
                break
