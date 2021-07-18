"""Dialog 对话框

在保留当前页面状态的情况下，告知用户并承载相关操作。
"""

__author__ = 'Richard'
__version__ = '2021-07-17'

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


# Confirm Dialog  弹框
class DialogConfirmElement(object):
    cancel_btn = (
        By.CSS_SELECTOR,
        'div.el-dialog__wrapper:not([style*="display: none;"]) div.el-dialog__footer > span > div:nth-child(1) > div')

    confirm_btn = (
        By.CSS_SELECTOR,
        'div.el-dialog__wrapper:not([style*="display: none;"]) div.el-dialog__footer > span > div:nth-child(2) > div')

    def __init__(self, driver: WebDriver):
        """Confirm Dialog
        :param driver: 驱动
        """
        self.driver = driver

    def _find_element(self, locator):
        return self.driver.find_element(*locator)

    def cancel(self):
        self._find_element(self.cancel_btn).click()

    def confirm(self):
        self._find_element(self.confirm_btn).click()
