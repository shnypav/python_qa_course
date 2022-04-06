from selenium.webdriver.common.by import By

from .BasePage import BasePage


class RegistrationPage(BasePage):
    REGISTRATION_LINK = "/index.php?route=account/register"
    PAGE_HEADER = (By.CSS_SELECTOR, "#content >  h1")
    LINKS_BLOCK = (By.CSS_SELECTOR, ".list-group > a")
    FIRST_NAME = (By.CSS_SELECTOR, "#input-firstname")
    LAST_NAME = (By.CSS_SELECTOR, "#input-lastname")
    EMAIL = (By.CSS_SELECTOR, "#input-email")
    PHONE = (By.CSS_SELECTOR, "#input-telephone")
    PASSWORD = (By.CSS_SELECTOR, "#input-password")
    PASSWORD_CONFIRM = (By.CSS_SELECTOR, "#input-confirm")
    RADIO_BUTTON = (By.CSS_SELECTOR, ".radio-inline")
    AGREE = (By.CSS_SELECTOR, "[name=agree]")
    SUBMIT = (By.CSS_SELECTOR, ".btn.btn-primary")
    SUCCESS = (By.CSS_SELECTOR, ".col-sm-9")
