"""Tests para el soporte de proxy en ToDus."""

import pytest
import socks
from todus.client.base import ToDusClientBase
from todus.client import ToDusClient2


class TestProxySupport:
    def test_parse_socks5_proxy_basic(self):
        client = ToDusClientBase()
        proxy_type, host, port, username, password = client._parse_proxy("socks5://127.0.0.1:1080")
        assert proxy_type == socks.SOCKS5
        assert host == "127.0.0.1"
        assert port == 1080
        assert username is None
        assert password is None

    def test_parse_socks5_proxy_auth(self):
        client = ToDusClientBase()
        proxy_type, host, port, username, password = client._parse_proxy("socks5://user:pass@127.0.0.1:1080")
        assert proxy_type == socks.SOCKS5
        assert host == "127.0.0.1"
        assert port == 1080
        assert username == "user"
        assert password == "pass"

    def test_parse_http_proxy_default_port(self):
        client = ToDusClientBase()
        proxy_type, host, port, username, password = client._parse_proxy("http://proxy.example.com")
        assert proxy_type == socks.HTTP
        assert host == "proxy.example.com"
        assert port == 8080
        assert username is None
        assert password is None

    def test_parse_socks5h_proxy(self):
        client = ToDusClientBase()
        proxy_type, host, port, username, password = client._parse_proxy("socks5h://127.0.0.1")
        assert proxy_type == socks.SOCKS5
        assert host == "127.0.0.1"
        assert port == 1080

    def test_parse_unsupported_scheme(self):
        client = ToDusClientBase()
        with pytest.raises(ValueError):
            client._parse_proxy("ftp://127.0.0.1")

    def test_client_init_with_proxy(self):
        proxy_url = "socks5://127.0.0.1:1080"
        client = ToDusClientBase(proxy=proxy_url)
        assert client.proxy == proxy_url
        assert client.session.proxies == {
            "http": proxy_url,
            "https": proxy_url,
        }

    def test_client2_init_with_proxy(self):
        proxy_url = "http://127.0.0.1:8080"
        client = ToDusClient2(phone_number="5312345678", password="pass", proxy=proxy_url)
        assert client.proxy == proxy_url
        assert client.session.proxies == {
            "http": proxy_url,
            "https": proxy_url,
        }
