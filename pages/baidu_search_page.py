""" Baidu搜索 PO

搜索页面
"""

__author__ = 'Richard'
__version__ = '2021-07-11'

from common.base_page import BasePage
from page_objects import PageElement


class BaiduSearchPage(BasePage):
    target_page = '/'
    kw = PageElement(id_='kw')
    su = PageElement(id_='su')
    search_results = PageElement(xpath='//*[@id="1"]/h3/a')
    # 尽可能用 css 选择器，性能会更好，id不能已数字开头
    # search_results = PageElement(css='div[id="1"] > h3 > a')

    def __init__(self, driver):
        super().__init__(driver)

    def goto_search_page(self, base_url):
        self.driver.get(base_url + self.target_page)

    def input_search_string(self, word):
        self.kw = word

    def search(self):
        self.su.click()

    def get_search_results(self):
        return self.search_results.get_attribute('innerHTML')
