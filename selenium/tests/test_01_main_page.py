from selenium.webdriver.common.by import By


def test_01_title(browser):
    assert "Your Store" in browser.title


def test_02_search_items(browser):
    browser.find_element(By.CSS_SELECTOR, "[name=search]")
    browser.find_element(By.CSS_SELECTOR, ".input-group-btn")


def test_03_cart_button(browser):
    browser.find_element(By.CSS_SELECTOR, "[id=cart]")


def test_04_slide_show(browser):
    browser.find_element(By.CSS_SELECTOR, "[id=slideshow0]")


def test_05_navbar(browser):
    elements = browser.find_elements(By.CSS_SELECTOR, "ul.navbar-nav > li")
    assert len(elements) == 8, "Wrong amount of items in navbar"
