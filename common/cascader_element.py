"""Cascader 级联选择器

当一个数据集合有清晰的层级结构时，可通过级联选择器逐级查看并选择。
"""

__author__ = 'Richard'
__version__ = '2021-07-17'

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common import utils
from common.base_page import BasePage

logger = utils.get_logger(__name__)


class CascaderElement(BasePage):
    # 级联选择器第一级选择项集合
    first_level_items_loc = (
        By.CSS_SELECTOR,
        'body > div.el-cascader__dropdown.el-popper:not([style*="display: none;"]) > div.el-cascader-panel > div:nth-child(1) ul li')

    # 级联选择器第二级选择项集合
    second_level_items_loc = (
        By.CSS_SELECTOR,
        'body > div.el-cascader__dropdown.el-popper:not([style*="display: none;"]) > div.el-cascader-panel > div:nth-child(2) ul li')

    # 级联选择器第三级选择项集合
    third_level_items_loc = (
        By.CSS_SELECTOR,
        'body > div.el-cascader__dropdown.el-popper:not([style*="display: none;"]) > div.el-cascader-panel > div:nth-child(3) ul li')

    # 一级选择元素 xpath
    first_level_item_xpath_loc = '//body/div[contains(@class,"el-cascader__dropdown") and not(contains(@style,"display: none;"))]/div/div[1]//ul/li/span[text()="{}"]'

    # 二级级选择元素 xpath
    second_level_item_xpath_loc = '//body/div[contains(@class,"el-cascader__dropdown") and not(contains(@style,"display: none;"))]/div/div[2]//ul/li/span[text()="{}"]'

    # 三级级选择元素 xpath
    third_level_item_xpath_loc = '//body/div[contains(@class,"el-cascader__dropdown") and not(contains(@style,"display: none;"))]/div/div[3]//ul/li/span[text()="{}"]'

    def __select_item(self, locator, item_text):
        """选择级联下拉元素"""

        time.sleep(0.3)
        items = self.find_elements(locator)
        logger.debug("选择项集合：%s", len(items))
        for i, item in enumerate(items):
            if item.text == item_text:
                item.click()
                logger.debug("找到并点击选择项：%s", i)
                time.sleep(0.3)
                WebDriverWait(self.driver, self.default_timeout).until_not(
                    lambda driver: item.find_element_by_css_selector('i.el-icon-loading'))
                logger.debug("等待下一级选择项加载完毕")
        pass

    def select_first_level_item_css(self, item_text):
        """选择级联下拉元素"""
        logger.debug("选择级联选择器第一级选择项：%s", item_text)
        self.__select_item(self.first_level_items_loc, item_text)

    def select_second_level_item_css(self, item_text):
        """选择级联下拉元素"""
        logger.debug("选择级联选择器第二级选择项：%s", item_text)
        self.__select_item(self.second_level_items_loc, item_text)

    def select_third_level_item_css(self, item_text):
        """选择级联下拉元素"""
        logger.debug("选择级联选择器第三级选择项：%s", item_text)
        self.__select_item(self.third_level_items_loc, item_text)

    def select_first_level_item(self, item_text):
        """选择级联下拉元素"""
        logger.debug("选择级联选择器第一级选择项：%s", item_text)

        locator = (
            By.XPATH,
            self.first_level_item_xpath_loc.format(item_text)
        )
        if self.wait_for_element_to_be_clickable(locator):
            self.click_by_script(self.find_element(locator))

        pass

    def select_second_level_item(self, item_text):
        """选择级联下拉元素"""
        logger.debug("选择级联选择器第二级选择项：%s", item_text)

        locator = (
            By.XPATH,
            self.second_level_item_xpath_loc.format(item_text)
        )
        if self.wait_for_element_to_be_clickable(locator):
            self.click_by_script(self.find_element(locator))

        pass

    def select_third_level_item(self, item_text):
        """选择级联下拉元素"""
        logger.debug("选择级联选择器第三级选择项：%s", item_text)

        locator = (
            By.XPATH,
            self.third_level_item_xpath_loc.format(item_text)
        )
        if self.wait_for_element_to_be_clickable(locator):
            self.click_by_script(self.find_element(locator))

        pass
