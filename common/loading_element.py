"""Loading 加载组件

加载数据时显示动效。
"""

__author__ = 'Richard'
__version__ = '2021-07-17'

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.base_page import BasePage


# 区域加载
class LoadingElement(BasePage):
    loading = (By.CSS_SELECTOR, 'div.el-loading-mask:not([class*="is-fullscreen"])')

    def _find_element(self, locator):
        return self.driver.find_element(*locator)

    def wait_loading(self, timeout=10):
        """延迟等待，加载提示关闭"""
        time.sleep(0.5)
        WebDriverWait(self.driver, timeout).until_not(EC.visibility_of(self._find_element(self.loading)))


# 整页加载
class LoadingFullscreenElement(BasePage):
    loading = (By.CSS_SELECTOR, 'div.el-loading-mask.is-fullscreen')

    def _find_element(self, locator):
        return self.driver.find_element(*locator)

    def wait_loading(self, timeout=10):
        """延迟等待，加载提示关闭"""
        time.sleep(0.5)
        WebDriverWait(self.driver, timeout).until_not(EC.visibility_of(self._find_element(self.loading)))
