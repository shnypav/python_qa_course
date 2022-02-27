from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, browser):
        self.browser = browser

    def open_url(self, base_url, path):
        self.browser.get(f"{base_url}{path}")

    def element_presence(self, locator):
        try:
            return WebDriverWait(self.browser, 3).until((ec.visibility_of_element_located(locator)))
        except TimeoutException:
            raise AssertionError(f"Element was not found: {locator}")

    def all_elements_presence(self, locator):
        try:
            return WebDriverWait(self.browser, 3).until((ec.visibility_of_all_elements_located(locator)))
        except TimeoutException:
            raise AssertionError(f"Element was not found: {locator}")

    def link_presence(self, link_text):
        try:
            return WebDriverWait(self.browser, 3) \
                .until(ec.visibility_of_element_located((By.LINK_TEXT, link_text)))
        except TimeoutException:
            raise AssertionError(f"Link was not found: {link_text}")

    def element_clickable(self, locator):
        try:
            return WebDriverWait(self.browser, 3).until((ec.element_to_be_clickable(locator)))
        except TimeoutException:
            raise AssertionError(f"Element is not clickable: {locator}")

    def get_element(self, locator):
        return self.element_presence(locator)

    def get_all_elements(self, locator):
        return self.all_elements_presence(locator)

    def click_on_element(self, locator):
        self.element_clickable(locator).click()

    def get_title(self):
        title = self.browser.title
        return title

    def fill_input_field(self, locator, value):
        field = self.element_clickable(locator)
        field.click()
        field.clear()
        field.send_keys(value)

    def get_current_url(self):
        url = self.browser.current_url
        return url
