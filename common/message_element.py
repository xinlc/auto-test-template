"""Message 消息提示组件

常用于主动操作后的反馈提示。
"""

__author__ = 'Richard'
__version__ = '2021-07-17'

import time
from typing import Union

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MessageElement(object):
    # 提示内容元素
    # message_info_content = (By.CSS_SELECTOR,
    #                         'body > div.el-message--info.el-message:nth-child(1) .el-message__content')
    message_info_content = (By.CSS_SELECTOR,
                            'body > div.el-message:nth-child(1) .el-message__content')

    # 成功提示内容元素
    message_success_content = (By.CSS_SELECTOR,
                               'body > div.el-message--success.el-message:nth-child(1) .el-message__content')

    # 警告提示内容元素
    message_warning_content = (By.CSS_SELECTOR,
                               'body > div.el-message--warning.el-message:nth-child(1) .el-message__content')

    # 错误提示内容元素
    message_error_content = (By.CSS_SELECTOR,
                             'body > div.el-message--error.el-message:nth-child(1) .el-message__content')

    # 多个消息内容集合
    message_contents = (By.CSS_SELECTOR,
                        'body > div.el-message .el-message__content')

    def __init__(self, driver: WebDriver):
        """
        :param driver: 驱动
        """
        self.driver = driver

    def _find_message(self, locator, timeout):
        """
        :param timeout 默认超时时间
        :return: 成功返回内容，否则返回 False
        """
        msg: Union[bool, WebElement]
        message_content = None
        try:
            msg = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            msg = False

        if msg:
            message_content = msg.text
            # 等待提示关闭
            WebDriverWait(self.driver, timeout).until(EC.staleness_of(msg))

        # 成功返回内容，否则返回
        return message_content if message_content is not None else False

    def is_success(self, timeout=10):
        """
        :param timeout: default 10s
        :return: 成功返回内容，否则返回 False
        """
        return self._find_message(self.message_success_content, timeout)

    def is_warning(self, timeout=10):
        """
        :param timeout: default 10s
        :return: 成功返回内容，否则返回 False
        """
        return self._find_message(self.message_warning_content, timeout)

    def is_error(self, timeout=10):
        """
        :param timeout: default 10s
        :return: 成功返回内容，否则返回 False
        """
        return self._find_message(self.message_error_content, timeout)
