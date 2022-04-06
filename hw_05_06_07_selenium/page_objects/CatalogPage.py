from selenium.webdriver.common.by import By

from .BasePage import BasePage


class CatalogPage(BasePage):
    MONITORS = "/index.php?route=product/category&path=25_28"
    SOFTWARE = "/index.php?route=product/category&path=17"
    CONTENT_HEADER = (By.CSS_SELECTOR, "#content h2")
    CONTENT_SUB_HEADER = (By.CSS_SELECTOR, "#content p")
    PRODUCTS = (By.CSS_SELECTOR, ".product-thumb")
    GRID_VIEW = (By.CSS_SELECTOR, "#grid-view")
    LIST_VIEW = (By.CSS_SELECTOR, "#list-view")
    SORTING = (By.CSS_SELECTOR, "#input-sort")
