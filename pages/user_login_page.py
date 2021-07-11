""" 用户登录 PO

用户登录
"""

__author__ = 'Richard'
__version__ = '2021-07-10'

from selenium.webdriver.common.by import By
from common.base_page import BasePage


class UserLoginPage(BasePage):
    target_page = 'https://xxx.com/login'
    username_input = (By.NAME, 'account')
    pwd_input = (By.NAME, 'password')
    login_btn = (By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/form/button')

    def __init__(self, driver):
        super().__init__(driver)

    def goto_login_page(self):
        self.driver.get(self.target_page)
        self.driver.maximize_window()

    def input_username(self, username):
        self.clear(*self.username_input)
        self.send_text(username, *self.username_input)

    def input_pwd(self, pwd):
        self.clear(*self.pwd_input)
        self.send_text(pwd, *self.pwd_input)

    def click_login_btn(self):
        self.click(*self.login_btn)
