"""Cascader 级联选择器

当一个数据集合有清晰的层级结构时，可通过级联选择器逐级查看并选择。
"""

__author__ = 'Richard'
__version__ = '2021-07-17'

import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class CascaderElement(object):
    # 级联选择器第一级选择项集合
    first_level_items_loc = (
        By.CSS_SELECTOR,
        'body > div.el-cascader__dropdown.el-popper:not([style*="display: none;"]) > div.el-cascader-panel > div:nth-child(1) ul li')

    # 级联选择器第二级选择项集合
    second_level_items_loc = (
        By.CSS_SELECTOR,
        'body > div.el-cascader__dropdown.el-popper:not([style*="display: none;"]) > div.el-cascader-panel > div:nth-child(2) ul li')

    def __init__(self, driver: WebDriver):
        """
        :param driver: 驱动
        """
        self.driver = driver

    def _find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def select_first_level_item(self, item_text):
        """选择级联下拉元素"""

        time.sleep(0.3)
        items = self._find_elements(self.first_level_items_loc)
        for item in items:
            if item.text == item_text:
                item.click()
                time.sleep(0.3)
                WebDriverWait(self.driver, 5).until_not(
                    lambda driver: item.find_element_by_css_selector('i.el-icon-loading'))
        pass

    def select_second_level_item(self, item_text):
        """选择级联下拉元素"""

        time.sleep(0.3)
        items = self._find_elements(self.second_level_items_loc)
        for item in items:
            if item.text == item_text:
                item.click()
        pass
