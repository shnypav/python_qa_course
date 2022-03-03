from page_objects.MainPage import MainPage


def test_01_title(browser):
    assert "Your Store" in MainPage(browser).get_title()


def test_02_search_items(browser):
    mp = MainPage(browser)
    mp.element_presence(MainPage.SEARCH_BUTTON)
    mp.element_presence(MainPage.INPUT_SEARCH)


def test_03_cart_button(browser):
    MainPage(browser).element_presence(MainPage.CART_BUTTON)


def test_04_slide_show(browser):
    MainPage(browser).element_presence(MainPage.SLIDESHOW)


def test_05_navbar(browser):
    elements = MainPage(browser).get_all_elements(MainPage.NAVBAR)
    assert len(elements) == 8


def test_06_change_currency(browser):
    MainPage(browser).click_on_element(MainPage.CURRENCY)
    MainPage(browser).click_on_element(MainPage.GBP)
    assert MainPage(browser).get_element(MainPage.CURRENCY_I).text == "£"
