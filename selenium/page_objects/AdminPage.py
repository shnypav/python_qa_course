from selenium.webdriver.common.by import By

from .BasePage import BasePage


class AdminPage(BasePage):
    INPUT_USERNAME = (By.CSS_SELECTOR, "#input-username")
    INPUT_PASSWORD = (By.CSS_SELECTOR, "#input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    MENU_CATALOG = (By.CSS_SELECTOR, "#menu-catalog")
    PRODUCTS = (By.CSS_SELECTOR, "#menu-catalog ul li:nth-child(2) a")
    PRODUCT_ADD_BTN = (By.CSS_SELECTOR, ".pull-right a")
    PRODUCT_DELETE_BTN = (By.CSS_SELECTOR, ".pull-right button:nth-child(4)")
    PRODUCT_SAVE_BTN = (By.CSS_SELECTOR, ".pull-right button")
    FILTER_PRODUCT_NAME = (By.CSS_SELECTOR, "#filter-product #input-name")
    FILTER_APPLY_BTN = (By.CSS_SELECTOR, "#button-filter")
    PRODUCT_ADD_TITLE = (By.CSS_SELECTOR, ".container-fluid .panel-title")
    PRODUCT_DATA_TAB = (By.CSS_SELECTOR, "#form-product ul li:nth-child(2) a")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".tab-content #input-name1")
    PRODUCT_META_TAG_TITLE = (By.CSS_SELECTOR, ".tab-content #input-meta-title1")
    PRODUCT_MODEL = (By.CSS_SELECTOR, ".tab-content #input-model")
    RESULT_HEAD_CHECKBOX = (By.CSS_SELECTOR, "#form-product table thead input[type='checkbox']")
    RESULTS_NUMBER = (By.CSS_SELECTOR, ".col-sm-6.text-right")

    PRODUCT = {
        "Name": "Pikachu",
        "Meta Tag": "Pika",
        "Model": "Pokemon"
    }

    def open_admin_page(self, base_url):
        self.open_url(base_url, path="/admin")
        return self.get_title()

    def verify_login_form(self):
        self.element_presence(self.INPUT_USERNAME)
        self.element_presence(self.INPUT_PASSWORD)
        self.link_presence("Forgotten Password")

    def get_login_elements(self):
        name = self.get_element(self.INPUT_USERNAME)
        password = self.get_element(self.INPUT_PASSWORD)
        return name, password

    def login(self, username, password):
        self.get_element(self.INPUT_USERNAME).clear()
        self.get_element(self.INPUT_PASSWORD).clear()
        self.get_element(self.INPUT_USERNAME).send_keys(username)
        self.get_element(self.INPUT_PASSWORD).send_keys(password)
        self.get_element(self.LOGIN_BUTTON).click()

    def add_product(self):
        self.click_on_element(self.MENU_CATALOG)
        self.click_on_element(self.PRODUCTS)
        self.click_on_element(self.PRODUCT_ADD_BTN)

        text = self.element_presence(self.PRODUCT_ADD_TITLE).text
        assert text == "Add Product"

        self.fill_input_field(self.PRODUCT_NAME, self.PRODUCT["Name"])
        self.fill_input_field(self.PRODUCT_META_TAG_TITLE, self.PRODUCT["Meta Tag"])

        self.click_on_element(self.PRODUCT_DATA_TAB)
        self.fill_input_field(self.PRODUCT_MODEL, self.PRODUCT["Model"])

        self.click_on_element(self.PRODUCT_SAVE_BTN)

    def delete_product(self):
        self.click_on_element(self.MENU_CATALOG)
        self.click_on_element(self.PRODUCTS)
        self.fill_input_field(self.FILTER_PRODUCT_NAME, self.PRODUCT["Name"])
        self.click_on_element(self.FILTER_APPLY_BTN)

        self.click_on_element(self.RESULT_HEAD_CHECKBOX)
        self.click_on_element(self.PRODUCT_DELETE_BTN)
        alert = self.browser.switch_to.alert
        alert.accept()

    def find_product(self):
        self.click_on_element(self.MENU_CATALOG)
        self.click_on_element(self.PRODUCTS)
        self.fill_input_field(self.FILTER_PRODUCT_NAME, self.PRODUCT["Name"])
        self.click_on_element(self.FILTER_APPLY_BTN)
