from pages.BasePage import BaseClass as base_page
import locators.ProductsPageLocators as products_page_locators
import locators.CheckoutPageLocators as checkout_page_locators
from selenium.webdriver.common.by import By

class CheckoutPage(base_page):
    # initialising the web driver
    def __init__(self, browser):
        super().__init__(browser)
        self.browser = browser
    
    def performFillInUserDetails(self, firstName, lastName, postalCode):
        self.sendText(firstName, checkout_page_locators.firstName)
        self.sendText(lastName, checkout_page_locators.lastName)
        self.sendText(postalCode, checkout_page_locators.postalCode)

    def getAListOfTextItemsAddedInCart(self, list, elements):
        for element in elements:
            itemText = element.find_element_by_xpath('../..')
            itemName = itemText.find_element(By.CSS_SELECTOR,"div > a > div").text
            list.append(itemName)

    def getSumOfPriceItemsAddedInCart(self, elements):
        sum = 0
        for element in elements:
            itemPriceBar = element.find_element_by_xpath("..")
            priceProductText = itemPriceBar.find_element(By.CSS_SELECTOR, "div").text
            priceProduct = priceProductText.replace('$', '')
            sum += float(priceProduct)
        return sum