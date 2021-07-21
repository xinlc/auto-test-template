""" POM 基类

POM 通用操作
"""

__author__ = 'Richard'
__version__ = '2021-07-10'

from typing import Union

import json
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from common.page_objects import PageObject, PageElement
from common.requests_helper import SharedAPI
from common.selenium_helper import SeleniumHelper

WAIT_TIMEOUT = 5
POLL_DELAY = 0.5


class BasePage(PageObject):

    def __init__(self, driver: WebDriver, default_timeout=WAIT_TIMEOUT, default_poll_delay=POLL_DELAY):
        """
            :arg driver 驱动
        """
        if driver is not None:
            self.driver = driver
        else:
            self.driver = SeleniumHelper.initial_driver()
        super().__init__(driver, default_timeout=default_timeout, default_poll_delay=default_poll_delay)

    def wait_for(self, method, timeout=None) -> Union[WebElement, list[WebElement]]:
        """
        获取指定等待
        :param method: 执行方法
        :param timeout: 等待超时
        :return: 元素 或 元素集合
        """
        t = self.default_timeout if timeout is None else timeout
        return WebDriverWait(self.driver, t, poll_frequency=self.default_poll_delay).until(method)

    def find_element(self, locator, context: WebElement = None, timeout=None) -> WebElement:
        """
        获取元素
        :param locator: 定位器
        :param context: 指定上下文，默认 WebDriver
        :param timeout: 等待超时
        :return: 元素
        """
        # TODO 记录超时异常日志，再抛出异常
        context = self.driver if context is None else context
        return self.wait_for(lambda driver: context.find_element(*locator), timeout)
        # 等待条件改为可见元素, 避免元素还未渲染完成返回，如果就是要获取隐藏元素，单独写查询吧
        # return self.wait_for(lambda driver: EC.visibility_of_element_located(locator)(context), timeout)

    def find_elements(self, locator, context: WebElement = None, timeout=None) -> list[WebElement]:
        """
        获取元素集合
        :param locator: 定位器
        :param context: 指定上下文，默认 WebDriver
        :param timeout: 等待超时
        :return: 元素
        """
        context = self.driver if context is None else context
        return self.wait_for(lambda driver: context.find_elements(*locator), timeout)
        # 等待条件改为可见元素, 避免元素还未渲染完成返回，如果就是要获取隐藏元素，单独写查询吧
        # return self.wait_for(lambda driver: EC.visibility_of_any_elements_located(locator)(context), timeout)

    def send_text(self, locator, text, context: WebElement = None, timeout=None):
        """
        输入文本
        :param locator: 定位器
        :param text: 文本
        :param context: 指定上下文，默认 WebDriver
        :param timeout: 等待超时
        """
        self.find_element(locator, context, timeout).send_keys(text)

    def clear(self, locator, context: WebElement = None, timeout=None):
        """
        清空输入框内容
        :param locator: 定位器
        :param context: 指定上下文，默认 WebDriver
        :param timeout: 等待超时
        """
        self.find_element(locator, context, timeout).clear()

    def click(self, locator, context: WebElement = None, timeout=None):
        """
        点击元素
        :param locator: 定位器
        :param context: 指定上下文，默认 WebDriver
        :param timeout: 等待超时
        """
        # self.find_element(locator, context, timeout).click()
        elem = self.find_element(locator, context, timeout)
        ActionChains(self.driver).click(elem).perform()

    def get_title(self) -> str:
        """
        获取浏览器标题
        :return: 浏览器标题
        """
        return self.driver.title

    def send_key_enter(self):
        """
        发送回车按键到当前焦点
        """
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    def scroll_into_view(self, element: WebElement):
        """滚动至元素指定元素可见位置"""
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_by(self, x, y):
        """窗口滚动"""
        self.driver.execute_script('window.scrollBy(arguments[0],arguments[1])', x, y)

    def scroll_to(self, x, y):
        """窗口滚动"""
        self.driver.execute_script('window.scrollTo(arguments[0],arguments[1])', x, y)
