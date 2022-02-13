from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


def test_01_item(browser, base_url):
    browser.get(f"{base_url}/index.php?route=product/product&path=33&product_id=31")
    assert browser.title == "Nikon D300"
    try:
        item_name = WebDriverWait(browser, 3).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, ".col-sm-4 > h1"))).text
        assert item_name == "Nikon D300"
    except TimeoutException:
        raise AssertionError("Item name was not found")


def test_02_buttons_clickable(browser):
    try:
        WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, ".fa.fa-heart")))
        WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, ".fa.fa-exchange")))
        WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#button-cart")))
    except TimeoutException:
        raise AssertionError("Button(s) not clickable")


def test_03_qty_field_editable(browser):
    try:
        qty_field = WebDriverWait(browser, 3).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "#input-quantity")))
        qty_field.clear()
        qty_field.send_keys("5")
        assert qty_field.get_attribute("value") == "5"
    except TimeoutException:
        raise AssertionError("Qty field was not found")


def test_04_description_review(browser):
    try:
        WebDriverWait(browser, 3).until(ec.visibility_of_element_located((By.LINK_TEXT, "Description")))
        WebDriverWait(browser, 3).until(ec.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Reviews")))
        WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.LINK_TEXT, "Description")))
        WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Reviews")))
    except TimeoutException:
        raise AssertionError("Tabs are not clickable")


def test_05_image(browser):
    try:
        WebDriverWait(browser, 3).until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".col-sm-8 img")))
    except TimeoutException:
        raise AssertionError("No image found")
