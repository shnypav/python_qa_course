from copy import deepcopy
import socket

import pytest


class TestStatusFormatting:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (100, "100 CONTINUE"),
            ("101", "101 SWITCHING_PROTOCOLS"),
            (200, "200 OK"),
            ("201", "201 CREATED"),
            ("204", "204 NO_CONTENT"),
            ("301", "301 MOVED_PERMANENTLY"),
            ("304", "304 NOT_MODIFIED"),
            ("400", "400 BAD_REQUEST"),
            ("404", "404 NOT_FOUND"),
            ("418", "418 IM_A_TEAPOT"),
            ("500", "500 INTERNAL_SERVER_ERROR"),
            ("511", "511 NETWORK_AUTHENTICATION_REQUIRED"),
            (" 201 ", "201 CREATED"),
            ("+201", "201 CREATED"),
            ("0201", "201 CREATED"),
        ],
    )
    def test_known_status_returns_numeric_code_and_enum_name(self, server_module, value, expected):
        assert server_module.get_status(value) == expected

    @pytest.mark.parametrize(
        "value", ["", " ", "invalid", "20x", "200.0", "0xC8", "99", "600", "999", "-1", 0, 999]
    )
    def test_invalid_status_returns_200_ok(self, server_module, value):
        assert server_module.get_status(value) == "200 OK"


class TestResponseFormatting:
    def test_response_has_a_status_line_separator_and_exact_metadata(self, server_module):
        response = server_module.create_response(
            "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n", "GET", "201", ("127.0.0.1", 12345)
        )

        assert response == (
            "HTTP/1.1 201 CREATED\r\n\r\n"
            "Request Method: GET\n"
            "Request Source: ('127.0.0.1', 12345)\n"
            "Response Status: 201 CREATED\n"
            "Host: localhost\n\n"
        )

    def test_invalid_status_is_consistent_in_status_line_and_body(self, server_module):
        response = server_module.create_response("GET / HTTP/1.1", "GET", "invalid", ("127.0.0.1", 1))

        status_line, body = response.split("\r\n\r\n", 1)
        assert status_line == "HTTP/1.1 200 OK"
        assert "Response Status: 200 OK" in body.splitlines()

    @pytest.mark.parametrize("query_params", [None, {}])
    def test_absent_query_parameters_omit_query_section(self, server_module, query_params):
        response = server_module.create_response(
            "GET / HTTP/1.1", "GET", "200", ("127.0.0.1", 1), query_params
        )

        assert "Query Parameters:" not in response

    def test_query_parameters_preserve_order_duplicates_and_unicode(self, server_module):
        query_params = {"tag": ["one", "two"], "name": ["Привет 🌍"], "empty": [""]}
        original = deepcopy(query_params)

        response = server_module.create_response(
            "GET / HTTP/1.1", "GET", "200", ("127.0.0.1", 1), query_params
        )

        assert response.split("Query Parameters:\n", 1)[1].splitlines() == [
            "  tag: one", "  tag: two", "  name: Привет 🌍", "  empty: "
        ]
        assert query_params == original

    def test_echo_preserves_repeated_headers_colons_and_body_lines(self, server_module):
        response = server_module.create_response(
            "POST / HTTP/1.1\r\nX-Repeat: one\r\nX-Repeat: two:three\r\n\r\npayload\nПривет",
            "POST", "200", ("127.0.0.1", 1),
        )

        body = response.split("\r\n\r\n", 1)[1]
        assert body.splitlines()[3:] == [
            "X-Repeat: one", "X-Repeat: two:three", "", "payload", "Привет"
        ]
        assert "POST / HTTP/1.1" not in body


def test_open_port_is_a_valid_tcp_port(server_module):
    port = server_module.get_open_port()

    assert isinstance(port, int)
    assert 1 <= port <= 65535
    # The helper must release its socket before returning the port.
    with socket.socket() as listener:
        listener.bind(("", port))
