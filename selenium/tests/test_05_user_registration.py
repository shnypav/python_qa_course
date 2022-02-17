from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


def test_01_admin_page(browser, base_url):
    browser.get(f"{base_url}/index.php?route=account/register")
    assert browser.title == "Register Account"
    try:
        text = WebDriverWait(browser, 3).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "#content >  h1"))).text
        assert text == "Register Account"
    except TimeoutException:
        raise AssertionError("Item was not found")


def test_02_acc_links(browser):
    try:
        elements = WebDriverWait(browser, 3).until(
            ec.visibility_of_all_elements_located((By.CSS_SELECTOR, ".list-group > a")))
        assert len(elements) == 13
    except TimeoutException:
        raise AssertionError("Links were not found")


def test_03_registration_fields(browser):
    try:
        first_name = WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#input-firstname")))
        last_name = WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#input-lastname")))
        email = WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#input-email")))
        phone = WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#input-telephone")))
        password = WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#input-lastname")))
        confirm = WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#input-lastname")))
        radio = WebDriverWait(browser, 3).until(
            ec.visibility_of_all_elements_located((By.CSS_SELECTOR, ".radio-inline")))
        assert len(radio) == 2
    except TimeoutException:
        raise AssertionError("Fields were not found")
