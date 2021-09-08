""" POM 基类

POM 通用操作
"""

__author__ = 'Richard'
__version__ = '2021-07-10'

import time
import json
from datetime import datetime
from typing import Union

import allure
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from common import utils
from common.page_objects import PageObject, PageElement
from common.requests_helper import SharedAPI
from common.selenium_helper import SeleniumHelper

logger = utils.get_logger(__name__)

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

    def wait_for_element_to_be_visible(self, locator, timeout=None):
        """等待元素可见"""
        start_time = time.time()
        try:
            logger.info("开始等待页面元素<{}>是否可见.".format(locator))
            t = self.default_timeout if timeout is None else timeout
            WebDriverWait(self.driver, t, poll_frequency=self.default_poll_delay).until(
                EC.visibility_of_element_located(locator))
        except Exception as e:
            logger.error("页面元素<{}>等待可见失败！".format(locator))
            raise e
        else:
            end_time = time.time()
            logger.info("页面元素<{}>等待可见，等待时间：{}秒.".format(locator, round(end_time - start_time, 2)))

    def wait_for_element_to_be_clickable(self, locator, timeout=None) -> bool:
        """
        等待元素可点击
        :param locator: 定位器
        :param timeout: 等待超时
        :return: 是否可点击
        """
        t = self.default_timeout if timeout is None else timeout
        return WebDriverWait(self.driver, t, poll_frequency=self.default_poll_delay).until(
            EC.element_to_be_clickable(locator))

    def wait_ready(self, timeout=10):
        """等待页面加载完毕"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)

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

    def click_by_script(self, element):
        """
        点击元素
        :param element: 点击元素
        """
        self.driver.execute_script('arguments[0].click();', element)

    def click_on_element(self, on_element):
        """
        点击元素
        :param on_element: 点击元素
        """
        ActionChains(self.driver).click(on_element).perform()

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

    def save_screenshot(self, name):
        """页面截屏
        :param name: 说明
        """
        file = utils.get_screenshot_as_file(self.driver, name)
        allure.attach(file, name, allure.attachment_type.PNG)

    def switch_to_frame(self, locator, timeout=None):
        """
        切换iframe页面
        :param locator: 定位器
        :param timeout: 等待超时
        """
        t = self.default_timeout if timeout is None else timeout
        WebDriverWait(self.driver, t, poll_frequency=self.default_poll_delay).until(
            EC.frame_to_be_available_and_switch_to_it(locator))

    def switch_to_default_content(self):
        """切换iframe到main页面"""
        self.driver.switch_to.default_content()

    def switch_to_parent(self):
        """切换iframe到上一层页面"""
        self.driver.switch_to.parent_frame()

    def switch_to_windows(self, locator, timeout=None):
        """
        窗口切换
        :param locator: 点击出现窗口的按钮定位器
        :param timeout: 等待超时
        """

        # 获取点击之前的窗口总数
        cur_handles = self.driver.window_handles

        # 点击按钮后新的窗口出现
        self.find_element(locator, timeout).click()

        t = self.default_timeout if timeout is None else timeout
        WebDriverWait(self.driver, t, poll_frequency=self.default_poll_delay).until(
            EC.new_window_is_opened(cur_handles))

        # 再次获取窗口总数
        wins = self.driver.window_handles

        # 切换到新的页面
        self.driver.switch_to.window(wins[-1])

    def alert_close(self, alert_type='alert', text=None, timeout=None):
        """
        弹框关闭
        :param alert_type: 弹框类型：alert/confirm/prompt
        :param text: prompt弹框输入的文本
        :param timeout: 等待时间
        :return:
        """
        t = self.default_timeout if timeout is None else timeout
        WebDriverWait(self.driver, t, poll_frequency=self.default_poll_delay).until(EC.alert_is_present())

        if alert_type in ['alert', 'confirm']:
            self.driver.switch_to.alert.accept()
        elif alert_type == 'prompt':
            self.driver.switch_to.alert.send_keys(text)
            self.driver.switch_to.alert.accept()

    def select_action(self, locator, content, select_type, timeout=None):
        """
        Select操作
        :param locator: 定位器
        :param content: select_by_方法的入参
        :param select_type: select类型
        :param timeout: 等待超时
        """

        self.wait_for_element_to_be_clickable(locator, timeout)

        elem = self.find_element(locator)
        if select_type == 'index':
            Select(elem).select_by_index(content)
        elif select_type == 'value':
            Select(elem).select_by_value(content)
        elif select_type == 'text':
            Select(elem).select_by_visible_text(content)
