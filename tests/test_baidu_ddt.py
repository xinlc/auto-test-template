""" 测试Baidu

通过读取Excel方式驱动测试用例
"""

__author__ = 'Richard'
__version__ = '2021-07-11'

import logging
import os
import time

import allure
import pytest
import pandas as pd

from data.baidu_data import get_data_list
from pages.baidu_search_page import BaiduSearchPage
from common import utils

# 使用 pytest.ini 日志配置
# logger = logging.getLogger(__name__)

# 使用自定义配置
logger = utils.get_logger(__name__)


# 读取Excel文件 -- Pandas
def read_data_from_pandas(excel_file, sheet_name):
    if not os.path.exists(excel_file):
        raise ValueError("File not exists")
    s = pd.ExcelFile(excel_file)
    df = s.parse(sheet_name)
    return df.values.tolist()


"""
 allure 标注描述顺序：
    epic(史诗描述) -> feature(模块名称) -> story(用户故事) -> title(用例标题)、testcase(测试用例的链接地址)、
    issue(缺陷链接)、link(链接) 、description(用例描述) -> severity(用例等级: allure_results.severity_level) -> step(操作步骤)
    attachment(给报告添加附件)
"""


@allure.epic("Baidu epic 相当于总体描述 - 史诗(安徒生童话故事)")
@allure.feature("Baidu 测试模块 - 模块名称")
class TestBaidu:
    data = get_data_list()

    # testcase 和 issue 用的都是 link 只是显示样式不一样
    # @allure_results.testcase("https://baidu.com", '测试用例,点我一下')
    # @allure_results.issue("baidu", 'Bug 链接,点我一下')

    # @allure_results.severity(allure_results.severity_level.NORMAL)
    # allure_results.severity 用例级别
    # blocker：阻塞缺陷（功能未实现，无法下一步）
    # critical：严重缺陷（功能点缺失）
    # normal： 一般缺陷（边界情况，格式错误）
    # minor：次要缺陷（界面错误与ui需求不符）
    # trivial： 轻微缺陷（必须项无提示，或者提示不规范）

    @allure.story("Baidu搜索 - 用户故事")
    @allure.link('https://baidu.com', name="Baidu搜索链接")
    @allure.description("""
    测试Baidu搜索
    """)
    @allure.title("成功登录，测试数据是：{search_string},{expect_string}")
    # @pytest.mark.parametrize('search_string, expect_string',
    #                          read_data_from_pandas(r'../data/baidu_ddt.xlsx', 'Sheet1'))
    @pytest.mark.parametrize('search_string, expect_string', data)
    def test_baidu_search(self, login, search_string, expect_string):
        driver, s, base_url = login
        # driver.get(base_url)

        # # 动态标题设置
        # allure.dynamic.title('动态标题，测试数据是：%s , %s' % (search_string, expect_string))

        logger.info("开始测试Baidu搜索")

        search_page = BaiduSearchPage(driver)
        search_page.goto_search_page(base_url)
        search_page.input_search_string(search_string)
        # search_page.save_screenshot("截图啊")
        search_page.search()

        time.sleep(2)

        search_results = search_page.get_search_results()

        logger.info(search_results)

        assert (expect_string in search_results) is True, '未找到搜索内容'


if __name__ == "__main__":
    # 命令行 运行 pytest tests/test_baidu_ddt.py --alluredir=./reports/allure_results --clean-alluredir
    # --clean-alluredir 会给之前的报告清空

    # pytest.main(['-s', '-v', os.path.basename(__file__)])
    # 注意：使用 PyCharm 运行时，默认 Pytest 无法生成 allure 报告（命令行运行不受影响），
    # 需要设置 Preferences ->Tools -> Python Integrated Tools -> Testring -> Default test runner -> Unittests
    pytest.main(['-sv', os.path.basename(__file__), '--alluredir=../reports/allure_results'])
