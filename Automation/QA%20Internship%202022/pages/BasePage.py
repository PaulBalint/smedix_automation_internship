from telnetlib import EC
from traceback import print_stack
import allure_commons
from allure_commons.types import AttachmentType
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import allure

from helpers import AllureMessages


class BaseClass:

    def __init__(self, browser):
        self.browser = browser

    def launch_web_page(self, url, title = None):
        try:
            self.browser.get(url)
            self.browser.maximize_window()
            if title:
                assert title in self.browser.title
        except:
            print_stack()

    def get_locator_type(self, locator_type = "css"):
        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "tag":
            return By.TAG_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        elif locator_type == "plink":
            return By.PARTIAL_LINK_TEXT
        else:
            print("Locator Type : " + locator_type + " entered is not found")
        return False

    def getWebElement(self, locatorValue, locator_type= "css"):
        webElement = None
        try:
            locator_type = locator_type.lower()
            locatorByType = self.get_locator_type(locator_type)
            webElement = self.browser.find_element(locatorByType, locatorValue)
        except:
            print_stack()
        return webElement

    def waitForElement(self, locatorValue, locator_type="css", timeout = 25, frequency = 1):
        webElement = None
        try:
            locator_type = locator_type.lower()
            locatorByType = self.get_locator_type(locator_type)
            wait = WebDriverWait(self.browser, timeout, poll_frequency= frequency,
                                 ignored_exceptions= [ElementNotVisibleException, NoSuchElementException])
            webElement = wait.until(ec.presence_of_element_located((locatorByType, locatorValue)))
        except:
            print_stack()
        return webElement

    def clickOn(self, locatorValue, locator_type="css"):
        try:
            locator_type = locator_type.lower()
            self.waitForElement(locatorValue, locator_type)
            webElement = self.getWebElement(locatorValue, locator_type)
            webElement.click()
        except:
            print_stack()
            assert False

    def sendText(self, text, locatorValue, locator_type="css"):
        try:
            locator_type = locator_type.lower()
            webElement = self.waitForElement(locatorValue, locator_type)
            webElement.send_keys(text)
        except:
            print_stack()

    def getElementText(self, locatorValue, locator_type="css"):
        elementText = None
        try:
            locator_type = locator_type.lower()
            webElement = self.waitForElement(locatorValue, locator_type)
            elementText = webElement.text
        except:
            print_stack()

        return elementText

    def verifyIsElementDisplayed(self, locatorValue, locator_type="css"):
        elementDisplayed = None
        try:
            locator_type = locator_type.lower()
            webElement = self.waitForElement(locatorValue, locator_type)
            elementDisplayed = webElement.is_displayed()
        except:
            print_stack()
        return elementDisplayed

    def screenshot(self):
        scr = self.browser.get_screenshot_as_png()
        return scr

    def waitForElementToBeDisplayed(self, locator_type, locatorValue, maxtime=30, frequency=1):
        wait = WebDriverWait(self.browser, maxtime, poll_frequency = frequency, ignored_exceptions = [NoSuchElementException, ElementNotVisibleException])
        wait.until(ec.presence_of_element_located((locator_type,locatorValue)))

    def waitForElementToBeClickable(self, locator_type, locatorValue, maxtime = 30, searchFrequency = 1):
        wait = WebDriverWait(self.browser, maxtime, poll_frequency = searchFrequency, ignored_exceptions = [NoSuchElementException, ElementNotVisibleException])
        wait.until(ec.element_to_be_clickable((locator_type, locatorValue)))

    def getText(self, locator_type, locatorValue):
        text = self.browser.find_element(locator_type, locatorValue).text
        return text

    def isElementDisplayed(self, locator_type, locatorValue):
        isDisplayed = self.browser.find_element(locator_type, locatorValue).is_displayed()
        return isDisplayed

    def clickOnElement(self, locator_type, locatorValue):
        self.browser.find_element(locator_type, locatorValue).click()

    def getUrl(self):
        return self.browser.current_url