from selenium.webdriver.common.by import By

from .BasePage import BasePage


class ItemPage(BasePage):
    NOKOND300 = "/index.php?route=product/product&path=33&product_id=31"
    ITEM_HEADER = (By.CSS_SELECTOR, ".col-sm-4 > h1")
    FAVORITE_BUTTON = (By.CSS_SELECTOR, ".fa.fa-heart")
    COMPARE_BUTTON = (By.CSS_SELECTOR, ".fa.fa-exchange")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "#button-cart")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "#input-quantity")
    IMAGE = (By.CSS_SELECTOR, ".col-sm-8 img")
    REVIEWS_LINK = (By.PARTIAL_LINK_TEXT, "Reviews")
    DESCRIPTION_LINK = "Description"
