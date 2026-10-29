import argparse
from collections import deque
import importlib.util
from pathlib import Path
import queue
import re
import socket
import subprocess
import sys
import threading

import pytest
import requests


SERVER_PATH = Path(__file__).resolve().parents[1] / "server.py"
TIMEOUT = 5


def port_number(value):
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("port must be an integer") from None
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
    return port


def pytest_addoption(parser):
    parser.addoption(
        "--port",
        type=port_number,
        default=None,
        help="Test an existing localhost server instead of starting one",
    )


@pytest.fixture(scope="session")
def server_module():
    # Import this assignment by path to avoid other homeworks' server modules.
    spec = importlib.util.spec_from_file_location("echo_server_under_test", SERVER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def server_address(request):
    port = request.config.getoption("--port")
    if port is not None:
        yield "127.0.0.1", port
        return

    # The server announces its selected port after bind/listen. Drain stdout
    # continuously so a full pipe cannot stall the server during a long run.
    output = deque(maxlen=100)
    ready = queue.Queue()
    process = subprocess.Popen(
        [sys.executable, "-u", str(SERVER_PATH)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    def collect_output():
        announced = False
        for line in process.stdout:
            output.append(line)
            match = re.search(r"Waiting for a connection on \('', (\d+)\)", line)
            if match and not announced:
                ready.put(int(match.group(1)))
                announced = True
        if not announced:
            ready.put(None)

    reader = threading.Thread(target=collect_output, daemon=True)
    reader.start()
    try:
        try:
            port = ready.get(timeout=TIMEOUT)
        except queue.Empty:
            pytest.fail("Echo server did not start in time:\n" + "".join(output))
        if port is None or process.poll() is not None:
            pytest.fail("Echo server exited during startup:\n" + "".join(output))
        yield "127.0.0.1", port
    finally:
        process.terminate()
        try:
            process.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=TIMEOUT)
        reader.join(timeout=TIMEOUT)
        process.stdout.close()


@pytest.fixture(scope="session")
def server_url(server_address):
    host, port = server_address
    return f"http://{host}:{port}"


@pytest.fixture
def send_request(server_url):
    with requests.Session() as session:
        session.trust_env = False

        def send(method="GET", path="/", **kwargs):
            response = session.request(
                method,
                server_url + path,
                timeout=TIMEOUT,
                allow_redirects=False,
                **kwargs,
            )
            response.encoding = "utf-8"
            return response

        yield send


@pytest.fixture
def raw_request(server_address):
    def send(data):
        with socket.create_connection(server_address, timeout=TIMEOUT) as client:
            source = client.getsockname()
            client.sendall(data)
            client.shutdown(socket.SHUT_WR)
            chunks = []
            while chunk := client.recv(4096):
                chunks.append(chunk)
        return b"".join(chunks), source

    return send
