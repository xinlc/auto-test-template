"""Select 选择器

当选项过多时，使用下拉菜单展示并选择内容。
"""

__author__ = 'Richard'
__version__ = '2021-07-17'

import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class SelectElement(object):
    # 下拉选择器元素
    select_dropdown_items = (
        By.CSS_SELECTOR,
        'body > div.el-select-dropdown.el-popper:not([style*="display: none;"]) ul li')

    def __init__(self, driver: WebDriver):
        """
        :param driver: 驱动
        """
        self.driver = driver

    def _find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def select_item(self, item_text):
        """
        下拉选择元素
        :param item_text: 元素文本
        :return: None
        """
        time.sleep(0.3)

        items = self._find_elements(self.select_dropdown_items)
        for item in items:
            if item.text == item_text:
                item.click()

        time.sleep(0.3)
        pass
