from pages.BasePage import BaseClass as base_page
import locators.LoginPageLocators as login_page_locators
from selenium.webdriver.common.by import By

class LoginPage(base_page):
    # initialising the web driver
    def __init__(self, browser):
        super().__init__(browser)
        self.browser = browser

    def performLogin(self, username, password):
        self.sendText(username, login_page_locators.usernameField)
        self.sendText(password, login_page_locators.passwordField)
        self.clickOn(login_page_locators.loginButton)
        