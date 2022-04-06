import datetime

import allure
from allure_commons.types import AttachmentType

from env import PASS
from page_objects.AdminPage import AdminPage


@allure.suite("Admin page testing")
def test_01_admin_page(browser, base_url):
    title = AdminPage(browser).open_admin_page(base_url)
    assert title == "Administration"


@allure.suite("Admin page testing")
def test_02_credential_fields(browser):
    name, password = AdminPage(browser).get_login_elements()
    if "demo.opencart.com" in AdminPage(browser).get_current_url():
        assert name.get_attribute("value") == "demo"
        assert password.get_attribute("value") == "demo"
    else:
        assert name.get_attribute("value") == ""
        assert password.get_attribute("value") == ""


@allure.suite("Admin page testing")
def test_03_other_elements(browser):
    AdminPage(browser).verify_login_form()


@allure.suite("Admin page testing")
def test_04_admin_login(browser):
    if "demo.opencart.com" in AdminPage(browser).get_current_url():
        AdminPage(browser).login("demo", "demo")
    else:
        AdminPage(browser).login("admin", PASS)

    assert AdminPage(browser).get_title() == "Dashboard"


@allure.suite("Admin page testing")
def test_05_add_new_item_in_products(browser):
    AdminPage(browser).add_product()
    AdminPage(browser).find_product()
    results = AdminPage(browser).get_element(AdminPage.RESULTS_NUMBER).text
    try:
        assert "1 to 1 of 1" in results
    except AssertionError:
        # make a screenshot and attach to allure report in case of assertion error
        allure.attach(browser.get_screenshot_as_png(), name=f"Screenshot_{datetime.datetime.now()}",
                      attachment_type=AttachmentType.PNG)
        raise


@allure.suite("Admin page testing")
def test_06_delete_product(browser):
    AdminPage(browser).delete_product()
    AdminPage(browser).find_product()
    results = AdminPage(browser).get_element(AdminPage.RESULTS_NUMBER).text
    try:
        assert "0 to 0 of 0" in results
    except AssertionError:
        # make a screenshot and attach to allure report in case of assertion error
        allure.attach(browser.get_screenshot_as_png(), name=f"Screenshot_{datetime.datetime.now()}",
                      attachment_type=AttachmentType.PNG)
        raise
