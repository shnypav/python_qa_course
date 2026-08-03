import datetime
import logging
import os
from pathlib import Path

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

LOGGER = logging.getLogger("selenium")
PROJECT_DIR = Path(__file__).resolve().parent
LOG_PATH = PROJECT_DIR.parent / "logs"
ALLURE_RESULTS_PATH = PROJECT_DIR / "allure-results"


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Please provide browser name")
    parser.addoption("--browser_ver", action="store", default="98.0")
    parser.addoption("--url", default="https://demo.opencart.com", help="Please provide url")
    parser.addoption("--log_level", default="INFO", help="Please provide logging level you want to use")
    parser.addoption("--executor", default="local", help="Provide executor for tests")


def choose_driver(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("executor")
    LOGGER.info("Creating %s driver for executor %s", browser, executor)

    try:
        if executor == "local":

            if browser == "chrome":
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            elif browser == "firefox":
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            else:
                LOGGER.error("Unsupported browser requested: %s", browser)
                raise ValueError("Browser is not supported")
        else:
            browser_ver = request.config.getoption("--browser_ver")
            if browser == "chrome":
                options = webdriver.ChromeOptions()
            elif browser == "firefox":
                options = webdriver.FirefoxOptions()
            else:
                LOGGER.error("Unsupported browser requested: %s", browser)
                raise ValueError("Browser is not supported")
            driver = webdriver.Remote(
                command_executor=f"http://{executor}:4444/wd/hub",
                desired_capabilities={
                    "browserName": browser,
                    "browserVersion": browser_ver,
                    "selenoid:options": {"enableVNC": True, "enableVideo": False},
                },
                options=options,
            )
            driver.maximize_window()
    except Exception:
        LOGGER.exception("Failed to create %s driver for executor %s", browser, executor)
        raise

    LOGGER.info("Created %s driver", browser)
    return driver


@pytest.fixture(scope="session", autouse=True)
def configure_logging(request):
    LOG_PATH.mkdir(exist_ok=True)
    log_file = LOG_PATH / f"hw_05_06_07_selenium_{datetime.datetime.now():%Y%m%d_%H%M%S_%f}.log"
    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    root_logger = logging.getLogger("selenium")
    root_logger.setLevel(request.config.getoption("--log_level").upper())
    root_logger.addHandler(handler)
    LOGGER.info("Selenium logging configured: %s", log_file)
    yield
    root_logger.removeHandler(handler)
    handler.close()


@pytest.fixture(scope="session")
def browser(request, configure_logging):
    driver = choose_driver(request)
    base_url = request.config.getoption("--url")
    try:
        LOGGER.info("Opening initial URL: %s", base_url)
        driver.get(base_url)
    except Exception:
        LOGGER.exception("Failed to open initial URL: %s", base_url)
        driver.quit()
        raise
    log_level = request.config.getoption("--log_level")
    driver.log_level = log_level

    yield driver
    try:
        LOGGER.info("Quitting browser driver")
        driver.quit()
    except Exception:
        LOGGER.exception("Failed to quit browser driver")


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture(scope="session", autouse=True)
def get_environment(pytestconfig, request, browser):
    props = {
        "Browser": request.config.getoption("--browser"),
        "Stand": 'Demo',
        "Shell": os.getenv("SHELL")
    }

    ALLURE_RESULTS_PATH.mkdir(exist_ok=True)
    with (ALLURE_RESULTS_PATH / "environment.properties").open("w", encoding="utf-8") as f:
        env_props = '\n'.join([f'{k}={v}' for k, v in props.items()])
        f.write(env_props)
    LOGGER.info("Wrote Allure environment properties")


# set up a hook to be able to check if a test has failed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)


# check if a test has failed
@pytest.fixture(scope="function", autouse=True)
def log_test_case(request):
    parameters = getattr(request.node, "callspec", None)
    LOGGER.info("Test started: %s; parameters=%s", request.node.nodeid, getattr(parameters, "params", {}))
    yield
    LOGGER.info("Test finished: %s", request.node.nodeid)


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request, browser):
    yield
    # request.node is an "item" because we use the default
    # "function" scope
    if request.node.rep_setup.failed:
        LOGGER.error("Test setup failed: %s", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            take_screenshot(browser, request.node.nodeid)
            LOGGER.error("Test execution failed: %s", request.node.nodeid)


# make a screenshot with a name of the test, date and time
def take_screenshot(browser, nodeid):
    try:
        screenshot = browser.get_screenshot_as_png()
        allure.attach(screenshot, name=f"{nodeid}_screenshot_{datetime.datetime.now()}", attachment_type=AttachmentType.PNG)
        LOGGER.info("Attached screenshot for failed test: %s", nodeid)
    except Exception:
        LOGGER.exception("Failed to capture screenshot for test: %s", nodeid)
