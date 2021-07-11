""" selenium 工具

初始化 SE
"""

__author__ = 'Richard'
__version__ = '2021-07-10'

from selenium import webdriver


class SeleniumHelper(object):

    # 初始化 webdriver
    @staticmethod
    def initial_driver(browser_name='chrome'):
        browser_name = browser_name.lower()
        if browser_name not in {'chrome', 'firefox', 'ff', 'ie'}:
            browser_name = 'chrome'
        if browser_name == 'chrome':
            browser = webdriver.Chrome()
        elif browser_name in ('firefox', 'ff'):
            browser = webdriver.Firefox()
        elif browser_name == 'ie':
            webdriver.Ie()
        browser.maximize_window()
        browser.implicitly_wait(60)
        return browser

    # 把获取的cookie转换成Selenium / WebDriver能识别的格式
    @staticmethod
    def cookie_to_selenium_format(cookie):
        cookie_selenium_mapping = {'path': '', 'secure': '', 'name': '', 'value': '', 'expires': ''}
        cookie_dict = {}
        if getattr(cookie, 'domain_initial_dot'):
            cookie_dict['domain'] = '.' + getattr(cookie, 'domain')
        else:
            cookie_dict['domain'] = getattr(cookie, 'domain')
        for k in list(cookie_selenium_mapping.keys()):
            key = k
            value = getattr(cookie, k)
            cookie_dict[key] = value
        return cookie_dict
