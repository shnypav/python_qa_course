import pytest


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="https://ya.ru", help="Please provide url")
    parser.addoption("--status_code", action="store", default="200", help="Please provide status code")


@pytest.fixture
def url_given(request):
    return request.config.getoption("--url")


@pytest.fixture
def status_given(request):
    return request.config.getoption("--status_code")
