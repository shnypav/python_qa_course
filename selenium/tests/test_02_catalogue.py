from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select


def test_01_catalogue(browser, base_url):
    browser.get(f"{base_url}/index.php?route=product/category&path=25_28")
    text = WebDriverWait(browser, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#content h2"))).text
    assert text == "Monitors"


def test_02_product_thumb(browser, base_url):
    browser.get(f"{base_url}/index.php?route=product/category&path=25_28")
    elements = WebDriverWait(browser, 5).until(
        ec.visibility_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb")))
    assert len(elements) == 2


def test_03_empty_catalogue(browser, base_url):
    browser.get(f"{base_url}/index.php?route=product/category&path=17")
    text = WebDriverWait(browser, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#content p"))).text
    assert text == "There are no products to list in this category."
    browser.find_element(By.LINK_TEXT, "Continue")


def test_04_view_switchers(browser, base_url):
    browser.get(f"{base_url}/index.php?route=product/category&path=25_28")
    try:
        WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#grid-view")))
        WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#list-view")))
    except TimeoutException:
        raise AssertionError("View switcher elements were not found")


def test_05_sort_by_list(browser, base_url):
    browser.get(f"{base_url}/index.php?route=product/category&path=25_28")
    try:
        sort_by = WebDriverWait(browser, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#input-sort")))
        assert Select(sort_by).first_selected_option.text == "Default"
    except TimeoutException:
        raise AssertionError("Element was not found")
