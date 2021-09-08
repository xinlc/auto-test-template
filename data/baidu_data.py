""" Baidu数据

baidu数据
"""

__author__ = 'Richard'
__version__ = '2021-07-12'

import os

from common import utils


def get_data_list():
    curr_path = os.path.dirname(os.path.abspath(__file__))
    excel_file = os.path.join(curr_path, 'baidu_ddt.xlsx')
    sheet_name = 'Sheet1'
    # types = {'expect_string': str, 'search_string': str}
    types = str
    return utils.read_data_from_excel(excel_file, sheet_name, types)
    # return utils.read_data_dic_from_excel(excel_file, sheet_name)


if __name__ == '__main__':
    data = get_data_list()

    print(data)
