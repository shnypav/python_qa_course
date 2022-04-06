import random
import string

import allure

from page_objects.RegistrationPage import RegistrationPage as rp


@allure.suite("User page testing")
def test_01_admin_page(browser, base_url):
    rp(browser).open_url(base_url, rp.REGISTRATION_LINK)
    assert rp(browser).get_title() == "Register Account"
    assert rp(browser).get_element(rp.PAGE_HEADER).text == "Register Account"


@allure.suite("User page testing")
def test_02_acc_links(browser):
    elements = rp(browser).get_all_elements(rp.LINKS_BLOCK)
    assert len(elements) == 13, "Wrong amount of items in block"


@allure.suite("User page testing")
def test_03_registration_fields(browser):
    rp(browser).element_presence(rp.FIRST_NAME)
    rp(browser).element_presence(rp.LAST_NAME)
    rp(browser).element_presence(rp.EMAIL)
    rp(browser).element_presence(rp.PHONE)
    rp(browser).element_presence(rp.PASSWORD)
    rp(browser).element_presence(rp.PASSWORD_CONFIRM)
    radio = rp(browser).get_all_elements(rp.RADIO_BUTTON)
    assert len(radio) == 2, "Wrong amount of items in block"


@allure.suite("User page testing")
def test_04_registration(browser):
    temp = ''.join(random.choice(string.ascii_lowercase) for _ in range(7))
    rp(browser).fill_input_field(rp.FIRST_NAME, temp)
    rp(browser).fill_input_field(rp.LAST_NAME, temp)
    rp(browser).fill_input_field(rp.EMAIL, f"{temp}@email.com")
    rp(browser).fill_input_field(rp.PHONE, "6666")
    rp(browser).fill_input_field(rp.PASSWORD, temp)
    rp(browser).fill_input_field(rp.PASSWORD_CONFIRM, temp)
    rp(browser).click_on_element(rp.AGREE)
    rp(browser).click_on_element(rp.SUBMIT)
    assert "Your Account Has Been Created!" in rp(browser).get_element(rp.SUCCESS).text
