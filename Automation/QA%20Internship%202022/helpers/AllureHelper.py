import allure
import pages.BasePage as Base
from selenium import webdriver
from allure_commons.types import AttachmentType

def log_step_info_message(self, text):
    with allure.step(text):  
        allure.attach(Base.BaseClass.screenshot(self), "stepScreenshot", AttachmentType.PNG)