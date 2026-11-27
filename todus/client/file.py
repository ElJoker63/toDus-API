import logging
import os
import re
import time
from typing import Callable, Iterable
import requests
from .. import constants, parser, stanza, util
from ..types import FileType
from ..errors import ConnectionLostError, TokenExpiredError, UploadError

logger = logging.getLogger("todus")


class _ProgressReader:
    def __init__(self, data: bytes, progress_callback: Callable[[int, int], None]) -> None:
        self.data = data
        self.total = len(data)
        self.offset = 0
        self.progress_callback = progress_callback

    def read(self, size: int = -1) -> bytes:
        if self.offset >= self.total:
            return b""

        if size is None or size < 0:
            chunk = self.data[self.offset:]
            self.offset = self.total
        else:
            end = min(self.offset + size, self.total)
            chunk = self.data[self.offset:end]
            self.offset = end

        if chunk and self.progress_callback:
            try:
                self.progress_callback(self.offset, self.total)
            except Exception:
                pass

        return chunk


class _FileStreamReader:
    """Lector por streaming desde disco con bloques grandes para evitar carga completa en RAM."""

    def __init__(
        self,
        filepath: str,
        progress_callback: Callable[[int, int], None] | None = None,
        chunk_size: int = constants.UPLOAD_CHUNK_SIZE,
    ) -> None:
        self.filepath = filepath
        self.total = os.path.getsize(filepath)
        self.sent = 0
        self.progress_callback = progress_callback
        self.chunk_size = max(64 * 1024, int(chunk_size or constants.UPLOAD_CHUNK_SIZE))
        self._fp = open(filepath, "rb")

    def __iter__(self):
        while True:
            chunk = self._fp.read(self.chunk_size)
            if not chunk:
                break
            self.sent += len(chunk)
            if self.progress_callback:
                try:
                    self.progress_callback(self.sent, self.total)
                except Exception:
                    pass
            yield chunk

    def __len__(self) -> int:
        return self.total

    def close(self) -> None:
        try:
            self._fp.close()
        except Exception:
            pass


def _extract_iq_upload_urls(stanza_str: str) -> tuple[str, str]:
    put_match = re.search(r"\bput=['\"]([^'\"]+)['\"]", stanza_str)
    get_match = re.search(r"\bget=['\"]([^'\"]+)['\"]", stanza_str)
    if put_match and get_match:
        return (
            put_match.group(1).replace("&amp;", "&"),
            get_match.group(1).replace("&amp;", "&"),
        )
    return "", ""


