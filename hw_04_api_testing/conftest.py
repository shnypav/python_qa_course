import logging
from datetime import datetime
from pathlib import Path
from time import monotonic

import pytest
import requests


LOGGER = logging.getLogger("hw_04_api_testing")
DEFAULT_TIMEOUT_SECONDS = 15
LOG_DIR = Path(__file__).resolve().parents[1] / "logs"


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="https://ya.ru", help="Please provide url")
    parser.addoption("--status_code", action="store", default="200", help="Please provide status code")


@pytest.fixture
def url_given(request):
    return request.config.getoption("--url")


@pytest.fixture
def status_given(request):
    return request.config.getoption("--status_code")


@pytest.fixture(scope="session", autouse=True)
def configure_file_logging():
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f"hw_04_api_testing_{datetime.now():%Y%m%d_%H%M%S_%f}.log"
    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(handler)
    LOGGER.info("Writing API test logs to %s", log_file)
    yield
    LOGGER.removeHandler(handler)
    handler.close()


@pytest.fixture(autouse=True)
def log_http_requests(monkeypatch):
    """Log every HTTP exchange and turn connection failures into useful test errors."""
    original_request = requests.sessions.Session.request
    original_json = requests.models.Response.json

    def request_with_logging(session, method, url, **kwargs):
        timeout = kwargs.setdefault("timeout", DEFAULT_TIMEOUT_SECONDS)
        LOGGER.info("HTTP request started: %s %s (timeout=%ss)", method.upper(), url, timeout)
        started_at = monotonic()
        try:
            response = original_request(session, method, url, **kwargs)
        except requests.RequestException:
            LOGGER.exception("HTTP request failed: %s %s", method.upper(), url)
            raise

        LOGGER.info(
            "HTTP response received: %s %s -> %s in %.3fs",
            method.upper(),
            url,
            response.status_code,
            monotonic() - started_at,
        )
        return response

    monkeypatch.setattr(requests.sessions.Session, "request", request_with_logging)

    def json_with_logging(response, **kwargs):
        try:
            result = original_json(response, **kwargs)
        except requests.JSONDecodeError:
            LOGGER.exception(
                "Failed to decode JSON response from %s %s (status=%s)",
                response.request.method,
                response.url,
                response.status_code,
            )
            raise
        LOGGER.debug("Decoded JSON response from %s %s", response.request.method, response.url)
        return result

    monkeypatch.setattr(requests.models.Response, "json", json_with_logging)


@pytest.fixture
def log_test_case(request):
    parameters = getattr(request.node, "callspec", None)
    LOGGER.info("Test started: %s; parameters=%s", request.node.nodeid, getattr(parameters, "params", {}))
    yield
    LOGGER.info("Test finished: %s", request.node.nodeid)
