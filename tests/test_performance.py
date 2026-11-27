"""Pruebas de rendimiento, pipelining XMPP y concurrencia para v1.6.2."""

import re
import socket
import threading
import time
from unittest.mock import MagicMock

import pytest

from todus import ToDusClient2, constants
from todus.client.base import ToDusClientBase
from todus.client.file import ToDusFileMixin
from todus.errors import TokenExpiredError
from todus.types import FileType


class _DummyUploadClient(ToDusFileMixin, ToDusClientBase):
    pass


def test_http_pool_and_rate_limit_configurable():
    client = _DummyUploadClient(pool_size=24, rate_limit=12.0)
    https_adapter = client.session.get_adapter("https://s3.todus.cu")
    assert https_adapter._pool_connections == 24
    assert https_adapter._pool_maxsize == 24
    assert client.rate_limiter.min_interval == pytest.approx(1.0 / 12.0)


def test_tcp_nodelay_enabled_on_connect_xmpp(monkeypatch):
    client = _DummyUploadClient()
    sock_opts = []

    class FakeRawSock:
        def settimeout(self, t):
            pass

        def setsockopt(self, level, optname, val):
            sock_opts.append((level, optname, val))

        def connect(self, addr):
            pass

    class FakeWrapped:
        def send(self, data):
            pass

    monkeypatch.setattr(socket, "socket", lambda *args, **kwargs: FakeRawSock())

    class FakeCtx:
        verify_mode = None
        check_hostname = True

        def wrap_socket(self, sock, server_hostname=None):
            return FakeWrapped()

    monkeypatch.setattr("ssl.create_default_context", lambda: FakeCtx())
    client._connect_xmpp()

    assert (socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) in sock_opts
    assert (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) in sock_opts


def test_persistent_xmpp_session_serializes_threads():
    client = _DummyUploadClient(rate_limit=0.0)
    active = 0
    max_active = 0
    guard = threading.Lock()

    class FakeSock:
        def getpeername(self):
            return ("127.0.0.1", 1756)

    client._persistent_sock = FakeSock()
    client._persistent_token = "tok1"

    def worker():
        nonlocal active, max_active
        with client._xmpp_session("tok1"):
            with guard:
                active += 1
                max_active = max(max_active, active)
            time.sleep(0.03)
            with guard:
                active -= 1

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert max_active == 1


def test_reserve_upload_urls_pipelined_batch_and_fragmented_responses():
    client = _DummyUploadClient(rate_limit=0.0)
    sent_payloads = []
    recv_queue = []

    class FakeSock:
        def getpeername(self):
            return ("127.0.0.1", 1756)

        def sendall(self, data: bytes):
            txt = data.decode("utf-8")
            sent_payloads.append(txt)
            iq_ids = re.findall(r"i='([^']+)'", txt)
            # Responder fuera de orden y fragmentado en dos bloques TCP
            full_reply = "".join(
                f"<iq i='{iq_id}' t='result' put='https://s3.todus.cu/file/p/{iq_id}?sig=1&amp;x=2' get='https://s3.todus.cu/file/p/{iq_id}'></iq>"
                for iq_id in reversed(iq_ids)
            )
            mid = len(full_reply) // 2
            recv_queue.append(full_reply[:mid])
            recv_queue.append(full_reply[mid:])

    client._persistent_sock = FakeSock()
    client._persistent_token = "tok1"
    client._recv_all = lambda sock: recv_queue.pop(0) if recv_queue else ""

    items = [
        (1024, FileType.FILE, "part.001"),
        (2048, FileType.FILE, "part.002"),
        (4096, FileType.FILE, "part.003"),
    ]
    res = client.reserve_upload_urls("tok1", items)
    assert len(sent_payloads) == 1
    assert len(res) == 3
    for put_url, get_url in res:
        assert put_url.startswith("https://s3.todus.cu/file/p/")
        assert "&x=2" in put_url
        assert get_url.startswith("https://s3.todus.cu/file/p/")


def test_reserve_upload_urls_raises_on_not_authorized():
    client = _DummyUploadClient(rate_limit=0.0)

    class FakeSock:
        def getpeername(self):
            return ("127.0.0.1", 1756)

        def sendall(self, data: bytes):
            pass

    client._persistent_sock = FakeSock()
    client._persistent_token = "tok_bad"
    client._recv_all = lambda sock: "<not-authorized/>"

    with pytest.raises(TokenExpiredError):
        client.reserve_upload_urls("tok_bad", [(100, FileType.FILE, "a.bin")])


def test_client2_use_cache_false_and_upload_file_path(tmp_path):
    c = ToDusClient2("5351234567", password="secret", use_cache=False, rate_limit=0.0)
    assert c.cache is None
    assert c.queue is None

    fpath = tmp_path / "sample.bin"
    fpath.write_bytes(b"X" * (constants.UPLOAD_CHUNK_SIZE + 123))

    c.reserve_upload_url = MagicMock(return_value=("https://s3.todus.cu/file/up", "https://s3.todus.cu/file/get"))
    captured = {}

    def fake_put(url, data=None, headers=None, timeout=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["len"] = len(data)
        captured["chunks"] = [chunk for chunk in data]
        return MagicMock(status_code=200, raise_for_status=lambda: None)

    c.session.put = fake_put
    seen_progress = []
    out_url = c.upload_file_path(
        "tok",
        str(fpath),
        file_type=FileType.FILE,
        progress_callback=lambda s, t: seen_progress.append((s, t)),
    )

    assert out_url == "https://s3.todus.cu/file/get"
    assert "Authorization" not in captured["headers"]
    assert captured["len"] == constants.UPLOAD_CHUNK_SIZE + 123
    assert len(captured["chunks"]) == 2
    assert seen_progress[-1] == (constants.UPLOAD_CHUNK_SIZE + 123, constants.UPLOAD_CHUNK_SIZE + 123)
