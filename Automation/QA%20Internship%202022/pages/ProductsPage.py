from pages.BasePage import BaseClass as base_page
import locators.ProductsPageLocators as products_page_locators
from selenium.webdriver.common.by import By

class ProductsPage(base_page):
    # initialising the web driver
    def __init__(self, browser):
        super().__init__(browser)
        self.browser = browser

    def addMultipleItemsToCart(self, itemsNumber):
        elements = self.browser.find_elements(By.CSS_SELECTOR, products_page_locators.addToCartBefore)
        for item in range(0, itemsNumber):
            elements[item].click()

    def addElementsInAList(self, elements, list):
        for element in elements:
            list.append(element.text)

    def createAParsedElementsList(self, elements, newList):
        for element in elements:
            parsedElement = (element.text).replace('$','')
            parsedElementAsFloat = float(parsedElement)
            newList.append(parsedElementAsFloat)

    def sortListByAGivenOption(self, list, option, optionToBeEqual):
        if option == optionToBeEqual:
            list.sort()
        else: list.sort(reverse = True)

    #def addSrcAttributeInList(self, list, )
    def checkItemsImagesForProblemUser(self, itemsList, image):
        for item in itemsList:
            if item != image:
                return False
        return True
