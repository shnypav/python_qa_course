from env import PASS
from page_objects.AdminPage import AdminPage


def test_01_admin_page(browser, base_url):
    title = AdminPage(browser).open_admin_page(base_url)
    assert title == "Administration"


def test_02_credential_fields(browser):
    name, password = AdminPage(browser).get_login_elements()
    if "demo.opencart.com" in AdminPage(browser).get_current_url():
        assert name.get_attribute("value") == "demo"
        assert password.get_attribute("value") == "demo"
    else:
        assert name.get_attribute("value") == ""
        assert password.get_attribute("value") == ""


def test_03_other_elements(browser):
    AdminPage(browser).verify_login_form()


def test_04_admin_login(browser):
    if "demo.opencart.com" in AdminPage(browser).get_current_url():
        AdminPage(browser).login("demo", "demo")
    else:
        AdminPage(browser).login("admin", PASS)

    assert AdminPage(browser).get_title() == "Dashboard"


def test_05_add_new_item_in_products(browser):
    AdminPage(browser).add_product()
    AdminPage(browser).find_product()
    results = AdminPage(browser).get_element(AdminPage.RESULTS_NUMBER).text
    assert "1 to 1 of 1" in results


def test_06_delete_product(browser):
    AdminPage(browser).delete_product()
    AdminPage(browser).find_product()
    results = AdminPage(browser).get_element(AdminPage.RESULTS_NUMBER).text
    assert "0 to 0 of 0" in results
