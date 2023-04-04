import allure

from page_objects.MainPage import MainPage


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
