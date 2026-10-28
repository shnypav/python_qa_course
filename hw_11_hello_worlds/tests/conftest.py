import logging
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

import pytest


LOGGER = logging.getLogger("hw_11_hello_worlds.tests")
LOG_DIR = Path(__file__).resolve().parents[1]


def pytest_configure(config):
    handler = logging.FileHandler(LOG_DIR / "test_run.log", mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    config._hello_world_log_handler = handler
    config._hello_world_log_level = LOGGER.level
    LOGGER.setLevel(logging.INFO)
    LOGGER.addHandler(handler)


def pytest_sessionstart(session):
    session._hello_world_started = perf_counter()
    LOGGER.info("Test session started")


@pytest.fixture(autouse=True)
def log_test_case(request):
    LOGGER.info("Test started: %s", request.node.nodeid)
    yield


def pytest_runtest_logreport(report):
    if report.when == "call" or report.failed or report.skipped:
        LOGGER.info(
            "Test result: %s phase=%s outcome=%s duration=%.6fs",
            report.nodeid, report.when, report.outcome, report.duration,
        )
        if report.failed:
            LOGGER.error("%s", report.longreprtext)


def pytest_sessionfinish(session, exitstatus):
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    stats = reporter.stats if reporter is not None else {}
    summary = (
        f"passed: {len(stats.get('passed', []))} | "
        f"failed: {len(stats.get('failed', []))} | "
        f"errors: {len(stats.get('error', []))} | "
        f"skipped: {len(stats.get('skipped', []))} | "
        f"exit status: {int(exitstatus)} | "
        f"duration: {perf_counter() - session._hello_world_started:.6f}s"
    )
    LOGGER.info("Test session finished: %s", summary)
    with (LOG_DIR / "test_results.log").open("a", encoding="utf-8") as file:
        file.write(f"{datetime.now(timezone.utc).isoformat()} | {summary}\n")


def pytest_unconfigure(config):
    handler = config._hello_world_log_handler
    LOGGER.removeHandler(handler)
    handler.close()
    LOGGER.setLevel(config._hello_world_log_level)
