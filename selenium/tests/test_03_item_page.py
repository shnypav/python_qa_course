import allure

from page_objects.ItemPage import ItemPage


@allure.suite("Item's page testing")
def test_01_item(browser, base_url):
    ItemPage(browser).open_url(base_url, ItemPage.NOKOND300)
    assert ItemPage(browser).get_title() == "Nikon D300"
    item_name = ItemPage(browser).get_element(ItemPage.ITEM_HEADER).text
    assert item_name == "Nikon D300"


@allure.suite("Item's page testing")
def test_02_buttons_clickable(browser):
    ItemPage(browser).element_clickable(ItemPage.FAVORITE_BUTTON)
    ItemPage(browser).element_clickable(ItemPage.COMPARE_BUTTON)
    ItemPage(browser).element_clickable(ItemPage.ADD_TO_CART_BUTTON)


@allure.suite("Item's page testing")
def test_03_qty_field_editable(browser):
    qty_field = ItemPage(browser).get_element(ItemPage.QUANTITY_INPUT)
    qty_field.clear()
    qty_field.send_keys("5")
    assert qty_field.get_attribute("value") == "5"


@allure.suite("Item's page testing")
def test_04_description_review(browser):
    ip = ItemPage(browser)
    ip.link_presence(ItemPage.DESCRIPTION_LINK)
    ip.element_presence(ItemPage.REVIEWS_LINK)
    ip.element_clickable(ItemPage.REVIEWS_LINK)


@allure.suite("Item's page testing")
def test_05_image(browser):
    ItemPage(browser).element_presence(ItemPage.IMAGE)
