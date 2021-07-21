""" 用户登录 PO

用户登录
"""

__author__ = 'Richard'
__version__ = '2021-07-10'

import allure
from selenium.webdriver.common.by import By
from common.base_page import BasePage


class UserLoginPage(BasePage):
    target_page = 'https://xxx.com/login'
    username_input = (By.NAME, 'account')
    pwd_input = (By.NAME, 'password')
    login_btn = (By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/form/button')

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("跳转到登录页")
    def goto_login_page(self):
        self.driver.get(self.target_page)

    @allure.step("输入用户名:{1}")
    def input_username(self, username):
        self.clear(self.username_input)
        self.send_text(self.username_input, username)

    @allure.step("输入密码:{1}")
    def input_pwd(self, pwd):
        self.clear(self.pwd_input)
        self.send_text(self.pwd_input, pwd)

    @allure.step("点击登录")
    def click_login_btn(self):
        self.click(self.login_btn)

    @allure.step("执行注销")
    def logout(self):
        print('logout')
