"""Dialog 对话框

在保留当前页面状态的情况下，告知用户并承载相关操作。
"""

__author__ = 'Richard'
__version__ = '2021-07-17'

from selenium.webdriver.common.by import By

from common import utils
from common.base_page import BasePage

logger = utils.get_logger(__name__)


# Confirm Dialog  弹框
class DialogConfirmElement(BasePage):
    # dialog = (By.CSS_SELECTOR, 'div.el-dialog__wrapper:not([style*="display: none;"])')

    cancel_btn = (
        By.CSS_SELECTOR,
        'div.el-dialog__wrapper:not([style*="display: none;"]) div.el-dialog__footer > span > div:nth-child(1) > div')

    confirm_btn = (
        By.CSS_SELECTOR,
        'div.el-dialog__wrapper:not([style*="display: none;"]) div.el-dialog__footer > span > div:nth-child(2) > div')

    def cancel(self):
        self.find_element(self.cancel_btn).click()
        logger.debug("点击取消按钮")

    def confirm(self):
        self.find_element(self.confirm_btn).click()
        logger.debug("点击确定按钮")
