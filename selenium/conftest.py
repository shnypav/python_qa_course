import datetime
import logging
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.opera.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager

DRIVERS = os.path.expanduser("~/Downloads")


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Please provide browser name")
    parser.addoption("--url", default="https://demo.opencart.com", help="Please provide url")
    parser.addoption("--log_level", default="INFO", help="Please provide logging level you want to use")
    parser.addoption("--executor", default="local", help="Provide executor for tests")


def choose_driver(request):
    browser = request.config.getoption("--browser")

    # options for selenoid
    capabilities = {
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": False
        }
    }

    if request.config.getoption("executor") == "local":

        if browser == "chrome":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif browser == "firefox":
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        elif browser == "opera":
            driver = webdriver.Opera(executable_path=OperaDriverManager().install())
        else:
            raise Exception("Browser is not supported")

    else:

        options = None
        if browser == "chrome":
            options = webdriver.ChromeOptions()
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
        elif browser == "opera":
            options = Options()
        else:
            raise Exception("Browser is not supported")
        driver = webdriver.Remote(
            command_executor=f"http://{request.config.getoption('executor')}:4444/wd/hub",
            desired_capabilities=capabilities,
            options=options
        )
        driver.maximize_window()

    return driver


@pytest.fixture(scope="module")
def browser(request):
    driver = choose_driver(request)
    driver.get(request.config.getoption("--url"))
    log_level = request.config.getoption("--log_level")
    test_name = request.node.name

    handler = logging.FileHandler(filename=f"../logs/log_{datetime.date.today()}.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger = logging.getLogger(name="Browser")
    logger.addHandler(handler)
    logger.setLevel(level=log_level)
    logger.info(f"Test {test_name} is started in browser {request.config.getoption('--browser')}")

    driver.log_level = log_level
    driver.test_name = test_name

    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture(scope="module", autouse=True)
def get_environment(pytestconfig, request, browser):
    props = {
        'Browser': request.config.getoption("--browser"),
        'Stand': 'Demo',
        'Shell': os.getenv('SHELL')
    }

    with open(f"../allure-results/environment.properties", "w") as f:
        env_props = '\n'.join([f'{k}={v}' for k, v in props.items()])
        f.write(env_props)
