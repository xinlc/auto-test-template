"""Select 选择器

当选项过多时，使用下拉菜单展示并选择内容。
"""

__author__ = 'Richard'
__version__ = '2021-07-17'

import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from common import utils
from common.base_page import BasePage

logger = utils.get_logger(__name__)


class SelectElement(BasePage):
    # 下拉选择器元素
    select_dropdown_items = (
        By.CSS_SELECTOR,
        'body > div.el-select-dropdown.el-popper:not([style*="display: none;"]) ul li')

    # 下拉选择元素 xpath
    select_dropdown_item_xpath_loc = '//body/div[contains(@class,"el-select-dropdown") and not(contains(@style,"display: none;"))]//ul/li/span[text()="{}"]'

    def select_item_css(self, item_text):
        """
        下拉选择元素
        :param item_text: 元素文本
        :return: None
        """
        logger.debug("选择下拉选择器项：%s", item_text)
        time.sleep(0.3)
        items = self.find_elements(self.select_dropdown_items)
        logger.debug("选择项集合：%s", len(items))
        for i, item in enumerate(items):
            if item.text == item_text:
                item.click()
                logger.debug("找到并点击选择器选择项：%s", i)
                break

        time.sleep(0.3)
        pass

    def select_item(self, item_text):
        """
        下拉选择元素
        :param item_text: 元素文本
        :return: None
        """
        locator = (
            By.XPATH,
            self.select_dropdown_item_xpath_loc.format(item_text)
        )
        if self.wait_for_element_to_be_clickable(locator):
            self.find_element(locator).click()

        pass
