
from ast import Assert
from time import sleep
import time
import unittest
from pyparsing import PrecededBy
import pytest
from selenium import webdriver
import helpers.AllureHelper as helper
import helpers.AllureMessages as messages
import allure_pytest
from pages.LoginPage import LoginPage
from pages.BasePage import BaseClass
from pages.ProductsPage import ProductsPage
from pages.CheckoutPage import CheckoutPage
import allure
from allure_commons.types import AttachmentType
import requests
from selenium.webdriver.common.by import By
import locators.LoginPageLocators as login_locators
import locators.ProductsPageLocators as products_locators
import locators.CheckoutPageLocators as checkout_locators
from datetime import datetime, timedelta
class Tests:

   @pytest.fixture(autouse = True)
   def class_objects(self):
      self.login_page = LoginPage(self.browser)
      self.base_class = BaseClass(self.browser)
      self.base_class = ProductsPage(self.browser)
      self.base_class = CheckoutPage(self.browser)

   #try to login locked user 
   @pytest.mark.usefixtures("before_login_tests")  
   def test_perform_login_locked_user(self):
      self.login_page.performLogin("locked_out_user", "secret_sauce")
      errorTextMessage = self.base_class.getText(By.CSS_SELECTOR, login_locators.errorMessage)
      assert errorTextMessage == "Epic sadface: Sorry, this user has been locked out."   

   #login with wrong user
   @pytest.mark.usefixtures("before_login_tests")  
   def test_perform_login_wrong_user(self):
      self.login_page.performLogin("_user", "secret_sauce")
      errorTextMessage = self.base_class.getText(By.CSS_SELECTOR, login_locators.errorMessage)
      assert errorTextMessage == "Epic sadface: Username and password do not match any user in this service"   

   #login with empty user
   @pytest.mark.usefixtures("before_login_tests")  
   def test_perform_login_empty_user(self):
      self.login_page.performLogin("", "secret_sauce")
      isErrorMessageDisplayed = self.base_class.isElementDisplayed(By.CSS_SELECTOR, login_locators.errorMessage)
      assert isErrorMessageDisplayed == True
      errorTextMessageUser = self.base_class.getText(By.CSS_SELECTOR, login_locators.errorMessage)
      assert errorTextMessageUser == 'Epic sadface: Username is required'

   #login with empty password
   @pytest.mark.usefixtures("before_login_tests")  
   def test_perform_login_empty_password(self):
      self.login_page.performLogin("standard_user", "")
      colorError = self.browser.find_element(By.CSS_SELECTOR, login_locators.passwordField).value_of_css_property('color')
      assert colorError == 'rgba(72, 76, 85, 1)'
      errorTextMessagePassword = self.base_class.getText(By.CSS_SELECTOR, login_locators.errorMessage)
      assert errorTextMessagePassword == 'Epic sadface: Password is required'

   #check input type for password
   @pytest.mark.usefixtures("before_login_tests")  
   def test_check_input_type_password(self):   
      typeElem = self.browser.find_element(By.CSS_SELECTOR, login_locators.passwordField).get_attribute("type")
      assert typeElem == 'password'


   #refreshing the page the fields content dissapear
   @pytest.mark.usefixtures("before_login_tests")  
   def test_refresh_login_page(self):
      self.base_class.sendText("standard_user", login_locators.usernameField)
      self.base_class.sendText("secret_sauce", login_locators.passwordField)
      self.base_class.browser.refresh
      username = self.base_class.getText(By.CSS_SELECTOR,login_locators.usernameField)
      password = self.base_class.getText(By.CSS_SELECTOR,login_locators.passwordField)
      assert username == ""
      assert password == ""

   #back after login redirect to login page
   @pytest.mark.usefixtures("before_login_tests")  
   def test_back_after_login(self):
      self.login_page.performLogin("standard_user", "secret_sauce")
      self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.productPageTitle)
      isShopCartDisplayed = self.base_class.isElementDisplayed(By.CSS_SELECTOR, products_locators.shoppingCart)
      assert isShopCartDisplayed == True
      self.base_class.browser.back()
      isLoginButtonDisplayed = self.base_class.isElementDisplayed(By.CSS_SELECTOR, login_locators.loginButton)
      assert isLoginButtonDisplayed == True

   #how much time take to log in
   @pytest.mark.usefixtures("before_login_tests")  
   def test_time_take_to_log_in(self):
      self.browser.find_element(By.CSS_SELECTOR, login_locators.usernameField).send_keys("standard_user")
      self.browser.find_element(By.CSS_SELECTOR, login_locators.passwordField).send_keys("secret_sauce")
      start_time = time.time()
      self.base_class.clickOnElement(By.CSS_SELECTOR, login_locators.loginButton)
      self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.productPageTitle)
      end_time = time.time()
      total_time = end_time - start_time
      assert total_time < 2

   #login with different users
   usersCredentials = [
      ('standard_user', 'secret_sauce'),
      ('problem_user', 'secret_sauce'),
      ('performance_glitch_user', 'secret_sauce')
   ]   
   @pytest.mark.parametrize("username,password", usersCredentials)
   @pytest.mark.usefixtures("before_login_tests")
   def test_multiple_login(self, username, password):
      self.login_page.performLogin(username, password)
      isDisplayedShoppingCart = self.base_class.isElementDisplayed(By.CSS_SELECTOR, products_locators.shoppingCart)
      assert isDisplayedShoppingCart == True
      self.browser.back()
      self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, login_locators.loginButton)

   #test performance glitch user log in
   @pytest.mark.usefixtures("before_login_tests")  
   def test_performance_glitch_user_click_after_log_in(self):
      self.login_page.performLogin('performance_glitch_user', 'secret_sauce')
      self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.shoppingCart)
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
      textTitle = self.base_class.getText(By.CSS_SELECTOR, checkout_locators.title)
      assert textTitle == 'YOUR CART'