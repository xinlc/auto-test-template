"""Message 消息提示组件

常用于主动操作后的反馈提示。
"""

__author__ = 'Richard'
__version__ = '2021-07-17'

from typing import Union

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common import utils
from common.base_page import BasePage

logger = utils.get_logger(__name__)


class MessageElement(BasePage):
    # class 标识，用于区分消息
    __info_class_flag = 'el-message--info'
    __success_class_flag = 'el-message--success'
    __warning_class_flag = 'el-message--warning'
    __error_class_flag = 'el-message--error'

    # 消息
    current_msg_elem = None
    # 消息 class: "el-message el-message--success"
    current_msg_class = ''
    # 消息内容
    current_msg_content = '获取消息内容失败'

    # 多个消息集合
    message_locator = (By.CSS_SELECTOR, 'body > div.el-message')
    # 消息内容
    message_content_with_context = (By.CSS_SELECTOR, '.el-message__content')

    def __find_message(self, msg=None, timeout=10):
        """
        :param msg: 消息内容
        :param timeout: default 10s
        :return: True or False
        :
        """
        logger.debug("查找提示消息")
        msg_list = None
        msg_elem = None
        msg_content = None
        try:
            msg_list = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_any_elements_located(self.message_locator))
            logger.debug("找到提示消息集合：%s", len(msg_list))
        except TimeoutException as exc:
            logger.debug("查找提示消息发生异常", exc_info=exc)

        # 查找指定内容消息
        if msg_list is not None and msg is not None:
            logger.debug("查找指定消息是否存在：%s", msg)
            for i, item in enumerate(msg_list):
                content = self.find_element(self.message_content_with_context, context=item).text
                if content == msg:
                    logger.debug("查找指定消息在：%s 提示", i)
                    msg_elem = item
                    msg_content = content
                    break

        # 没有指定消息, 获取第一个消息
        elif msg_list is not None:
            msg_elem = msg_list[0]
            msg_content = self.find_element(self.message_content_with_context, context=msg_elem).text
            logger.debug("没有指定消息，默认查找第一个消息: %s", msg_content)

        if msg_elem is not None:
            logger.debug("找到消息元素")
            self.current_msg_elem = msg_elem
            self.current_msg_content = msg_content
            self.current_msg_class = msg_elem.get_attribute("class")
            logger.debug("消息内容为：%s", self.current_msg_content)
            return True
        else:
            logger.debug("未找到消息元素")
            return False

    def is_success(self, msg=None, timeout=10) -> bool:
        """
        :param msg: 消息内容
        :param timeout: default 10s
        :return: bool
        """
        fined = self.__find_message(msg, timeout)

        if fined and self.__success_class_flag in self.current_msg_class:
            return True
        return False

    def is_warning(self, msg=None, timeout=10) -> bool:
        """
        :param msg: 消息内容
        :param timeout: default 10s
        :return: bool
        """
        fined = self.__find_message(msg, timeout)

        if fined and self.__warning_class_flag in self.current_msg_class:
            return True
        return False

    def is_error(self, msg=None, timeout=10) -> bool:
        """
        :param msg: 消息内容
        :param timeout: default 10s
        :return: bool
        """
        fined = self.__find_message(msg, timeout)

        if fined and self.__error_class_flag in self.current_msg_class:
            return True
        return False

    def get_message(self) -> str:
        """获取消息内容
        先调用 is_success 再调用这个哦^_^
        """
        return self.current_msg_content

    def wait_message_close(self, timeout=10):
        """等待提示关闭"""
        if self.current_msg_elem is not None:
            WebDriverWait(self.driver, timeout).until(EC.staleness_of(self.current_msg_elem))
            logger.debug("提示消息已关闭：%s", self.current_msg_content)


class MessageElementFoo(object):
    # 第一个成功提示内容元素
    # css选择器无法按index查找，改为xpath实现
    # 这里的 nth-child(1) 是找 body 下第一个 div 元素，如果这个div 没有 el-message--success 和 el-message class是找不到的
    # 只用css 不写div 使用 nth-of-type(1) 也无法找到，原因是会用css会先查找元素，再选择同类型元素的第一个元素，同类型的第一个元素并没有 el-message
    # message_success_content = (
    #     By.CSS_SELECTOR,
    #     'body > div.el-message--success.el-message:nth-child(1) .el-message__content')

    # 第一个成功提示内容元素
    message_success_content = (
        By.XPATH,
        'html/body/div[@class="el-message el-message--success"][1]/p')

    # 警告提示内容元素
    message_warning_content = (
        By.XPATH,
        'html/body/div[@class="el-message el-message--warning"][1]/p')

    # 错误提示内容元素
    message_error_content = (
        By.XPATH,
        'html/body/div[@class="el-message el-message--error"][1]/p')

    # 多个消息内容集合
    message_contents = (
        By.CSS_SELECTOR,
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
        logger.debug("查找提示消息")
        msg: Union[bool, WebElement]
        message_content = None
        try:
            msg = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            logger.debug("找到提示消息：%s", msg.text)
        except TimeoutException as exc:
            msg = False
            logger.debug("查找提示消息发生异常", exc_info=exc)

        if msg:
            message_content = msg.text
            # 等待提示关闭
            WebDriverWait(self.driver, timeout).until(EC.staleness_of(msg))
            logger.debug("提示消息已关闭：%s", message_content)

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
