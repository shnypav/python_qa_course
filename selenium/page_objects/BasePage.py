import datetime
import logging

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, browser):
        self.browser = browser
        self.config_logger()

    def config_logger(self):
        self.handler = logging.FileHandler(filename=f"../logs/log_{datetime.date.today()}.log", encoding="utf-8")
        self.handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(name)s %(message)s"))
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(level=self.browser.log_level)

    @allure.step
    def open_url(self, base_url, path):
        self.logger.debug(f"Opening url = {base_url}{path}")
        self.browser.get(f"{base_url}{path}")

    @allure.step
    def element_presence(self, locator):
        self.logger.debug(f"Checking element presence by locator {locator}")
        try:
            return WebDriverWait(self.browser, 3).until((ec.visibility_of_element_located(locator)))
        except TimeoutException:
            self.logger.error(f"Element was not found: {locator}")
            raise AssertionError(f"Element was not found: {locator}")

    @allure.step
    def all_elements_presence(self, locator):
        self.logger.debug(f"Checking all elements presence by locator {locator}")
        try:
            return WebDriverWait(self.browser, 3).until((ec.visibility_of_all_elements_located(locator)))
        except TimeoutException:
            self.logger.error(f"Element was not found: {locator}")
            raise AssertionError(f"Element was not found: {locator}")

    @allure.step
    def link_presence(self, link_text):
        self.logger.debug(f"Checking link presence by link text {link_text}")
        try:
            return WebDriverWait(self.browser, 3) \
                .until(ec.visibility_of_element_located((By.LINK_TEXT, link_text)))
        except TimeoutException:
            self.logger.error(f"Link was not found: {link_text}")
            raise AssertionError(f"Link was not found: {link_text}")

    @allure.step
    def element_clickable(self, locator):
        self.logger.debug(f"Checking element clickable by locator {locator}")
        try:
            return WebDriverWait(self.browser, 3).until((ec.element_to_be_clickable(locator)))
        except TimeoutException:
            self.logger.error(f"Element is not clickable: {locator}")
            raise AssertionError(f"Element is not clickable: {locator}")

    @allure.step
    def get_element(self, locator):
        return self.element_presence(locator)

    @allure.step
    def get_all_elements(self, locator):
        return self.all_elements_presence(locator)

    @allure.step
    def click_on_element(self, locator):
        self.element_clickable(locator).click()

    @allure.step
    def get_title(self):
        self.logger.debug(f"Page title requested")
        title = self.browser.title
        self.logger.debug(f"Page title is '{title}'")
        return title

    @allure.step
    def fill_input_field(self, locator, value):
        self.logger.debug(f"Input field filling, locator = {locator}, value = {value}")
        field = self.element_clickable(locator)
        field.click()
        field.clear()
        field.send_keys(value)

    @allure.step
    def get_current_url(self):
        self.logger.debug(f"Current url requested")
        url = self.browser.current_url
        self.logger.debug(f"Current url is {url}")
        return url
