"""MessageBox 弹框组件

模拟系统的消息提示框而实现的一套模态对话框组件，用于消息提示、确认消息和提交内容。
MessageBox 的作用是美化系统自带的 alert、confirm 和 prompt。
"""

__author__ = 'Richard'
__version__ = '2021-07-17'

import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Alert 弹框
class MessageAlertElement(object):
    confirm_btn = (
        By.CSS_SELECTOR,
        'body > div.el-message-box__wrapper:not([style*="display: none;"]) .el-message-box__btns > button:nth-child(2)')

    def __init__(self, driver: WebDriver):
        """Alert message
        :param driver: 驱动
        """
        self.driver = driver

    def _find_element(self, locator):
        return self.driver.find_element(*locator)

    def confirm(self):
        self._find_element(self.confirm_btn).click()


# Confirm 弹框
class MessageConfirmElement(object):
    cancel_btn = (
        By.CSS_SELECTOR,
        'body > div.el-message-box__wrapper:not([style*="display: none;"]) .el-message-box__btns > button:nth-child(1)')

    confirm_btn = (
        By.CSS_SELECTOR,
        'body > div.el-message-box__wrapper:not([style*="display: none;"]) .el-message-box__btns > button:nth-child(2)')

    def __init__(self, driver: WebDriver):
        """Confirm message
        :param driver: 驱动
        """
        self.driver = driver

    def _find_element(self, locator):
        return self.driver.find_element(*locator)

    def cancel(self):
        self._find_element(self.cancel_btn).click()

    def confirm(self):
        self._find_element(self.confirm_btn).click()
