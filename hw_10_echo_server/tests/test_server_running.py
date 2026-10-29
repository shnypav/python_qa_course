import pytest


class TestHttpMethods:
    @pytest.mark.parametrize(
        "method", ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "TRACE"]
    )
    def test_response_echoes_request_method(self, send_request, method):
        response = send_request(method)

        assert response.status_code == 200
        assert f"Request Method: {method}" in response.text.splitlines()
        assert "Response Status: 200 OK" in response.text.splitlines()

    def test_head_returns_status_without_a_client_visible_body(self, send_request):
        response = send_request("HEAD", params={"status": 201})

        assert response.status_code == 201
        assert response.reason == "CREATED"
        assert response.content == b""


class TestStatusCodes:
    @pytest.mark.parametrize(
        "status, reason",
        [
            (200, "OK"),
            (201, "CREATED"),
            (202, "ACCEPTED"),
            (206, "PARTIAL_CONTENT"),
            (301, "MOVED_PERMANENTLY"),
            (302, "FOUND"),
            (307, "TEMPORARY_REDIRECT"),
            (308, "PERMANENT_REDIRECT"),
            (400, "BAD_REQUEST"),
            (401, "UNAUTHORIZED"),
            (403, "FORBIDDEN"),
            (404, "NOT_FOUND"),
            (405, "METHOD_NOT_ALLOWED"),
            (418, "IM_A_TEAPOT"),
            (422, "UNPROCESSABLE_ENTITY"),
            (429, "TOO_MANY_REQUESTS"),
            (500, "INTERNAL_SERVER_ERROR"),
            (502, "BAD_GATEWAY"),
            (503, "SERVICE_UNAVAILABLE"),
        ],
    )
    def test_requested_status_matches_http_status_and_echo(self, send_request, status, reason):
        response = send_request(params={"status": status})

        assert response.status_code == status
        assert response.reason == reason
        assert f"Response Status: {status} {reason}" in response.text.splitlines()
        assert response.history == []

    @pytest.mark.parametrize("status", ["", "invalid", "200.0", "-1", "0", "99", "600", "999"])
    def test_invalid_status_defaults_to_200(self, send_request, status):
        response = send_request(params={"status": status})

        assert response.status_code == 200
        assert response.reason == "OK"
        assert "Response Status: 200 OK" in response.text.splitlines()

    @pytest.mark.parametrize(
        "values, expected", [(["404", "201"], 404), (["invalid", "404"], 200)]
    )
    def test_first_repeated_status_controls_response(self, send_request, values, expected):
        response = send_request(params=[("status", value) for value in values])

        assert response.status_code == expected
        echoed = [line for line in response.text.splitlines() if line.startswith("  status: ")]
        assert echoed == [f"  status: {value}" for value in values]

    def test_status_in_another_parameter_or_header_does_not_control_response(self, send_request):
        response = send_request(
            params={"note": "status=404"}, headers={"X-Status": "status=500"}
        )

        assert response.status_code == 200
        assert "  note: status=404" in response.text.splitlines()
        assert "X-Status: status=500" in response.text.splitlines()

    @pytest.mark.parametrize("status", [204, 304])
    def test_bodyless_status_has_no_client_visible_body(self, send_request, status):
        response = send_request(params={"status": status})

        assert response.status_code == status
        assert response.content == b""


