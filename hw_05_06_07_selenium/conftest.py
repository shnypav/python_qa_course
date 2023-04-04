import datetime
import logging
import os
import time

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.opera.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager

DRIVERS = os.path.expanduser("~/Downloads")
LOG_PATH = "../logs"


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Please provide browser name")
    parser.addoption("--browser_ver", action="store", default="98.0")
    parser.addoption("--url", default="https://demo.opencart.com", help="Please provide url")
    parser.addoption("--log_level", default="INFO", help="Please provide logging level you want to use")
    parser.addoption("--executor", default="local", help="Provide executor for tests")


def choose_driver(request):
    browser = request.config.getoption("--browser")

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
        browser_ver = request.config.getoption("--browser_ver")
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
            desired_capabilities={
                "browserName": browser,
                "browserVersion": browser_ver,
                "selenoid:options": {
                    "enableVNC": True,
                    "enableVideo": False
                }
            },
            options=options
        )
        driver.maximize_window()

    return driver


@pytest.fixture(scope="session")
def browser(request):
    driver = choose_driver(request)
    driver.get(request.config.getoption("--url"))
    log_level = request.config.getoption("--log_level")
    test_name = request.node.name

    if not os.path.exists(os.path.join(os.getcwd(), LOG_PATH)):
        os.mkdir(LOG_PATH)

    handler = logging.FileHandler(filename=f"{LOG_PATH}/log_{datetime.date.today()}.log", encoding="utf-8")
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


@pytest.fixture(scope="session", autouse=True)
def get_environment(pytestconfig, request, browser):
    props = {
        "Browser": request.config.getoption("--browser"),
        "Stand": 'Demo',
        "Shell": os.getenv("SHELL")
    }

    with open(f"../allure-results/environment.properties", "w") as f:
        env_props = '\n'.join([f'{k}={v}' for k, v in props.items()])
        f.write(env_props)


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
def test_failed_check(request, browser):
    yield
    # request.node is an "item" because we use the default
    # "function" scope
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            take_screenshot(browser, request.node.nodeid)
            print("executing test failed", request.node.nodeid)


# make a screenshot with a name of the test, date and time
def take_screenshot(browser, nodeid):
    time.sleep(1)

    allure.attach(browser.get_screenshot_as_png(), name=f"{nodeid}_screenshot_{datetime.datetime.now()}",
                  attachment_type=AttachmentType.PNG)
