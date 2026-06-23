import os
import re
import time
import logging
from typing import Callable
import requests
from .. import util, stanza
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


class ToDusFileMixin:
    """Mixin que contiene los métodos de subida y descarga de archivos de ToDus."""

    # --- Archivos ---

    def reserve_upload_url(self, token: str, size: int, file_type: FileType, file_name: str = "") -> tuple[str, str]:
        sid = util.generate_token(5)
        up_url = down_url = ""

        # Sanitizar nombre del archivo
        sanitized_name = util.sanitize_filename(file_name, int(file_type))

        with self._xmpp_session(token) as sock:
            sock.send(stanza.upload_query(sid, size, int(file_type), file_name=sanitized_name).encode())
            for _ in range(15):
                response = self._recv_all(sock)
                if response is None:
                    raise ConnectionLostError("Conexión perdida reservando URL de subida")
                if response == "":
                    continue
                if f"i='{sid}-3'" in response and "put='" in response:
                    put_match = re.search(r"put=['\"]([^'\"]+)['\"]", response)
                    get_match = re.search(r"get=['\"]([^'\"]+)['\"]", response)
                    if put_match and get_match:
                        up_url = put_match.group(1).replace("&amp;", "&")
                        down_url = get_match.group(1).replace("&amp;", "&")
                    break
                if "<not-authorized/>" in response:
                    raise TokenExpiredError()
        
        if not up_url:
            raise UploadError("No se pudo reservar URL de subida (timeout o error de respuesta)")

        return up_url, down_url

    def get_real_download_url(self, token: str, url: str) -> str:
        sid = util.generate_token(5)
        real_url = ""

        with self._xmpp_session(token) as sock:
            sock.send(stanza.download_query(sid, url).encode())
            for _ in range(15):
                response = self._recv_all(sock)
                if response is None:
                    raise ConnectionLostError("Conexión perdida resolviendo URL de descarga")
                if response == "":
                    continue
                if f"i='{sid}-2'" in response and "du='" in response:
                    match = re.search(r"du=['\"]([^'\"]+)['\"]", response)
                    if match:
                        real_url = match.group(1).replace("&amp;", "&")
                    break
                if "<not-authorized/>" in response:
                    raise TokenExpiredError()

        return real_url

    def upload_file(self, token: str, data: bytes, file_type: FileType = FileType.FILE, progress_callback: Callable[[int, int], None] = None, file_name: str = "") -> str:
        up_url, down_url = self.reserve_upload_url(token, len(data), file_type, file_name=file_name)
        upload_data = _ProgressReader(data, progress_callback) if progress_callback else data
        
        headers = {
            "Content-Length": str(len(data)),
            "Content-Type": "application/octet-stream" if file_type != FileType.PICTURE else "image/jpeg",
            "User-Agent": f"ToDus {self.version_name} HTTP-Upload"
        }
        
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

    def download_file(self, token: str, url: str, path: str) -> int:
        real_url = self.get_real_download_url(token, url)
        if not real_url:
            raise UploadError("No se pudo obtener URL real de descarga")
            
        headers = {
            "User-Agent": "ToDus " + self.version_name + " HTTP-Download",
            "Authorization": "Bearer " + token,
        }
        temp_path = path + ".part"
        size = -1
        retries = 5
        
        with open(temp_path, "ab") as f:
            while retries > 0:
                pos = f.tell()
                if size != -1 and pos >= size:
                    break
                    
                if pos > 0:
                    headers["Range"] = f"bytes={pos}-"
                    
                try:
                    with self.session.get(real_url, headers=headers, stream=True, timeout=60) as resp:
                        if resp.status_code == 416: # Range not satisfiable
                            break
                        resp.raise_for_status()
                        
                        content_len = int(resp.headers.get("Content-Length", 0))
                        if size == -1:
                            size = pos + content_len
                            
                        for chunk in resp.iter_content(chunk_size=16384):
                            if chunk:
                                f.write(chunk)
                    break # Éxito
                except Exception as e:
                    logger.warning(f"Error en descarga (reintentando): {e}")
                    retries -= 1
                    time.sleep(3)
        
        if os.path.exists(path):
            os.remove(path)
        os.rename(temp_path, path)
        return os.path.getsize(path)

    def download_file_to_folder(self, token: str, url: str, folder: str, filename: str = "") -> tuple[int, str]:
        if not filename:
            filename = os.path.basename(url.split("?")[0]) or "download"
        
        final_path = os.path.join(folder, filename)
        size = self.download_file(token, url, final_path)
        return size, final_path
