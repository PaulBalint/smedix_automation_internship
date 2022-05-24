
from ast import Assert
from time import sleep
import time
from tkinter.tix import Select
import unittest
import pytest
from selenium import webdriver
import helpers.AllureHelper as helper
import helpers.AllureMessages as messages
import allure_pytest
from pages.CheckoutPage import CheckoutPage
from pages.ProductsPage import ProductsPage
from pages.LoginPage import LoginPage
from pages.BasePage import BaseClass
import allure
from allure_commons.types import AttachmentType
import requests
from selenium.webdriver.common.by import By
import locators.LoginPageLocators as login_locators
import locators.ProductsPageLocators as products_locators
import locators.CheckoutPageLocators as checkout_locators
from datetime import datetime, timedelta
from selenium.webdriver.support.select import Select
class Tests:

    @pytest.fixture(autouse = True)
    def class_objects(self):
        self.checkout_page = CheckoutPage(self.browser)
        self.products_page = ProductsPage(self.browser)
        self.login_page = LoginPage(self.browser)
        self.base_class = BaseClass(self.browser)

    #order two products
    @pytest.mark.usefixtures("before_login_tests") 
    def test_add_two_items_to_cart(self):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.products_page.addMultipleItemsToCart(2)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        assert self.base_class.getUrl() == checkout_locators.cartUrl
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.checkoutButton)
        assert self.base_class.getUrl() == checkout_locators.checkoutFirstStepUrl
        self.checkout_page.performFillInUserDetails('Paul', 'Balint', '610115')
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.continueButton)
        assert self.base_class.getUrl() == checkout_locators.checkoutSecondStepUrl
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.finishButton)
        assert self.base_class.getUrl() == checkout_locators.checkoutCompleteUrl
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, checkout_locators.ponyExpressImage)
        assert self.base_class.isElementDisplayed(By.CSS_SELECTOR, checkout_locators.ponyExpressImage)

    #check functionality for back home button after sent order
    @pytest.mark.usefixtures("before_login_tests") 
    def test_back_to_home_button(self):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.products_page.addMultipleItemsToCart(3)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, checkout_locators.checkoutButton)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.checkoutButton)
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, checkout_locators.firstName)
        self.checkout_page.performFillInUserDetails('Paul', 'Balint', '610115')
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.continueButton)
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, checkout_locators.finishButton)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.finishButton)
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, checkout_locators.backHomeButton)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.backHomeButton)
        assert self.base_class.getUrl() == products_locators.inventoryUrl
        assert self.base_class.getText(By.CSS_SELECTOR, products_locators.shoppingCart) == ''

    #continue shooping button redirect back to products page
    @pytest.mark.usefixtures("before_login_tests") 
    def test_continue_shopping_button(self):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.products_page.addMultipleItemsToCart(3)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, checkout_locators.continueShoppingButton)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.continueShoppingButton)
        assert self.base_class.getUrl() == products_locators.inventoryUrl
        assert self.base_class.getText(By.CSS_SELECTOR, products_locators.shoppingCart) == '3'

    #cancel from step one checkout redirect to cart page
    @pytest.mark.usefixtures("before_login_tests") 
    def test_cancel_button_from_step_one_checkout(self):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.products_page.addMultipleItemsToCart(3)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, checkout_locators.checkoutButton)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.checkoutButton)
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, checkout_locators.cancelButton)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.cancelButton)
        assert self.base_class.getUrl() == checkout_locators.cartUrl
        assert self.base_class.getText(By.CSS_SELECTOR, products_locators.shoppingCart) == '3'

    #checkout with empty user details fields parametrized
    usersDetails = [
        ('', 'Paul', '611015', 'Error: First Name is required'),
        ('Balint', '', '611015', 'Error: Last Name is required'),
        ('Balint', 'Paul', '', 'Error: Postal Code is required')
    ]   
    @pytest.mark.parametrize("firstName,lastName,postalCode,error", usersDetails)
    @pytest.mark.usefixtures("before_login_tests")
    def test_checkout_with_empty_details(self, firstName, lastName, postalCode, error):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.products_page.addMultipleItemsToCart(2)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.checkoutButton)
        self.checkout_page.performFillInUserDetails(firstName, lastName, postalCode)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.continueButton)
        assert self.checkout_page.getText(By.CSS_SELECTOR, checkout_locators.errorContainer) == error

    #cancel from step two checkout redirect to products page
    @pytest.mark.usefixtures("before_login_tests") 
    def test_cancel_button_from_step_two_checkout(self):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.products_page.addMultipleItemsToCart(2)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.checkoutButton)
        self.checkout_page.performFillInUserDetails('Paul', 'Balint', '610115')
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.continueButton)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.cancelButton)
        assert self.base_class.getUrl() == products_locators.inventoryUrl

    #what items are added appear in cart 
    @pytest.mark.usefixtures("before_login_tests") 
    def test_cart_contain_right_items(self):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.products_page.addMultipleItemsToCart(4)
        productsAddedInCart = []
        clickedButtons = self.browser.find_elements(By.CSS_SELECTOR, products_locators.addToCartAfter)
        self.checkout_page.getAListOfTextItemsAddedInCart(productsAddedInCart, clickedButtons)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        productsInCart = []
        productsNames = self.browser.find_elements(By.CSS_SELECTOR, checkout_locators.productName)
        for productName in productsNames:
            productsInCart.append(productName.text)
        assert productsAddedInCart.sort() == productsInCart.sort()

    #check if total price is right
    @pytest.mark.usefixtures("before_login_tests") 
    def test_check_price(self):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.products_page.addMultipleItemsToCart(4)
        clickedButtons = self.browser.find_elements(By.CSS_SELECTOR, products_locators.addToCartAfter)
        sumPrices = self.checkout_page.getSumOfPriceItemsAddedInCart(clickedButtons)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.checkoutButton)
        self.checkout_page.performFillInUserDetails('Paul', 'Balint', '610115')
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.continueButton)
        finalPrice = self.base_class.getText(By.CSS_SELECTOR, checkout_locators.summarySubtotal)
        finalPrice = finalPrice.replace('Item total: $', '')
        finalPrice = float(finalPrice)
        assert sumPrices == finalPrice
        sumPrices = round(float(sumPrices),2)
        tax = self.base_class.getText(By.CSS_SELECTOR, checkout_locators.summaryTaxLabel)
        tax = tax.replace('Tax: $', '')
        tax = float(tax)
        totalTax = sumPrices*0.08
        totalTax = round(totalTax,2)
        assert totalTax == tax

    #back to another page works properly
    @pytest.mark.usefixtures("before_login_tests") 
    def test_back_to_a_page_after_redirected_manual_to_one(self):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.products_page.addMultipleItemsToCart(2)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.checkoutButton)
        presentUrl = self.base_class.getUrl()
        self.browser.get('https://www.saucedemo.com/inventory.html')
        self.browser.back()
        actualUrl = self.base_class.getUrl()
        assert presentUrl == actualUrl

    #forward to another page works properly
    @pytest.mark.usefixtures("before_login_tests") 
    def test_forward_to_a_page_after_redirected_manual_to_one(self):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.browser.get('https://www.saucedemo.com/inventory.html')
        self.browser.back()
        self.browser.forward()
        actualUrl = self.base_class.getUrl()
        assert actualUrl == 'https://www.saucedemo.com/inventory.html'

    #test back browser for for performance_glitch_user
    @pytest.mark.usefixtures("before_login_tests")  
    def test_performance_glitch_user_back_browser(self):
        self.login_page.performLogin('performance_glitch_user', 'secret_sauce')
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.browser.back()
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.sorting_container)
        assert self.base_class.getText(By.CSS_SELECTOR, products_locators.title) == 'PRODUCTS'

    #test click on cart after cancel from step two checkout for performance_glitch_user
    @pytest.mark.usefixtures("before_login_tests")  
    def test_performance_glitch_user_cancel(self):
        self.login_page.performLogin('performance_glitch_user', 'secret_sauce')
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.checkoutButton)
        self.checkout_page.performFillInUserDetails('Paul', 'Balint', '610115')
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.continueButton)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.cancelButton)
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.sorting_container)
        assert self.base_class.getText(By.CSS_SELECTOR, products_locators.title) == 'PRODUCTS'

    #test back to products button for performance_glitch_user
    @pytest.mark.usefixtures("before_login_tests")  
    def test_performance_glitch_user_back_to_products(self):
        self.login_page.performLogin('performance_glitch_user', 'secret_sauce')
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.productsNames)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.productsNames)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.backToProductsButton)
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.productsNames)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.productsNames)
        assert self.base_class.getText(By.CSS_SELECTOR, products_locators.inventoryDetailsName) == 'Sauce Labs Backpack'

    #test back home button for performance glitch user
    @pytest.mark.usefixtures("before_login_tests")  
    def test_performance_glitch_user_cancel(self):
        self.login_page.performLogin('performance_glitch_user', 'secret_sauce')
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.checkoutButton)
        self.checkout_page.performFillInUserDetails('Paul', 'Balint', '610115')
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.continueButton)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.finishButton)
        self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.backHomeButton)
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.sorting_container)
        assert self.base_class.getText(By.CSS_SELECTOR, products_locators.title) == 'PRODUCTS'

    #test 'all items' option from burger menu for performance glitch user
    @pytest.mark.usefixtures("before_login_tests")  
    def test_performance_glitch_user_click_all_items_burger_menu(self):
        self.login_page.performLogin('performance_glitch_user', 'secret_sauce')
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.burgerMenu)
        self.base_class.waitForElementToBeClickable(By.CSS_SELECTOR, products_locators.allItemsSidebar)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.allItemsSidebar)
        self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.shoppingCart)
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
        assert self.base_class.getText(By.CSS_SELECTOR, checkout_locators.title) == 'YOUR CART'
