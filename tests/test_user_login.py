""" 用户登录 Test

用户登录测试
"""

__author__ = 'Richard'
__version__ = '2021-07-10'

import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep

from pages.user_login_page import UserLoginPage


class TestUserLogin(object):
    login_data = [
        ('mail@lichao.xin', '123456', '首页')
    ]

    def setup_class(self):
        options = webdriver.ChromeOptions()
        # 忽略https安全拦截
        options.add_argument('--ignore-certificate-errors')

        # 无头模式
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')

        # 初始化 webdriver
        self.driver = webdriver.Chrome(options=options)

        self.loginPage = UserLoginPage(self.driver)
        self.loginPage.goto_login_page()

    def teardown_class(self):
        self.driver.quit()

    # 测试用户登录
    @allure.title("测试用户登录，测试数据是：{username},{pwd},{expected}")
    @pytest.mark.parametrize('username, pwd, expected', login_data)
    def test_user_login(self, username, pwd, expected):

        # 输入用户名
        self.loginPage.input_username(username)
        # 输入密码
        self.loginPage.input_pwd(pwd)
        # 点击登录
        self.loginPage.click_login_btn()

        sleep(3)
        # 验证
        if username != '':
            # 等待提示框
            WebDriverWait(self.driver, 5).until(EC.title_is(expected))

            # 取反
            # WebDriverWait(self.driver, 5).until_not(EC.title_is(expected))

            sleep(3)
            # 验证
            assert self.driver.title == expected
        else:
            # 等待提示框
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            assert alert.text == expected
            alert.accept()


if __name__ == '__main__':
    pytest.main(['-sv', 'test_user_login.py'])
