""" 通用 fixture

通用用例
登录授权
链接DB
"""

__author__ = 'Richard'
__version__ = '2021-07-10'

import platform
import allure
import pytest
from selenium import webdriver
import requests
import time

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
USERNAME = 'your username'
PWD = 'your pwd'


# 测试总耗时
@pytest.fixture(scope='session', autouse=True)
def timer_session_scope():
    start = time.time()
    print('\nstart: {}'.format(time.strftime(DATE_FORMAT, time.localtime(start))))

    # yield 之前代码相当于 setup 内执行
    yield
    # yield 之后代码相当于 teardown 内执行

    finished = time.time()
    print('finished: {}'.format(time.strftime(DATE_FORMAT, time.localtime(finished))))
    print('Total time cost: {:.3f}s'.format(finished - start))


# 每个测试函数总耗时
@pytest.fixture(autouse=True)
def timer_function_scope():
    start = time.time()
    yield
    print(' Time cost: {:.3f}s'.format(time.time() - start))


# 启动驱动
@pytest.fixture(scope="session")
def start_driver():
    options = webdriver.ChromeOptions()
    # 忽略https安全拦截
    options.add_argument('--ignore-certificate-errors')

    sys = platform.system()
    if 'Linux' == sys:
        # Linux 系统 无头模式运行
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # 不建议使用隐式等待，会跟显示等待产生时间叠加效果，尽可能使用BasePage中封装好的显示等待
    # driver.implicitly_wait(1)
    base_url = 'https://www.baidu.com'
    s = requests.Session()

    yield driver, s, base_url

    print('\nturn off requests driver')
    s.close()

    print('turn off browser driver')
    driver.quit()


# 登录用例 - 依赖 start_driver
@allure.title("前置操作：登录")
@pytest.fixture(scope="function")
def login(start_driver):
    driver, s, base_url = start_driver

    # # 登录
    # login_page = UserLoginPage(driver)
    # login_page.goto_login_page(base_url)
    # login_page.input_username(USERNAME)
    # login_page.input_pwd(PWD)
    # login_page.click_login_btn()
    #
    # time.sleep(1)

    yield driver, s, base_url

    # login_page.logout()

    print('执行 logout')


# 参数化多账户测试 (可以通过 `@pytest.mark.parametrize('login_account', data, indirect=True)` 方式传参)
@pytest.fixture(scope="function", params=[
    ('admin', '123456'),
    ('admin2', '123456')
])
def login_account(request, start_driver):
    driver, s, base_url = start_driver
    param = request.param
    print(param)
    # uname = param.username
    # pwd = param.pwd
    #
    # # 登录
    # login_page = UserLoginPage(driver)
    # login_page.goto_login_page(base_url)
    # login_page.input_username(uname)
    # login_page.input_pwd(pwd)
    # login_page.click_login_btn()
    #
    # time.sleep(1)

    yield driver, s, base_url, param

    # login_page.logout()

    print('执行 logout')


# DB 参数
@pytest.fixture(scope="function", params=[
    ('redis', '6379'),
    ('elasticsearch', '9200')
])
def db_param(request):
    return request.param

# # 链接 DB
# @pytest.fixture(autouse=True)
# def connect_db(db_param):
#     print('\nSucceed to connect %s:%s' % db_param)
#
#     yield
#
#     print('\nSucceed to close %s:%s' % db_param)
