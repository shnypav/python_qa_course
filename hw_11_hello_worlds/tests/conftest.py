import logging
from collections import Counter
from datetime import datetime
from pathlib import Path

import pytest


LOGGER = logging.getLogger("hw_11_hello_worlds")
LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
RESULTS = Counter()


@pytest.fixture(scope="session", autouse=True)
def configure_file_logging():
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f"hw_11_hello_worlds_{datetime.now():%Y%m%d_%H%M%S_%f}.log"
    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(handler)
    LOGGER.info("Writing hello world test logs to %s", log_file)
    yield
    summary = ", ".join(f"{result}={count}" for result, count in sorted(RESULTS.items()))
    LOGGER.info("Test run summary: %s", summary or "no results")
    LOGGER.removeHandler(handler)
    handler.close()


@pytest.fixture(autouse=True)
def log_test_case(request):
    parameters = getattr(request.node, "callspec", None)
    LOGGER.info("Test started: %s; parameters=%s", request.node.nodeid, getattr(parameters, "params", {}))
    yield
    LOGGER.info("Test finished: %s", request.node.nodeid)


def pytest_runtest_logreport(report):
    """Log each test result, plus setup or teardown phases that did not pass."""
    if report.when != "call" and report.passed:
        return

    result = report.outcome if report.when == "call" else f"{report.outcome} during {report.when}"
    RESULTS[result] += 1
    if report.failed:
        LOGGER.error(
            "Test result: %s -> %s in %.3fs\n%s",
            report.nodeid,
            result.upper(),
            report.duration,
            report.longreprtext,
        )
    else:
        LOGGER.info("Test result: %s -> %s in %.3fs", report.nodeid, result.upper(), report.duration)
