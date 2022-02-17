from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


def test_01_admin_page(browser, base_url):
    browser.get(f"{base_url}/admin")
    assert browser.title == "Administration"
    try:
        text = WebDriverWait(browser, 3).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, ".panel-title"))).text
        assert text == "Please enter your login details."
    except TimeoutException:
        raise AssertionError("Item was not found")


def test_02_credential_fields(browser):
    try:
        login = WebDriverWait(browser, 3).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "#input-username")))
        password = WebDriverWait(browser, 3).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "#input-password")))
        assert login.get_attribute("value") == "demo"
        assert password.get_attribute("value") == "demo"
    except TimeoutException:
        raise AssertionError("There are no fields for login and password")


def test_03_other_elements(browser):
    try:
        WebDriverWait(browser, 3).until(ec.visibility_of_element_located((By.LINK_TEXT, "Forgotten Password")))
        WebDriverWait(browser, 3).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
        WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    except TimeoutException:
        raise AssertionError("Elements were not found")
