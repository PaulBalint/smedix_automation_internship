
from ast import Assert
from distutils.command import check
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
      self.products_page = ProductsPage(self.browser)
      self.login_page = LoginPage(self.browser)
      self.base_class = BaseClass(self.browser)

    #add 4 items in cart
    @pytest.mark.usefixtures("before_login_tests") 
    def test_add_four_items_to_cart(self):
      self.login_page.performLogin("standard_user", "secret_sauce")
      self.products_page.addMultipleItemsToCart(4)
      itemsInCart = self.base_class.getText(By.CSS_SELECTOR, products_locators.shoppingCart)
      assert itemsInCart == '4'

    #sort items by text parametrize
    textSortingOptions = [
      'Name (A to Z)',
      'Name (Z to A)'
    ]
    @pytest.mark.parametrize("sortingOptions", textSortingOptions)
    @pytest.mark.usefixtures("before_login_tests") 
    def test_sort_by_text(self, sortingOptions):
      self.login_page.performLogin("standard_user", "secret_sauce")
      products = self.browser.find_elements(By.CSS_SELECTOR, products_locators.productsNames)
      textPythonlist = []
      self.products_page.addElementsInAList(products, textPythonlist)
      self.products_page.sortListByAGivenOption(textPythonlist, sortingOptions, 'Name (A to Z)')
      sortContainer = self.browser.find_element(By.CSS_SELECTOR, products_locators.sorting_container)
      selectObjectByText = Select(sortContainer)
      selectObjectByText.select_by_visible_text(sortingOptions)
      productsAfterUiSorting = self.browser.find_elements(By.CSS_SELECTOR, products_locators.productsNames)
      textUiList = []
      self.products_page.addElementsInAList(productsAfterUiSorting, textUiList)
      newTextElement = self.base_class.getText(By.CSS_SELECTOR, products_locators.selected_option)
      assert newTextElement == sortingOptions.upper()
      assert textPythonlist == textUiList

    #sort items by price parametrize
    priceSortingOptions = [
      'Price (low to high)',
      'Price (high to low)'
    ]
    @pytest.mark.parametrize("sortingOptions", priceSortingOptions)
    @pytest.mark.usefixtures("before_login_tests") 
    def test_sort_by_price(self, sortingOptions):
      self.login_page.performLogin("standard_user", "secret_sauce")
      products = self.browser.find_elements(By.CSS_SELECTOR, products_locators.productsPrices)
      pricePythonlist = []
      self.products_page.createAParsedElementsList(products, pricePythonlist)
      self.products_page.sortListByAGivenOption(pricePythonlist, sortingOptions, 'Price (low to high)')
      sortContainer = self.browser.find_element(By.CSS_SELECTOR, products_locators.sorting_container)
      selectObjectByText = Select(sortContainer)
      selectObjectByText.select_by_visible_text(sortingOptions)
      productsAfterUiSorting = self.browser.find_elements(By.CSS_SELECTOR, products_locators.productsPrices)
      priceUiList = []
      self.products_page.createAParsedElementsList(productsAfterUiSorting, priceUiList)
      newTextElement = self.base_class.getText(By.CSS_SELECTOR, products_locators.selected_option)
      assert newTextElement == sortingOptions.upper()
      assert pricePythonlist == priceUiList

    #check add to cart button after re-click
    @pytest.mark.usefixtures("before_login_tests") 
    def test_check_addToCart_button_text_after_click_and_reclick(self):
      self.login_page.performLogin("standard_user", "secret_sauce")
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.thirdAddButtonBeforeAdd)
      textButton = self.base_class.getText(By.CSS_SELECTOR, products_locators.thirdAddButtonAfterAdd)
      assert textButton == 'REMOVE'
      self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.thirdAddButtonAfterAdd)
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.thirdAddButtonAfterAdd)
      textButton = self.base_class.getText(By.CSS_SELECTOR, products_locators.thirdAddButtonBeforeAdd)
      assert textButton == 'ADD TO CART'

    #verify that clicked product is displayed and added in cart
    @pytest.mark.usefixtures("before_login_tests") 
    def test_click_on_a_product_and_add_in_cart(self):
      self.login_page.performLogin("standard_user", "secret_sauce")
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.lightProduct)
      isDisplayed = self.base_class.isElementDisplayed(By.CSS_SELECTOR,products_locators.image)
      assert isDisplayed == True
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.addToCartBefore)
      textButton = self.base_class.getText(By.CSS_SELECTOR, products_locators.addToCartAfter)
      assert textButton == 'REMOVE'

    #verify that added product remain added when return to products page
    @pytest.mark.usefixtures("before_login_tests") 
    def test_return_to_products_after_add_a_product(self):
      self.login_page.performLogin("standard_user", "secret_sauce")
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.lightProduct)
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.addToCartBefore)
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.backToProductsButton)
      textButton = self.base_class.getText(By.CSS_SELECTOR, products_locators.lightRemoveButton)
      assert textButton == 'REMOVE'

    #check that reconnecting the cart remains same
    @pytest.mark.usefixtures("before_login_tests") 
    def test_check_cart_after_reconnecting(self):
      self.login_page.performLogin("standard_user", "secret_sauce")
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.lightAddButton)
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.burgerMenu)
      self.base_class.waitForElementToBeClickable(By.CSS_SELECTOR, products_locators.logoutSidebar)
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.logoutSidebar)
      self.login_page.performLogin("standard_user", "secret_sauce")
      textButton = self.base_class.getText(By.CSS_SELECTOR, products_locators.lightRemoveButton)
      assert textButton == "REMOVE"

    #try to open an item that doesn't exist
    @pytest.mark.usefixtures("before_login_tests") 
    def test_an_item_that_doesnt_exist_by_url(self):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.productImage)
        presentUrl = self.base_class.getUrl()
        presentUrl = presentUrl.replace('4', '7')
        self.browser.get(presentUrl)
        itemName = self.base_class.getText(By.CSS_SELECTOR, products_locators.itemNotFoundText)
        assert itemName == 'ITEM NOT FOUND'

    #navigate to another item and then back
    @pytest.mark.usefixtures("before_login_tests") 
    def test_navigate_to_another_product_and_back(self):
        self.login_page.performLogin("standard_user", "secret_sauce")
        self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.productImage)
        presentUrl = self.base_class.getUrl()
        newUrl = presentUrl.replace('4', '1')
        self.browser.get(newUrl)
        self.browser.back()
        actualUrl = self.base_class.getUrl()
        assert presentUrl == actualUrl

    #test performance glitch user continue shooping
    @pytest.mark.usefixtures("before_login_tests")  
    def test_performance_glitch_user_continue_shopping_button(self):
      self.login_page.performLogin('performance_glitch_user', 'secret_sauce')
      self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.shoppingCart)
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
      self.base_class.clickOnElement(By.CSS_SELECTOR, checkout_locators.continueShoppingButton)
      self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.shoppingCart)
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
      assert self.base_class.getText(By.CSS_SELECTOR, checkout_locators.title) == 'YOUR CART'

    #test performance glitch user sorting parametrize
    sortingOptions = [
      'Name (A to Z)',
      'Name (Z to A)',
      'Price (low to high)',
      'Price (high to low)'
    ]
    @pytest.mark.parametrize("options", sortingOptions)
    @pytest.mark.usefixtures("before_login_tests")  
    def test_performance_glitch_user_sorting(self, options):
      self.login_page.performLogin('performance_glitch_user', 'secret_sauce')
      self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.sorting_container)
      sortContainer = self.browser.find_element(By.CSS_SELECTOR, products_locators.sorting_container)
      selectObjectByText = Select(sortContainer)
      selectObjectByText.select_by_visible_text(options)
      self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.selected_option)
      newTextElement = self.base_class.getText(By.CSS_SELECTOR, products_locators.selected_option)
      assert newTextElement == options.upper()

    #test refresh on products page
    @pytest.mark.usefixtures("before_login_tests")  
    def test_performance_glitch_user_refresh(self):
      self.login_page.performLogin('performance_glitch_user', 'secret_sauce')
      self.browser.refresh()
      self.base_class.waitForElementToBeDisplayed(By.CSS_SELECTOR, products_locators.shoppingCart)
      self.base_class.clickOnElement(By.CSS_SELECTOR, products_locators.shoppingCart)
      assert self.base_class.getText(By.CSS_SELECTOR, products_locators.title) == 'YOUR CART'


    ################
    #Problem user tests
    #test images for items displayed in inventory 
    @pytest.mark.usefixtures("before_login_tests")  
    def test_items_images_displayed_in_inventory_for_problem_user(self):
      self.login_page.performLogin('problem_user', 'secret_sauce')
      
