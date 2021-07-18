""" 通用 fixture

通用用例
登录授权
链接DB
"""

__author__ = 'Richard'
__version__ = '2021-07-10'

import pytest
from selenium import webdriver
import requests

USERNAME = 'your username'
PWD = 'your pwd'


# 此方法名可以是你登录的业务代码，也可以是其他，这里暂命名为login
@pytest.fixture(scope="session")
def login():
    driver = webdriver.Chrome()
    # 不建议使用隐式等待，尽可能使用显示等待
    driver.implicitly_wait(10)
    base_url = 'https://www.baidu.com'
    s = requests.Session()

    # # 登录
    # login_page = UserLoginPage(driver)
    # login_page.goto_login_page(base_url)
    # login_page.input_username(USERNAME)
    # login_page.input_pwd(PWD)
    # login_page.click_login_btn()
    #
    # time.sleep(1)

    yield driver, s, base_url

    print('\nturn off requests driver')
    s.close()

    print('turn off browser driver')
    driver.quit()

# @pytest.fixture(scope="function", autouse=True)
# def connect_db():
#     print('connecting db')
#     # 此处写你的链接db的业务逻辑
#     pass
