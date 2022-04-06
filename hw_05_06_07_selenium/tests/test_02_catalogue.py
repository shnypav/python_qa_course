import allure
from selenium.webdriver.support.select import Select

from page_objects.CatalogPage import CatalogPage


@allure.suite("Catalogue testing")
def test_01_catalogue(browser, base_url):
    CatalogPage(browser).open_url(base_url, CatalogPage.MONITORS)
    assert CatalogPage(browser).get_element(CatalogPage.CONTENT_HEADER).text == "Monitors"


@allure.suite("Catalogue testing")
def test_02_product_thumb(browser, base_url):
    CatalogPage(browser).open_url(base_url, CatalogPage.MONITORS)
    elements = CatalogPage(browser).get_all_elements(CatalogPage.PRODUCTS)
    assert len(elements) == 2, "Wrong amount of items"


@allure.suite("Catalogue testing")
def test_03_empty_catalogue(browser, base_url):
    cp = CatalogPage(browser)
    cp.open_url(base_url, CatalogPage.SOFTWARE)
    text = cp.get_element(CatalogPage.CONTENT_SUB_HEADER).text
    assert text == "There are no products to list in this category."
    cp.link_presence("Continue")


@allure.suite("Catalogue testing")
@allure.description("""
The test verifies ability to change catalogue view mode: grid or list
""")
def test_04_view_switchers(browser, base_url):
    cp = CatalogPage(browser)
    cp.open_url(base_url, CatalogPage.MONITORS)
    cp.element_clickable(CatalogPage.GRID_VIEW)
    cp.element_clickable(CatalogPage.LIST_VIEW)


@allure.suite("Catalogue testing")
@allure.sub_suite("Catalogue sorting")
@allure.title("Test to check sorting options")
def test_05_sort_by_list(browser, base_url):
    CatalogPage(browser).open_url(base_url, CatalogPage.MONITORS)
    sort_by = CatalogPage(browser).element_clickable(CatalogPage.SORTING)
    assert Select(sort_by).first_selected_option.text == "Default"