class TestQueryParameters:
    @pytest.mark.parametrize("path", ["/", "/nested/path", "/?", "/?flag&empty="])
    def test_missing_or_blank_values_omit_query_section(self, send_request, path):
        response = send_request(path=path)

        assert response.status_code == 200
        assert "Query Parameters:" not in response.text.splitlines()

    @pytest.mark.parametrize(
        "query, expected",
        [
            ("name=Ada&role=QA", ["  name: Ada", "  role: QA"]),
            ("tag=one&tag=two", ["  tag: one", "  tag: two"]),
            ("tag=one&other=value&tag=two", ["  tag: one", "  tag: two", "  other: value"]),
            ("q=hello+world", ["  q: hello world"]),
            ("q=hello%20world", ["  q: hello world"]),
            ("q=%2B%26%3D%3F%2F%25", ["  q: +&=?/%"]),
            ("first%20name=Ada%20Lovelace", ["  first name: Ada Lovelace"]),
            ("q=%D0%9F%D1%80%D0%B8%D0%B2%D0%B5%D1%82", ["  q: Привет"]),
            ("empty=&q=value&flag", ["  q: value"]),
            ("Status=404", ["  Status: 404"]),
        ],
    )
    def test_query_values_are_decoded_and_echoed_in_order(self, send_request, query, expected):
        response = send_request(path="/echo?" + query)

        assert response.status_code == 200
        lines = response.text.splitlines()
        assert lines.count("Query Parameters:") == 1
        start = lines.index("Query Parameters:") + 1
        assert lines[start : start + len(expected)] == expected
        assert [line for line in lines if line.startswith("  ")] == expected


class TestWireResponse:
    @pytest.mark.parametrize(
        "request_data, expected",
        [(b"GET /\r\n", "200 OK"), (b"GET /?status=404\r\n", "404 NOT_FOUND")],
    )
    def test_legacy_request_without_http_version_uses_fallback_parser(
        self, raw_request, request_data, expected
    ):
        response, _ = raw_request(request_data)

        status_line, body = response.decode("utf-8").split("\r\n\r\n", 1)
        assert status_line == f"HTTP/1.1 {expected}"
        assert "Request Method: GET" in body.splitlines()
        assert f"Response Status: {expected}" in body.splitlines()

    def test_small_utf8_request_body_is_echoed(self, raw_request):
        payload = "Привет 🌍".encode("utf-8")
        request = (
            b"POST / HTTP/1.1\r\nHost: localhost\r\n"
            + f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii")
            + payload
        )

        response, _ = raw_request(request)

        status_line, body = response.decode("utf-8").split("\r\n\r\n", 1)
        assert status_line == "HTTP/1.1 200 OK"
        assert "Request Method: POST" in body.splitlines()
        assert body.endswith("\n\nПривет 🌍\n")

    def test_response_echoes_actual_client_address_and_headers(self, raw_request):
        response, source = raw_request(
            b"GET /echo?status=201&tag=one&tag=two HTTP/1.1\r\n"
            b"Host: localhost\r\n"
            b"X-Trace: one:two\r\n"
            b"X-Repeat: first\r\n"
            b"X-Repeat: second\r\n\r\n"
        )

        status_line, body = response.decode("utf-8").split("\r\n\r\n", 1)
        assert status_line == "HTTP/1.1 201 CREATED"
        assert body.splitlines() == [
            "Request Method: GET",
            f"Request Source: {source}",
            "Response Status: 201 CREATED",
            "Query Parameters:",
            "  status: 201",
            "  tag: one",
            "  tag: two",
            "Host: localhost",
            "X-Trace: one:two",
            "X-Repeat: first",
            "X-Repeat: second",
            "",
        ]

    def test_server_handles_an_empty_connection_then_a_valid_request(self, raw_request, send_request):
        response, _ = raw_request(b"")

        assert response == b""
        assert send_request().status_code == 200

    def test_request_state_does_not_leak_between_connections(self, send_request):
        first = send_request(
            "POST", params={"status": 404, "previous": "secret"}, headers={"X-Previous": "secret"}
        )
        second = send_request("GET", params={"current": "value"})

        assert first.status_code == 404
        assert "X-Previous: secret" in first.text.splitlines()
        assert second.status_code == 200
        assert "Request Method: GET" in second.text.splitlines()
        assert "  current: value" in second.text.splitlines()
        assert "previous" not in second.text.lower()
        assert "secret" not in second.text

    def test_server_handles_a_sequence_of_methods_and_statuses(self, send_request):
        for sequence, (method, status) in enumerate(
            [("GET", 200), ("POST", 201), ("PATCH", 400), ("DELETE", 500), ("OPTIONS", 200)]
        ):
            response = send_request(method, params={"status": status, "seq": sequence})

            assert response.status_code == status
            assert f"Request Method: {method}" in response.text.splitlines()
            assert f"  seq: {sequence}" in response.text.splitlines()
