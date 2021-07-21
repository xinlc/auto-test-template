"""MessageBox 弹框组件

模拟系统的消息提示框而实现的一套模态对话框组件，用于消息提示、确认消息和提交内容。
MessageBox 的作用是美化系统自带的 alert、confirm 和 prompt。
"""

__author__ = 'Richard'
__version__ = '2021-07-17'

from selenium.webdriver.common.by import By

from common import utils
from common.base_page import BasePage

logger = utils.get_logger(__name__)


# Alert 弹框
class MessageAlertElement(BasePage):
    confirm_btn = (
        By.CSS_SELECTOR,
        'body > div.el-message-box__wrapper:not([style*="display: none;"]) .el-message-box__btns > button:nth-child(2)')

    def confirm(self):
        self.click(self.confirm_btn)
        logger.debug("点击确定按钮")


# Confirm 弹框
class MessageConfirmElement(BasePage):
    cancel_btn = (
        By.CSS_SELECTOR,
        'body > div.el-message-box__wrapper:not([style*="display: none;"]) .el-message-box__btns > button:nth-child(1)')

    confirm_btn = (
        By.CSS_SELECTOR,
        'body > div.el-message-box__wrapper:not([style*="display: none;"]) .el-message-box__btns > button:nth-child(2)')

    def cancel(self):
        self.click(self.cancel_btn)
        logger.debug("点击取消按钮")

    def confirm(self):
        self.click(self.confirm_btn)
        logger.debug("点击确定按钮")
