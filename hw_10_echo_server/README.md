# Echo server tests

From the repository root, using Python with the root requirements installed:

```bash
python -m pytest hw_10_echo_server/tests -v
```

Pytest starts a real server on an automatically selected port, waits for its
listening announcement, and stops it at teardown, including when a test fails.
No manual startup, fixed port, process scanning, or external service is needed.
Every HTTP/socket operation and startup/shutdown wait has a timeout. Requests
bypass environment proxies and do not follow redirects, so assertions inspect
the echo server's response directly. Startup and connection failures fail tests.

To test a server you started yourself, pass its port. Pytest leaves that process
running:

```bash
python -m pytest hw_10_echo_server/tests --port=8080 -v
```

The Python and shell runners also accept pytest arguments and return its exit
status. They work from any current directory:

```bash
python hw_10_echo_server/run_server_and_tests.py -q
bash hw_10_echo_server/run_tests.sh -q
bash hw_10_echo_server/run_server_and_tests.sh -q
```

The suite covers:

- Unit tests for status formatting, invalid status fallback, response framing,
  metadata, repeated headers, body echoing, query order, Unicode, and input
  preservation. Run only these with
  `python -m pytest hw_10_echo_server/tests/test_server.py`.
- HTTP tests for methods, statuses, redirects, invalid and repeated status
  parameters, query decoding, repeated values, blank values, and request isolation.
- Socket tests for exact wire output, the actual client address, connection
  closure, small UTF-8 request bodies, the legacy request parser, and recovery
  after a client disconnects without sending a request.
- CLI tests for help output and invalid argument errors without starting a server.

Assertions follow this assignment's existing contract: status labels use
`HTTPStatus` enum names such as `NOT_FOUND`; the first nonblank `status` value
controls the response; unknown statuses default to 200; blank query values are
omitted. HEAD, 204, and 304 tests check the body exposed by an HTTP client.

The server currently reads one chunk of at most 1024 bytes per connection. This
suite covers small, complete requests; fragmented/large requests, malformed
input recovery, concurrent clients, and HTTP-compliant suppression of response
bodies on the wire need server changes and are outside this test-only update.
