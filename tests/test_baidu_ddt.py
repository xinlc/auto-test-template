""" 测试Baidu

通过读取Excel方式驱动测试用例
"""

__author__ = 'Richard'
__version__ = '2021-07-11'

import os
import time
import pytest
import pandas as pd
from pages.baidu_search_page import BaiduSearchPage


# 读取Excel文件 -- Pandas
def read_data_from_pandas(excel_file, sheet_name):
    if not os.path.exists(excel_file):
        raise ValueError("File not exists")
    s = pd.ExcelFile(excel_file)
    df = s.parse(sheet_name)
    return df.values.tolist()


class TestBaidu:
    @pytest.mark.parametrize('search_string, expect_string',
                             read_data_from_pandas(r'../data/baidu_ddt.xlsx', 'Sheet1'))
    def test_baidu_search(self, login, search_string, expect_string):
        driver, s, base_url = login
        # driver.get(base_url)

        search_page = BaiduSearchPage(driver)
        search_page.goto_search_page(base_url)
        search_page.input_search_string(search_string)
        search_page.search()

        time.sleep(2)

        search_results = search_page.get_search_results()

        print(search_results)

        assert (expect_string in search_results) is True


if __name__ == "__main__":
    pytest.main(['-s', '-v', 'test_baidu_ddt.py'])
