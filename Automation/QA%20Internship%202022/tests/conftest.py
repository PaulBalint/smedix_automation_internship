import datetime
import imp
import os
import time
from unittest import TestCase
import pytest
from selenium import webdriver

from pages.BasePage import BaseClass
from helpers.CleanupMethod import CleanupMethod
import allure

@pytest.fixture(scope = 'session', autouse = True)
def cleanup():
    cleanup = CleanupMethod()
    cleanup.reportsCleanup()


@pytest.fixture(scope = 'class')
def before_login_tests(request):

    browser = webdriver.Chrome()
    base_class = BaseClass(browser)
    base_class.launch_web_page("https://www.saucedemo.com/")
    if request.cls is not None:
        request.cls.browser = browser
    yield browser
    time.sleep(5)
    browser.quit()

@pytest.fixture()
def before_method():
    print("beforeMethod")
    # yield sets the hook for the after execution
    yield
    print("after beforeMethod")

