import allure
import pytest

from page_objects.MainPage import MainPage

pytestmark = pytest.mark.usefixtures("log_test_case")


@allure.suite("Main page testing")
@allure.severity(allure.severity_level.CRITICAL)
def test_01_title(browser):
    assert "Your Store" in MainPage(browser).get_title()


@allure.suite("Main page testing")
@allure.severity(allure.severity_level.NORMAL)
def test_02_search_items(browser):
    mp = MainPage(browser)
    mp.element_presence(MainPage.SEARCH_BUTTON)
    mp.element_presence(MainPage.INPUT_SEARCH)


@allure.suite("Main page testing")
@allure.severity(allure.severity_level.NORMAL)
def test_03_cart_button(browser):
    MainPage(browser).element_presence(MainPage.CART_BUTTON)


@allure.suite("Main page testing")
@allure.severity(allure.severity_level.NORMAL)
def test_04_slide_show(browser):
    MainPage(browser).element_presence(MainPage.SLIDESHOW)


@allure.suite("Main page testing")
@allure.severity(allure.severity_level.NORMAL)
def test_05_navbar(browser):
    elements = MainPage(browser).get_all_elements(MainPage.NAVBAR)
    assert len(elements) == 8


@allure.suite("Main page testing")
@allure.severity(allure.severity_level.NORMAL)
def test_06_change_currency(browser):
    MainPage(browser).click_on_element(MainPage.CURRENCY)
    MainPage(browser).click_on_element(MainPage.GBP)
    assert MainPage(browser).get_element(MainPage.CURRENCY_I).text == "£"


@allure.suite("Main page testing")
@allure.severity(allure.severity_level.NORMAL)
def test_07_logo(browser):
    MainPage(browser).element_presence(MainPage.LOGO)


@allure.suite("Main page testing")
@allure.severity(allure.severity_level.NORMAL)
def test_08_featured_products(browser):
    elements = MainPage(browser).get_all_elements(MainPage.FEATURED_PRODUCTS)
    assert len(elements) > 0, "No featured products on main page"


@allure.suite("Main page testing")
@allure.severity(allure.severity_level.MINOR)
def test_09_footer(browser):
    MainPage(browser).element_presence(MainPage.FOOTER)
