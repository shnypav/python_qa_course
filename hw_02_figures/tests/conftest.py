import logging
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

import pytest

from ..src.Circle import Circle
from ..src.Triangle import Triangle
from ..src.Rectangle import Rectangle
from ..src.Square import Square


TEST_RUN_LOG = Path(__file__).resolve().parents[1] / "test_run.log"
LOGGER = logging.getLogger("hw_02_figures.tests")
PROJECT_LOGGER = logging.getLogger("hw_02_figures")
LOG_DIR = Path(__file__).resolve().parents[2] / "logs"


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Store a monotonic start time for the complete pytest session."""
    session._figures_test_start_time = perf_counter()


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Append the test outcome summary and elapsed time after every run."""
    terminal_reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    stats = terminal_reporter.stats if terminal_reporter is not None else {}
    elapsed_seconds = perf_counter() - session._figures_test_start_time

    TEST_RUN_LOG.parent.mkdir(parents=True, exist_ok=True)
    with TEST_RUN_LOG.open("a", encoding="utf-8") as log_file:
        log_file.write(
            f"{datetime.now(timezone.utc).isoformat()} | "
            f"passed: {len(stats.get('passed', []))} | "
            f"failed: {len(stats.get('failed', []))} | "
            f"skipped: {len(stats.get('skipped', []))} | "
            f"duration: {elapsed_seconds:.6f}s\n"
        )


@pytest.fixture(scope="session", autouse=True)
def configure_file_logging():
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f"hw_02_figures_{datetime.now():%Y%m%d_%H%M%S_%f}.log"
    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    PROJECT_LOGGER.setLevel(logging.DEBUG)
    PROJECT_LOGGER.addHandler(handler)
    LOGGER.info("Writing test logs to %s", log_file)
    yield
    PROJECT_LOGGER.removeHandler(handler)
    handler.close()


@pytest.fixture
def log_test_case(request):
    parameters = getattr(request.node, "callspec", None)
    LOGGER.info("Test started: %s; parameters=%s", request.node.nodeid, getattr(parameters, "params", {}))
    yield
    LOGGER.info("Test finished: %s", request.node.nodeid)


@pytest.fixture()
def create_circle():
    circle = Circle(0)
    return circle


@pytest.fixture()
def create_triangle():
    triangle = Triangle(3, 3, 3)
    return triangle


@pytest.fixture()
def create_rectangle():
    rectangle = Rectangle(1, 2)
    return rectangle


@pytest.fixture()
def create_square():
    square = Square(1)
    return square
