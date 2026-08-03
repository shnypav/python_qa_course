import logging

import allure
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, browser):
        self.browser = browser
        self.logger = logging.getLogger(f"selenium.{type(self).__name__}")

    @allure.step
    def open_url(self, base_url, path):
        """

        @param base_url:
        @param path:
        """
        url = f"{base_url}{path}"
        self.logger.info("Opening URL: %s", url)
        try:
            self.browser.get(url)
        except WebDriverException:
            self.logger.exception("Failed to open URL: %s", url)
            raise

    @allure.step
    def element_presence(self, locator):
        self.logger.debug("Waiting for visible element: %s", locator)
        try:
            element = WebDriverWait(self.browser, 3).until((ec.visibility_of_element_located(locator)))
        except TimeoutException:
            self.logger.exception("Element was not found within 3 seconds: %s", locator)
            raise AssertionError(f"Element was not found: {locator}")
        self.logger.debug("Visible element found: %s", locator)
        return element

    @allure.step
    def all_elements_presence(self, locator):
        self.logger.debug("Waiting for visible elements: %s", locator)
        try:
            elements = WebDriverWait(self.browser, 3).until((ec.visibility_of_all_elements_located(locator)))
        except TimeoutException:
            self.logger.exception("Elements were not found within 3 seconds: %s", locator)
            raise AssertionError(f"Element was not found: {locator}")
        self.logger.debug("Found %s visible elements: %s", len(elements), locator)
        return elements

    @allure.step
    def link_presence(self, link_text):
        self.logger.debug("Waiting for visible link: %s", link_text)
        try:
            link = WebDriverWait(self.browser, 3) \
                .until(ec.visibility_of_element_located((By.LINK_TEXT, link_text)))
        except TimeoutException:
            self.logger.exception("Link was not found within 3 seconds: %s", link_text)
            raise AssertionError(f"Link was not found: {link_text}")
        self.logger.debug("Visible link found: %s", link_text)
        return link

    @allure.step
    def element_clickable(self, locator):
        self.logger.debug("Waiting for clickable element: %s", locator)
        try:
            element = WebDriverWait(self.browser, 3).until((ec.element_to_be_clickable(locator)))
        except TimeoutException:
            self.logger.exception("Element is not clickable within 3 seconds: %s", locator)
            raise AssertionError(f"Element is not clickable: {locator}")
        self.logger.debug("Clickable element found: %s", locator)
        return element

    @allure.step
    def get_element(self, locator):
        return self.element_presence(locator)

    @allure.step
    def get_all_elements(self, locator):
        return self.all_elements_presence(locator)

    @allure.step
    def click_on_element(self, locator):
        self.logger.info("Clicking element: %s", locator)
        try:
            self.element_clickable(locator).click()
        except WebDriverException:
            self.logger.exception("Failed to click element: %s", locator)
            raise

    @allure.step
    def get_title(self):
        self.logger.debug("Page title requested")
        title = self.browser.title
        self.logger.debug("Page title is %r", title)
        return title

    @allure.step
    def fill_input_field(self, locator, value):
        self.logger.info("Filling input field: %s", locator)
        try:
            field = self.element_clickable(locator)
            field.click()
            field.clear()
            field.send_keys(value)
        except WebDriverException:
            self.logger.exception("Failed to fill input field: %s", locator)
            raise

    @allure.step
    def get_current_url(self):
        self.logger.debug("Current URL requested")
        url = self.browser.current_url
        self.logger.debug("Current URL is %s", url)
        return url
