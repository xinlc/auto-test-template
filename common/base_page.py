""" POM 基类

POM 通用操作
"""

__author__ = 'Richard'
__version__ = '2021-07-10'

import json
from page_objects import PageObject, PageElement
from common.requests_helper import SharedAPI
from common.selenium_helper import SeleniumHelper


class BasePage(PageObject):

    def __init__(self, driver=None):
        """
            :arg driver
        """
        if driver is not None:
            self.driver = driver
        else:
            self.driver = SeleniumHelper.initial_driver()
        super().__init__(self.driver)

    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    def send_text(self, text, *loc):
        self.find_element(*loc).send_keys(text)

    def click(self, *loc):
        self.find_element(*loc).click()

    def clear(self, *loc):
        self.find_element(*loc).clear()

    def get_title(self):
        return self.driver.title