class ToDusFileMixin:
    """Mixin que contiene los métodos de subida y descarga de archivos de ToDus."""

    # --- Archivos ---

    def reserve_upload_url(self, token: str, size: int, file_type: FileType, file_name: str = "") -> tuple[str, str]:
        sid = util.generate_token(5)
        up_url = down_url = ""

        # Sanitizar nombre del archivo
        sanitized_name = util.sanitize_filename(file_name, int(file_type))
        iq_tag_re = re.compile(rf"i=['\"]{re.escape(sid)}-3['\"]")

        with self._xmpp_session(token) as sock:
            sock.sendall(stanza.upload_query(sid, size, int(file_type), file_name=sanitized_name).encode())
            buf = ""
            for _ in range(15):
                response = self._recv_all(sock)
                if response is None:
                    raise ConnectionLostError("Conexión perdida reservando URL de subida")
                if response == "":
                    continue
                buf += response
                if "<not-authorized/>" in buf:
                    raise TokenExpiredError()
                if iq_tag_re.search(buf):
                    up_url, down_url = _extract_iq_upload_urls(buf)
                    if up_url or "<error" in buf:
                        break

        if not up_url:
            raise UploadError("No se pudo reservar URL de subida (timeout o error de respuesta)")

        return up_url, down_url

    def reserve_upload_urls(
        self,
        token: str,
        items: Iterable[tuple[int, FileType | int, str]],
        persistent: bool = False,
        batch_size: int = 20,
    ) -> list[tuple[str, str]]:
        """
        Reserva múltiples URLs de subida por pipelining en una sola sesión XMPP,
        eliminando esperas de RateLimiter y latencias RTT entre chunks.

        items: secuencia de (size, file_type, file_name).
        Retorna una lista [(put_url, get_url), ...] en el mismo orden.
        """
        item_list = list(items)
        if not item_list:
            return []

        results: list[tuple[str, str]] = []
        eff_batch = max(1, int(batch_size or 20))

        for start in range(0, len(item_list), eff_batch):
            chunk = item_list[start : start + eff_batch]
            sid_to_idx: dict[str, int] = {}
            payload_parts: list[str] = []
            batch_out: list[tuple[str, str] | None] = [None] * len(chunk)

            for idx, (sz, ftype, fname) in enumerate(chunk):
                sid = util.generate_token(5)
                while sid in sid_to_idx:
                    sid = util.generate_token(5)
                iq_id = f"{sid}-3"
                sid_to_idx[iq_id] = idx
                sanitized_name = util.sanitize_filename(fname, int(ftype))
                payload_parts.append(
                    stanza.upload_query(
                        sid,
                        int(sz),
                        int(ftype),
                        persistent=persistent,
                        file_name=sanitized_name,
                    )
                )

            pending = set(sid_to_idx.keys())
            with self._xmpp_session(token) as sock:
                sock.sendall("".join(payload_parts).encode())
                buf = ""
                deadline = time.time() + max(constants.DEFAULT_TIMEOUT, len(chunk) * 2.0)
                while pending and time.time() < deadline:
                    response = self._recv_all(sock)
                    if response is None:
                        raise ConnectionLostError("Conexión perdida reservando URLs de subida en lote")
                    if response == "":
                        continue
                    buf += response
                    if "<not-authorized/>" in buf:
                        raise TokenExpiredError()

                    parsed = parser.extract_all_stanzas(buf)
                    for iq_str in parsed.get("iqs", []):
                        m_id = re.search(r"\bi=['\"]([^'\"]+)['\"]", iq_str)
                        if not m_id:
                            continue
                        iq_id = m_id.group(1)
                        if iq_id not in pending:
                            continue
                        if "<error" in iq_str:
                            raise UploadError(f"Error reservando URL de subida ({iq_id})")
                        up_url, down_url = _extract_iq_upload_urls(iq_str)
                        if up_url and down_url:
                            batch_out[sid_to_idx[iq_id]] = (up_url, down_url)
                            pending.discard(iq_id)

                    last_close = buf.rfind("</iq>")
                    if last_close != -1:
                        buf = buf[last_close + 5 :]

            if pending or any(entry is None for entry in batch_out):
                raise UploadError(
                    f"No se pudieron reservar todas las URLs en lote (faltaron {len(pending)})"
                )
            results.extend(entry for entry in batch_out if entry is not None)

        return results

    def get_real_download_url(self, token: str, url: str) -> str:
        sid = util.generate_token(5)
        real_url = ""

        with self._xmpp_session(token) as sock:
            sock.sendall(stanza.download_query(sid, url).encode())
            for _ in range(15):
                response = self._recv_all(sock)
                if response is None:
                    raise ConnectionLostError("Conexión perdida resolviendo URL de descarga")
                if response == "":
                    continue
                if f"i='{sid}-2'" in response or f'i="{sid}-2"' in response:
                    match = re.search(r"du=['\"]([^'\"]+)['\"]", response)
                    if match:
                        real_url = match.group(1).replace("&amp;", "&")
                        break
                if "<not-authorized/>" in response:
                    raise TokenExpiredError()

        return real_url

    def upload_file(
        self,
        token: str,
        data: bytes,
        file_type: FileType = FileType.FILE,
        progress_callback: Callable[[int, int], None] = None,
        file_name: str = "",
        include_auth_header: bool = True,
    ) -> str:
        up_url, down_url = self.reserve_upload_url(token, len(data), file_type, file_name=file_name)
        upload_data = _ProgressReader(data, progress_callback) if progress_callback else data

        headers = {
            "Content-Length": str(len(data)),
            "Content-Type": "application/octet-stream" if file_type != FileType.PICTURE else "image/jpeg",
            "User-Agent": f"ToDus {self.version_name} HTTP-Upload",
        }
        if include_auth_header:
            headers["Authorization"] = f"Bearer {token}"

        resp = self.session.put(
            up_url,
            data=upload_data,
            headers=headers,
            timeout=120,
        )
        resp.raise_for_status()

        if progress_callback:
            try:
                progress_callback(len(data), len(data))
            except Exception:
                pass

        return down_url

    def upload_to_presigned_url(
        self,
        put_url: str,
        filepath: str,
        content_type: str = "application/octet-stream",
        progress_callback: Callable[[int, int], None] | None = None,
        chunk_size: int = constants.UPLOAD_CHUNK_SIZE,
        timeout: tuple[int, int] | int = (20, 3600),
        auth_token: str | None = None,
    ) -> None:
        """Sube un archivo en streaming HTTP PUT reutilizando el pool keep-alive de self.session."""
        total_size = os.path.getsize(filepath)
        headers = {
            "Content-Length": str(total_size),
            "Content-Type": content_type or "application/octet-stream",
            "User-Agent": f"ToDus {self.version_name} HTTP-Upload",
        }
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        reader = _FileStreamReader(filepath, progress_callback=progress_callback, chunk_size=chunk_size)
        try:
            resp = self.session.put(
                put_url,
                data=reader,
                headers=headers,
                timeout=timeout,
            )
            resp.raise_for_status()
        finally:
            reader.close()

    def upload_file_path(
        self,
        token: str,
        filepath: str,
        file_type: FileType = FileType.FILE,
        progress_callback: Callable[[int, int], None] | None = None,
        file_name: str = "",
        include_auth_header: bool = False,
        chunk_size: int = constants.UPLOAD_CHUNK_SIZE,
    ) -> str:
        """Reserva URL y sube un archivo desde disco por streaming sin cargarlo completo en RAM."""
        eff_name = file_name or os.path.basename(filepath)
        total_size = os.path.getsize(filepath)
        up_url, down_url = self.reserve_upload_url(token, total_size, file_type, file_name=eff_name)
        ctype = "application/octet-stream" if file_type != FileType.PICTURE else "image/jpeg"
        self.upload_to_presigned_url(
            up_url,
            filepath,
            content_type=ctype,
            progress_callback=progress_callback,
            chunk_size=chunk_size,
            auth_token=token if include_auth_header else None,
        )
        return down_url

    def download_file(self, token: str, url: str, path: str, max_retries: int = 10) -> int:
        real_url = self.get_real_download_url(token, url)
        if not real_url:
            raise UploadError("No se pudo obtener URL real de descarga")

        headers = {
            "User-Agent": "ToDus " + self.version_name + " HTTP-Download",
            "Authorization": "Bearer " + token,
        }
        temp_path = path + ".part"
        size = -1
        retries = max_retries
        success = False

        with open(temp_path, "ab", buffering=constants.DOWNLOAD_CHUNK_SIZE) as f:
            while retries > 0:
                pos = f.tell()
                if size != -1 and pos >= size:
                    success = True
                    break

                if pos > 0:
                    headers["Range"] = f"bytes={pos}-"

                try:
                    with self.session.get(real_url, headers=headers, stream=True, timeout=60) as resp:
                        if resp.status_code == 416:  # Range not satisfiable
                            success = True
                            break
                        resp.raise_for_status()

                        content_len = int(resp.headers.get("Content-Length", 0))
                        if size == -1:
                            size = pos + content_len

                        for chunk in resp.iter_content(chunk_size=constants.DOWNLOAD_CHUNK_SIZE):
                            if chunk:
                                f.write(chunk)
                    success = True
                    break  # Éxito
                except Exception as e:
                    retries -= 1
                    logger.warning(f"Error en descarga (reintento {max_retries - retries}/{max_retries}): {e}")
                    if retries <= 0:
                        raise UploadError(f"Descarga fallida tras {max_retries} reintentos: {e}")
                    time.sleep(3)

        if not success and (size != -1 and os.path.getsize(temp_path) < size):
            raise UploadError("La descarga no se completó correctamente")

        if os.path.exists(path):
            os.remove(path)
        os.rename(temp_path, path)
        return os.path.getsize(path)

    def download_file_to_folder(self, token: str, url: str, folder: str, filename: str = "") -> tuple[int, str]:
        os.makedirs(folder, exist_ok=True)
        if not filename:
            filename = os.path.basename(url.split("?")[0]) or "download"
        
        final_path = os.path.join(folder, filename)
        size = self.download_file(token, url, final_path)
        return size, final_path
