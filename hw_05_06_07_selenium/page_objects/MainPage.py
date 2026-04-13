import allure
from selenium.webdriver.common.by import By

from .BasePage import BasePage


class MainPage(BasePage):
    INPUT_SEARCH = (By.CSS_SELECTOR, "[name=search]")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".input-group-btn")
    CART_BUTTON = (By.CSS_SELECTOR, "[id=cart]")
    CURRENCY = (By.CSS_SELECTOR, "[id=form-currency]")
    GBP = (By.CSS_SELECTOR, "[name=GBP]")
    CURRENCY_I = (By.CSS_SELECTOR, "strong")
    SLIDESHOW = (By.CSS_SELECTOR, "[id=slideshow0]")
    NAVBAR = (By.CSS_SELECTOR, "ul.navbar-nav > li")
    LOGO = (By.CSS_SELECTOR, "#logo")
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, "#featured .product-thumb")
    FOOTER = (By.CSS_SELECTOR, "#footer")

    @allure.step
    def search_elements(self):
        search_input = self.get_element(self.INPUT_SEARCH)
        search_button = self.get_element(self.SEARCH_BUTTON)
        return search_input, search_button
