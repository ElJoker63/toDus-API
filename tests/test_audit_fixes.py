"""Pruebas unitarias para validar la corrección de los 21 puntos auditados."""

import pytest
import os
import time
import threading
from todus.events import EventBus, PhoneFilter, GroupFilter, TextFilter, RegexFilter, CommandFilter
from todus.cache import SQLiteCache, MessageQueue, MessageStatus
from todus.rate_limiter import RateLimiter
from todus.client.channels import ToDusChannelMixin
from todus.client.base import ToDusClientBase
from todus import util, stanza, IncrementalParser, ToDusClient2
from todus.errors import UploadError


def test_issue_1_phone_filter_with_jid():
    filter_obj = PhoneFilter("5312345678")
    
    # Mensaje con JID completo
    event1 = {"from": "5312345678@im.todus.cu/resource"}
    assert filter_obj.filter(event1) is True

    # Mensaje con prefijo '+'
    event2 = {"from": "+5312345678@im.todus.cu"}
    assert filter_obj.filter(event2) is True

    # Remitente distinto
    event3 = {"from": "5399999999@im.todus.cu"}
    assert filter_obj.filter(event3) is False


def test_issue_2_download_file_max_retries(tmp_path):
    from todus.client.file import ToDusFileMixin
    class MockClient(ToDusFileMixin, ToDusClientBase):
        def get_real_download_url(self, token, url):
            return "https://invalid.todus.cu/nonexistent"

    client = MockClient()
    file_path = os.path.join(tmp_path, "test.bin")
    
    # Debe fallar tras agotar reintentos sin bucle infinito
    with pytest.raises(UploadError):
        client.download_file("mock_token", "https://todus.cu/file", file_path, max_retries=2)


def test_issue_3_and_13_auth_protobuf_and_token_cleanup():
    class MockResponse:
        status_code = 200
        text = "\r\n\t eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjUzMTIzNDU2NzgifQ.token_sig \n\x0b"
        content = b""
        def raise_for_status(self):
            pass

    client = ToDusClient2("5312345678", "password123")
    client.session.post = lambda url, data, headers, timeout: MockResponse()
    
    token = client.login()
    assert token == "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjUzMTIzNDU2NzgifQ.token_sig"
    assert "\r" not in token and "\n" not in token and "\t" not in token


def test_issue_7_message_queue_retry_worker(tmp_path):
    db_file = os.path.join(tmp_path, "queue_test.db")
    db = SQLiteCache(db_path=db_file)
    
    sent_messages = []

    class DummyClient:
        logged = True
        def send_message(self, target, body):
            sent_messages.append((target, body))
            return "mid123"

    client = DummyClient()
    queue = MessageQueue(db=db, client=client, auto_start_worker=False)
    
    queue.enqueue("msg001", "5312345678", "Hola mundo retry")
    
    # Iniciar trabajador de reintento
    queue.start_retry_worker()
    time.sleep(2)
    queue.stop_retry_worker()

    assert len(sent_messages) >= 1
    assert sent_messages[0] == ("5312345678", "Hola mundo retry")
    db.close()


def test_issue_8_is_group_target_detection():
    client = ToDusClient2("5312345678")
    
    # Teléfono estándar cubano (10 dígitos con 53)
    assert client._is_group_target("53512345678") is False
    
    # Teléfono cubano con '+'
    assert client._is_group_target("+53512345678") is False

    # Teléfono cubano de 8 dígitos
    assert client._is_group_target("51234567") is False

    # JID de grupo MUC Light
    assert client._is_group_target("12345@muclight.im.todus.cu") is True

    # ID de grupo alfanumérico
    assert client._is_group_target("group-abcd-1234") is True


def test_issue_9_channel_mixin_not_inheriting_base():
    assert not issubclass(ToDusChannelMixin, ToDusClientBase)


def test_issue_10_xml_escaping_in_stanzas():
    msg = stanza.contact_message(
        "5312345678@im.todus.cu",
        "c1",
        "Juan <Testing>",
        "5300000000&extra='val'",
    )
    assert "&amp;" in msg
    assert "&apos;" in msg
    assert "5300000000&extra='val'" not in msg


def test_issue_11_dynamic_blurhash():
    hash1 = util.generate_blurhash(100, 100)
    hash2 = util.generate_blurhash(200, 400)
    assert hash1 != "LFE_@w00ay00ay00ay00ay00ay00ay" or len(hash1) > 0
    assert hash1 != hash2


def test_issue_12_sasl_auth_return_type():
    res = stanza.sasl_auth(b"test_auth")
    assert isinstance(res, str)
    assert "<ah xmlns='ah:ns' e='PLAIN'>test_auth</ah>" in res


def test_issue_14_rate_limiter():
    limiter = RateLimiter(max_per_second=10.0)
    start = time.time()
    for _ in range(3):
        limiter.wait()
    elapsed = time.time() - start
    assert elapsed >= 0.15


def test_issue_16_incremental_parser_duplicates():
    parser = IncrementalParser()
    chunk = (
        "<m o='531@im.todus.cu' i='1'><b>Hola</b></m>"
        "<m o='531@im.todus.cu' i='1'><b>Hola</b></m>"
    )
    stanzas = parser.feed(chunk)
    assert len(stanzas) == 2
    assert stanzas[0]["id"] == "1"
    assert stanzas[1]["id"] == "1"
