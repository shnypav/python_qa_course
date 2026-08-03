from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

import pytest

from ..src.Circle import Circle
from ..src.Triangle import Triangle
from ..src.Rectangle import Rectangle
from ..src.Square import Square


TEST_RUN_LOG = Path(__file__).resolve().parents[1] / "test_run.log"


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
