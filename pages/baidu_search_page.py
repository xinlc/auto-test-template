""" Baidu搜索 PO

搜索页面
"""

__author__ = 'Richard'
__version__ = '2021-07-11'

import allure

from common.base_page import BasePage
from common.page_objects import PageElement


class BaiduSearchPage(BasePage):
    target_page = '/'
    kw = PageElement(id_='kw')
    su = PageElement(id_='su')
    search_results = PageElement(xpath='//*[@id="1"]/h3/a')

    # 尽可能用 css 选择器，性能会更好，id不能已数字开头
    # search_results = PageElement(css='div[id="1"] > h3 > a')

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("跳转到搜索页 {1}")
    def goto_search_page(self, base_url):
        self.driver.get(base_url + self.target_page)

    @allure.step("输入搜索关键字 {word}")
    def input_search_string(self, word):
        self.kw = word

    @allure.step("点击搜索按钮")
    def search(self):
        self.su.click()

    @allure.step("获取搜索结果集")
    def get_search_results(self) -> str:
        return self.search_results.get_attribute('innerHTML')
