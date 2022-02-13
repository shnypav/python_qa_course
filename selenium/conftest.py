import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.opera import OperaDriverManager

DRIVERS = os.path.expanduser("~/Downloads")


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Please provide browser name")
    parser.addoption("--url", default="https://demo.opencart.com", help="Please provide url")


def choose_driver(browser):
    if browser == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser == "opera":
        driver = webdriver.Opera(executable_path=OperaDriverManager().install())
    else:
        raise Exception("Browser is not supported")

    return driver


@pytest.fixture(scope="session")
def browser(request):
    driver = choose_driver(request.config.getoption("--browser"))
    driver.get(request.config.getoption("--url"))
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--url")
